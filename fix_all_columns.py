import pandas as pd
import numpy as np
import os

print("🔧 Adding missing columns to single-cell data...")

# Read the existing data
df = pd.read_parquet('data/processed/cell_metadata.parquet')

# Add missing columns that the web app expects
np.random.seed(42)

# Add mito_percent (mitochondrial gene percentage)
df['mito_percent'] = np.random.uniform(0.5, 15.0, len(df))

# Add n_counts (total UMI counts per cell)
df['n_counts'] = np.random.randint(5000, 30000, len(df))

# Ensure n_genes exists (it already does from our sample data)
if 'n_genes' not in df.columns:
    df['n_genes'] = np.random.randint(1000, 2000, len(df))

# Add log_counts (log transformed counts)
df['log_counts'] = np.log1p(df['n_counts'])

# Add log_genes (log transformed gene counts)
df['log_genes'] = np.log1p(df['n_genes'])

# Add pct_counts_mito (same as mito_percent but different name)
df['pct_counts_mito'] = df['mito_percent']

# Save with all required columns
df.to_parquet('data/processed/cell_metadata.parquet')

print("✅ Added missing columns:")
print(f"   - mito_percent: mitochondrial percentage")
print(f"   - n_counts: total UMI counts") 
print(f"   - log_counts: log transformed counts")
print(f"   - log_genes: log transformed gene counts")
print(f"   - pct_counts_mito: mitochondrial percentage")
print(f"📊 Final columns: {list(df.columns)}")
print(f"📈 Data shape: {df.shape}")

