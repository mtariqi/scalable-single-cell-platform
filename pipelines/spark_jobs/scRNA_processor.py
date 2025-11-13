#!/usr/bin/env python
# Create comprehensive Spark jobs
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.ml.feature import VectorAssembler, StandardScaler, PCA
from pyspark.ml.clustering import KMeans, GaussianMixture
import pandas as pd
import numpy as np
import json

class SingleCellProcessor:
    """
    Distributed single-cell RNA-seq data processor
    """
    
    def __init__(self, spark_session):
        self.spark = spark_session
        self.sc = spark_session.sparkContext
        
    def create_sample_data(self, n_cells=10000, n_genes=2000):
        """Create realistic sample single-cell data for testing"""
        print("Generating sample single-cell data...")
        
        # Create cell IDs
        cell_ids = [f"Cell_{i:05d}" for i in range(n_cells)]
        
        # Create sample metadata
        cell_types = np.random.choice(['T-Cell', 'B-Cell', 'Monocyte', 'NK-Cell', 'Dendritic'], 
                                    n_cells, p=[0.3, 0.25, 0.2, 0.15, 0.1])
        
        samples = np.random.choice(['Patient_01', 'Patient_02', 'Patient_03'], n_cells)
        
        # Create metadata DataFrame
        metadata_data = []
        for i, cell_id in enumerate(cell_ids):
            metadata_data.append({
                'cell_id': cell_id,
                'cell_type': cell_types[i],
                'sample_id': samples[i],
                'n_genes': np.random.randint(500, 3000),
                'total_counts': np.random.randint(1000, 20000),
                'mito_percent': np.random.uniform(0.01, 0.15),
                'dataset_name': 'demo_dataset'
            })
        
        metadata_df = self.spark.createDataFrame(metadata_data)
        
        # Create gene expression data (sparse representation)
        expr_data = []
        gene_names = [f"Gene_{i:04d}" for i in range(n_genes)]
        
        for cell_idx, cell_id in enumerate(cell_ids):
            # Sample some genes to be expressed (sparsity)
            n_expressed = np.random.randint(500, 2500)
            expressed_genes = np.random.choice(n_genes, n_expressed, replace=False)
            
            for gene_idx in expressed_genes:
                expression = np.random.gamma(shape=2, scale=2)  # Gamma distribution for counts
                expr_data.append((cell_id, gene_names[gene_idx], float(expression)))
        
        expr_df = self.spark.createDataFrame(expr_data, ["cell_id", "gene_name", "expression"])
        
        print(f"Created sample data: {n_cells} cells, {n_genes} genes")
        return metadata_df, expr_df
    
    def quality_control(self, metadata_df, expr_df, min_genes=200, max_genes=5000, max_mito=0.2):
        """Perform distributed quality control"""
        print("Performing quality control...")
        
        # Filter cells based on QC metrics
        qc_cells = metadata_df.filter(
            (col("n_genes") >= min_genes) & 
            (col("n_genes") <= max_genes) &
            (col("mito_percent") <= max_mito)
        )
        
        # Filter expression data to only include QC-passed cells
        qc_expr = expr_df.join(qc_cells.select("cell_id"), "cell_id", "inner")
        
        print(f"Cells after QC: {qc_cells.count()}")
        return qc_cells, qc_expr
    
    def normalize_expression(self, expr_df, scale_factor=10000):
        """Normalize expression data"""
        print("Normalizing expression data...")
        
        # Calculate size factors per cell
        cell_totals = expr_df.groupBy("cell_id").agg(
            sum("expression").alias("total_expression")
        )
        
        # Normalize and log transform
        normalized_expr = expr_df.join(cell_totals, "cell_id").withColumn(
            "normalized_expression",
            log1p(col("expression") / col("total_expression") * scale_factor)
        ).select("cell_id", "gene_name", "normalized_expression")
        
        return normalized_expr
    
    def run_analysis_pipeline(self):
        """Run complete analysis pipeline"""
        print("Starting single-cell analysis pipeline...")
        
        # Create sample data
        metadata_df, expr_df = self.create_sample_data(n_cells=5000, n_genes=1000)
        
        # Quality control
        qc_metadata, qc_expr = self.quality_control(metadata_df, expr_df)
        
        # Normalization
        normalized_expr = self.normalize_expression(qc_expr)
        
        # Save results
        print("Saving results...")
        qc_metadata.write.mode("overwrite").parquet("/data/processed/cell_metadata.parquet")
        normalized_expr.write.mode("overwrite").parquet("/data/processed/normalized_expression.parquet")
        
        # Generate summary statistics
        summary = qc_metadata.agg(
            count("*").alias("total_cells"),
            countDistinct("cell_type").alias("n_cell_types"),
            countDistinct("sample_id").alias("n_samples"),
            avg("n_genes").alias("avg_genes_per_cell"),
            avg("mito_percent").alias("avg_mito_percent")
        ).collect()[0]
        
        print("\n📊 ANALYSIS SUMMARY:")
        print(f"   Total cells: {summary['total_cells']}")
        print(f"   Cell types: {summary['n_cell_types']}")
        print(f"   Samples: {summary['n_samples']}")
        print(f"   Avg genes/cell: {summary['avg_genes_per_cell']:.1f}")
        print(f"   Avg mitochondrial %: {summary['avg_mito_percent']:.3f}")
        
        return qc_metadata, normalized_expr

def main():
    spark = SparkSession.builder \
        .appName("SingleCellProcessor") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    processor = SingleCellProcessor(spark)
    
    try:
        metadata_df, expr_df = processor.run_analysis_pipeline()
        print("✅ Analysis pipeline completed successfully!")
    except Exception as e:
        print(f"❌ Error in analysis pipeline: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()

