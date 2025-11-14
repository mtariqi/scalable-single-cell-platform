import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_parquet('data/processed/cell_metadata.parquet')

print("🔬 Testing Visualization")
print("=" * 50)
print(f"Total cells: {len(df)}")
print(f"Cell types: {df['cell_type'].nunique()}")
print(f"Cell type distribution:")
print(df['cell_type'].value_counts())

# Create a test plot
fig = px.scatter(
    df, 
    x='umap_1', 
    y='umap_2', 
    color='cell_type',
    title=f"Test UMAP - {len(df)} cells, {df['cell_type'].nunique()} types",
    hover_data=['cell_id', 'sample_id']
)

print("✅ Plot created successfully!")
print("💡 If this works but the web app doesn't, there's a web app configuration issue")
fig.show()

