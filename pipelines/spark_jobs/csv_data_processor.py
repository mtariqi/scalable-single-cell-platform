# Create a CSV data processor for Spark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

class CSVDataProcessor:
    """Process single-cell data from CSV files"""
    
    def __init__(self, spark_session):
        self.spark = spark_session
    
    def load_csv_data(self):
        """Load single-cell data from CSV files"""
        print("Loading single-cell data from CSV files...")
        
        # Load cell metadata
        cell_metadata = self.spark.read.option("header", "true").csv("/data/raw/cell_metadata.csv")
        
        # Load gene metadata
        gene_metadata = self.spark.read.option("header", "true").csv("/data/raw/gene_metadata.csv")
        
        # Load expression data
        expression_data = self.spark.read.option("header", "true").csv("/data/raw/expression_sample.csv")
        
        print(f"Loaded: {cell_metadata.count()} cells, {gene_metadata.count()} genes")
        return cell_metadata, gene_metadata, expression_data
    
    def process_data(self):
        """Process the single-cell data"""
        print("Processing single-cell data...")
        
        cell_metadata, gene_metadata, expression_data = self.load_csv_data()
        
        # Basic quality control
        print("Performing quality control...")
        cell_metadata = cell_metadata.filter(
            (col("n_genes").cast("int") >= 200) & 
            (col("n_genes").cast("int") <= 5000) &
            (col("mito_percent").cast("double") <= 0.2)
        )
        
        print(f"Cells after QC: {cell_metadata.count()}")
        
        # Convert data types
        cell_metadata = cell_metadata \
            .withColumn("n_genes", col("n_genes").cast("int")) \
            .withColumn("total_counts", col("total_counts").cast("int")) \
            .withColumn("mito_percent", col("mito_percent").cast("double")) \
            .withColumn("umap_1", col("umap_1").cast("double")) \
            .withColumn("umap_2", col("umap_2").cast("double"))
        
        # Save processed data
        print("Saving processed data...")
        cell_metadata.write.mode("overwrite").parquet("/data/processed/cell_metadata.parquet")
        gene_metadata.write.mode("overwrite").parquet("/data/processed/gene_metadata.parquet")
        
        # Generate summary statistics
        summary = cell_metadata.agg(
            count("*").alias("total_cells"),
            countDistinct("cell_type").alias("n_cell_types"),
            countDistinct("sample_id").alias("n_samples"),
            avg("n_genes").alias("avg_genes_per_cell"),
            avg("total_counts").alias("avg_counts_per_cell"),
            avg("mito_percent").alias("avg_mito_percent")
        ).collect()[0]
        
        print("\n📊 SINGLE-CELL DATA SUMMARY:")
        print(f"   Total cells: {summary['total_cells']}")
        print(f"   Cell types: {summary['n_cell_types']}")
        print(f"   Samples: {summary['n_samples']}")
        print(f"   Avg genes/cell: {summary['avg_genes_per_cell']:.1f}")
        print(f"   Avg counts/cell: {summary['avg_counts_per_cell']:.1f}")
        print(f"   Avg mitochondrial %: {summary['avg_mito_percent']:.3f}")
        
        return cell_metadata, gene_metadata

def main():
    spark = SparkSession.builder \
        .appName("CSVSingleCellProcessor") \
        .getOrCreate()
    
    processor = CSVDataProcessor(spark)
    
    try:
        cell_metadata, gene_metadata = processor.process_data()
        print("✅ Single-cell data processing completed successfully!")
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        # Fall back to sample data
        from scRNA_processor import SingleCellProcessor
        print("Falling back to sample data generation...")
        sample_processor = SingleCellProcessor(spark)
        sample_processor.run_analysis_pipeline()
    finally:
        spark.stop()

if __name__ == "__main__":
    main()

