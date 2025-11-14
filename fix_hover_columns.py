# Create a fix for the column name mismatch
import pandas as pd
import os

print("🔧 Fixing column names for web app compatibility...")

# Read the existing data
df = pd.read_parquet('data/processed/cell_metadata.parquet')

# Rename n_counts to total_counts (what the web app expects)
df = df.rename(columns={'n_counts': 'total_counts'})

# Save with corrected column names
df.to_parquet('data/processed/cell_metadata.parquet')

print("✅ Fixed column names:")
print("   n_counts → total_counts")
print(f"📊 Current columns: {list(df.columns)}")

