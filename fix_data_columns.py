import pandas as pd
import os

print("🔧 Fixing column names in single-cell data...")

# Read the existing data
df = pd.read_parquet('data/processed/cell_metadata.parquet')

# Convert column names to lowercase
df = df.rename(columns={
    'UMAP_1': 'umap_1',
    'UMAP_2': 'umap_2'
})

# Save with corrected column names
df.to_parquet('data/processed/cell_metadata.parquet')
print("✅ Fixed column names:")
print("   UMAP_1 → umap_1")
print("   UMAP_2 → umap_2")
print(f"📊 Current columns: {list(df.columns)}")
