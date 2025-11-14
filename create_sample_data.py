# Create the sample data script I mentioned earlier
import pandas as pd
import numpy as np
import os

print("🔬 Creating Realistic Single-Cell Data")
print("=" * 50)

# Create processed directory
os.makedirs('data/processed', exist_ok=True)

# Create sample cell metadata with 8 cell types
n_cells = 5000
cell_types = ['CD4+ T-cell', 'CD8+ T-cell', 'B-cell', 'NK-cell', 
              'Monocyte', 'Dendritic', 'Stem Cell', 'Macrophage']

np.random.seed(42)
metadata = pd.DataFrame({
    'cell_id': [f'cell_{i}' for i in range(n_cells)],
    'cell_type': np.random.choice(cell_types, n_cells),
    'sample_id': np.random.choice(['sample_1', 'sample_2', 'sample_3'], n_cells),
    'n_genes': np.random.randint(1000, 2000, n_cells),
    'UMAP_1': np.random.normal(0, 1, n_cells),
    'UMAP_2': np.random.normal(0, 1, n_cells)
})

# Save as Parquet
metadata.to_parquet('data/processed/cell_metadata.parquet')
print(f"✅ Created sample data with {n_cells} cells and {len(cell_types)} cell types")
print("📊 Cell type distribution:")
print(metadata['cell_type'].value_counts())
print(f"💾 Data saved to: data/processed/cell_metadata.parquet")

