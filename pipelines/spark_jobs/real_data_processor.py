# Create a real data processor
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import scanpy as sc
import pandas as pd
import numpy as np
import os

class RealDataProcessor:
    """
    Process real single-cell data from common formats (H5AD, MTX, 10X)
    """
    
    def __init__(self, spark_session):
        self.spark = spark_session
        
    def load_10x_data(self, data_dir):
        """Load 10X Genomics data"""
        print(f"Loading 10X data from {data_dir}")
        
        # Check for 10X files
        matrix_file = os.path.join(data_dir, "matrix.mtx.gz")
        features_file = os.path.join(data_dir, "features.tsv.gz")
        barcodes_file = os.path.join(data_dir, "barcodes.tsv.gz")
        
        if os.path.exists(matrix_file):
            adata = sc.read_10x_mtx(data_dir)
        else:
            # Try H5 format
            h5_file = os.path.join(data_dir, "filtered_feature_bc_matrix.h5")
            if os.path.exists(h5_file):
                adata = sc.read_10x_h5(h5_file)
            else:
                raise FileNotFoundError("No 10X data files found")
        
        return self.anndata_to_spark(adata)
    
    def load_h5ad(self, file_path):
        """Load H5AD file"""
        print(f"Loading H5AD file: {file_path}")
        adata = sc.read_h5ad(file_path)
        return self.anndata_to_spark(adata)
    
    def anndata_to_spark(self, adata):
        """Convert AnnData object to Spark DataFrames"""
        print(f"Converting AnnData: {adata.shape[0]} cells, {adata.shape[1]} genes")
        
        # Cell metadata
        cell_metadata = adata.obs.reset_index().rename(columns={'index': 'cell_id'})
        cell_metadata_df = self.spark.createDataFrame(cell_metadata)
        
        # Gene metadata
        gene_metadata = adata.var.reset_index().rename(columns={'index': 'gene_id'})
        
        # Expression data (convert to long format for Spark)
        print("Converting expression matrix to Spark format...")
        
        # For large datasets, process in chunks
        chunk_size = 10000
        n_cells = adata.shape[0]
        expr_dfs = []
        
        for start_idx in range(0, n_cells, chunk_size):
            end_idx = min(start_idx + chunk_size, n_cells)
            chunk_data = []
            
            # Convert sparse matrix to COO format for the chunk
            X_chunk = adata.X[start_idx:end_idx]
            if hasattr(X_chunk, 'tocoo'):
                X_chunk = X_chunk.tocoo()
                
                for i, j, v in zip(X_chunk.row, X_chunk.col, X_chunk.data):
                    if v != 0:  # Store non-zero values only
                        cell_id = adata.obs_names[start_idx + i]
                        gene_id = adata.var_names[j]
                        chunk_data.append((cell_id, gene_id, float(v)))
            
            # Create DataFrame for chunk
            if chunk_data:
                chunk_df = self.spark.createDataFrame(
                    chunk_data, 
                    ["cell_id", "gene_id", "expression"]
                )
                expr_dfs.append(chunk_df)
        
        # Union all chunks
        if expr_dfs:
            expr_df = expr_dfs[0]
            for df in expr_dfs[1:]:
                expr_df = expr_df.union(df)
        else:
            # Fallback: create empty DataFrame
            expr_df = self.spark.createDataFrame([], StructType([
                StructField("cell_id", StringType()),
                StructField("gene_id", StringType()),
                StructField("expression", DoubleType())
            ]))
        
        print(f"Expression data: {expr_df.count()} records")
        return cell_metadata_df, expr_df, gene_metadata
    
    def process_real_dataset(self, input_path, output_dir):
        """Process a real single-cell dataset"""
        print(f"Processing real dataset: {input_path}")
        
        # Determine file type and load
        if input_path.endswith('.h5ad'):
            cell_metadata, expr_data, gene_metadata = self.load_h5ad(input_path)
        elif os.path.isdir(input_path):
            cell_metadata, expr_data, gene_metadata = self.load_10x_data(input_path)
        else:
            raise ValueError(f"Unsupported file format: {input_path}")
        
        # Quality control
        print("Performing quality control...")
        cell_metadata = cell_metadata.filter(
            (col("n_genes") >= 200) & 
            (col("n_genes") <= 5000) &
            (col("mito_percent") <= 0.2)
        )
        
        # Normalize
        print("Normalizing expression data...")
        cell_totals = expr_data.groupBy("cell_id").agg(
            sum("expression").alias("total_counts")
        )
        
        normalized_expr = expr_data.join(cell_totals, "cell_id").withColumn(
            "normalized_expression",
            log1p(col("expression") / col("total_counts") * 10000)
        )
        
        # Save results
        print("Saving processed data...")
        cell_metadata.write.mode("overwrite").parquet(f"{output_dir}/cell_metadata.parquet")
        normalized_expr.write.mode("overwrite").parquet(f"{output_dir}/normalized_expression.parquet")
        
        # Summary statistics
        summary = cell_metadata.agg(
            count("*").alias("n_cells"),
            countDistinct("cell_type").alias("n_cell_types"),
            avg("n_genes").alias("avg_genes_per_cell"),
            avg("total_counts").alias("avg_counts_per_cell")
        ).collect()[0]
        
        print(f"\n📊 REAL DATASET SUMMARY:")
        print(f"   Cells: {summary['n_cells']}")
        print(f"   Cell types: {summary['n_cell_types']}")
        print(f"   Avg genes/cell: {summary['avg_genes_per_cell']:.1f}")
        print(f"   Avg counts/cell: {summary['avg_counts_per_cell']:.1f}")
        
        return cell_metadata, normalized_expr

def main():
    spark = SparkSession.builder \
        .appName("RealSingleCellProcessor") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    
    processor = RealDataProcessor(spark)
    
    # Check for real data in data/raw/
    raw_data_dir = "/data/raw"
    processed_dir = "/data/processed"
    
    # Look for single-cell data files
    data_files = []
    if os.path.exists(raw_data_dir):
        for file in os.listdir(raw_data_dir):
            if file.endswith('.h5ad') or file.endswith('.h5'):
                data_files.append(os.path.join(raw_data_dir, file))
            elif os.path.isdir(os.path.join(raw_data_dir, file)):
                # Check if it's a 10X directory
                subdir = os.path.join(raw_data_dir, file)
                if any(f.endswith(('.mtx', '.h5', 'features.tsv')) for f in os.listdir(subdir)):
                    data_files.append(subdir)
    
    if data_files:
        print(f"Found {len(data_files)} real dataset(s)")
        for data_file in data_files:
            print(f"Processing: {data_file}")
            try:
                processor.process_real_dataset(data_file, processed_dir)
                print(f"✅ Successfully processed {data_file}")
            except Exception as e:
                print(f"❌ Failed to process {data_file}: {e}")
    else:
        print("No real data found. Using sample data.")
        # Fall back to sample data generator
        from scRNA_processor import SingleCellProcessor
        sample_processor = SingleCellProcessor(spark)
        sample_processor.run_analysis_pipeline()
    
    spark.stop()

if __name__ == "__main__":
    main()

