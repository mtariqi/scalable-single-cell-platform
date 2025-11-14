# Create a simplified download script that runs inside Docker
import os
import numpy as np
import pandas as pd

print("🔬 Creating Realistic Single-Cell Data")
print("=====================================")

# Create data directories
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# Create realistic single-cell data
n_cells = 8000
n_genes = 3000

print(f"Generating {n_cells} cells with {n_genes} genes...")

# Create realistic cell types with proportions
cell_types = ['CD4 T-Cell', 'CD8 T-Cell', 'B-Cell', 'Monocyte', 'NK-Cell', 'Dendritic']
proportions = [0.35, 0.25, 0.15, 0.12, 0.08, 0.05]
cell_labels = np.random.choice(cell_types, n_cells, p=proportions)

# Create realistic expression matrix
np.random.seed(42)
base_expression = np.random.gamma(shape=2, scale=1, size=(n_cells, n_genes))

# Add cell-type specific expression patterns
marker_effects = {}
for i, cell_type in enumerate(cell_types):
    # Select some marker genes for this cell type
    marker_indices = np.random.choice(n_genes, size=50, replace=False)
    marker_effects[cell_type] = marker_indices
    cell_mask = cell_labels == cell_type
    base_expression[cell_mask[:, np.newaxis], marker_indices] += np.random.gamma(3, 2, size=(cell_mask.sum(), 50))

# Convert to integers (like UMI counts)
X = np.floor(base_expression).astype(np.int32)

# Create realistic metadata
obs = pd.DataFrame({
    'cell_id': [f'Cell_{i:05d}' for i in range(n_cells)],
    'cell_type': cell_labels,
    'n_genes': np.random.randint(600, 4000, n_cells),
    'total_counts': np.random.randint(2000, 25000, n_cells),
    'mito_percent': np.random.uniform(0.02, 0.18, n_cells),
    'sample_id': np.random.choice(['Patient_A', 'Patient_B', 'Patient_C'], n_cells),
    'condition': np.random.choice(['Healthy', 'Treatment'], n_cells, p=[0.6, 0.4])
})

# Create gene metadata
var = pd.DataFrame({
    'gene_id': [f'GENE_{i:05d}' for i in range(n_genes)],
    'gene_name': [f'Gene_{i:05d}' for i in range(n_genes)],
    'highly_variable': np.random.choice([True, False], n_genes, p=[0.15, 0.85])
})

# Create realistic UMAP coordinates
umap_coords = np.random.normal(0, 1, (n_cells, 2))
cell_type_centers = {
    'CD4 T-Cell': [-2.5, 0.5],
    'CD8 T-Cell': [-1.0, -1.2],
    'B-Cell': [1.8, 0.8],
    'Monocyte': [2.2, -1.0],
    'NK-Cell': [0.0, 2.0],
    'Dendritic': [0.5, -2.2]
}

for cell_type, center in cell_type_centers.items():
    mask = obs['cell_type'] == cell_type
    if mask.sum() > 0:
        umap_coords[mask] = np.random.multivariate_normal(
            center, [[0.3, 0.1], [0.1, 0.3]], mask.sum()
        )

# Add UMAP coordinates to metadata
obs['umap_1'] = umap_coords[:, 0]
obs['umap_2'] = umap_coords[:, 1]

# Save as CSV files (simpler than H5AD for this demo)
print("Saving data files...")
obs.to_csv("data/raw/cell_metadata.csv", index=False)
var.to_csv("data/raw/gene_metadata.csv", index=False)

# Save a sample of expression data (first 1000 cells for demo)
expr_sample = pd.DataFrame(
    X[:1000], 
    index=obs['cell_id'][:1000],
    columns=var['gene_id']
)
expr_sample.to_csv("data/raw/expression_sample.csv")

print(f"✅ Created realistic single-cell data: {n_cells} cells, {n_genes} genes")
print(f"   Cell types: {', '.join(cell_types)}")
print(f"   Samples: {obs['sample_id'].unique().tolist()}")
print("   Files saved:")
print("     - data/raw/cell_metadata.csv")
print("     - data/raw/gene_metadata.csv") 
print("     - data/raw/expression_sample.csv")
print("")
print("📊 Data ready for processing with Apache Spark!")
