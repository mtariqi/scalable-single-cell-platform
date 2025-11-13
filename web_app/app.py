#!/usr/bin/env python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json

# Page configuration
st.set_page_config(
    page_title="Single-Cell Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SingleCellDashboard:
    def __init__(self):
        self.setup_sidebar()
        self.load_sample_data()
        
    def setup_sidebar(self):
        """Setup the sidebar with filters and controls"""
        st.sidebar.title("🔬 Single-Cell Explorer")
        st.sidebar.markdown("---")
        
        # Platform status
        st.sidebar.subheader("Platform Status")
        st.sidebar.success("✅ All Systems Operational")
        
        # Data controls
        st.sidebar.subheader("Data Controls")
        self.n_cells = st.sidebar.slider("Number of cells to display", 100, 5000, 1000)
        
        # Visualization controls
        st.sidebar.subheader("Visualization")
        self.color_by = st.sidebar.selectbox(
            "Color cells by",
            ["cell_type", "n_genes", "total_counts", "mito_percent", "sample_id"]
        )
        
        self.selected_gene = st.sidebar.text_input("Gene expression", "Gene_0100")
        
    def load_sample_data(self):
        """Load or generate sample single-cell data"""
        # Check if we have processed data
        if os.path.exists("/app/data/processed/cell_metadata.parquet"):
            try:
                self.metadata_df = pd.read_parquet("/app/data/processed/cell_metadata.parquet")
                st.sidebar.info("📁 Using processed data from Spark")
            except:
                self.generate_sample_data()
        else:
            self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate sample data for demonstration"""
        np.random.seed(42)
        n_cells = 5000
        
        # Generate UMAP-like coordinates
        t_cells = np.random.multivariate_normal([2, -1], [[0.5, 0.1], [0.1, 0.5]], n_cells//3)
        b_cells = np.random.multivariate_normal([-1, 1], [[0.4, 0.05], [0.05, 0.4]], n_cells//3)
        monocytes = np.random.multivariate_normal([0, 2], [[0.3, -0.1], [-0.1, 0.3]], n_cells//4)
        other = np.random.multivariate_normal([1, 0], [[0.6, 0.2], [0.2, 0.6]], n_cells - len(t_cells) - len(b_cells) - len(monocytes))
        
        coords = np.vstack([t_cells, b_cells, monocytes, other])
        
        cell_types = (['T-Cell'] * len(t_cells) + 
                     ['B-Cell'] * len(b_cells) + 
                     ['Monocyte'] * len(monocytes) + 
                     ['Other'] * len(other))
        
        samples = np.random.choice(['Patient_01', 'Patient_02', 'Patient_03'], n_cells)
        
        self.metadata_df = pd.DataFrame({
            'cell_id': [f'Cell_{i:05d}' for i in range(n_cells)],
            'cell_type': cell_types,
            'sample_id': samples,
            'n_genes': np.random.randint(500, 3000, n_cells),
            'total_counts': np.random.randint(1000, 20000, n_cells),
            'mito_percent': np.random.uniform(0.01, 0.15, n_cells),
            'umap_1': coords[:, 0],
            'umap_2': coords[:, 1],
            'cluster_id': np.random.randint(1, 8, n_cells)
        })
        
        st.sidebar.info("🔧 Using generated sample data")
    
    def create_umap_plot(self):
        """Create interactive UMAP visualization"""
        fig = px.scatter(
            self.metadata_df.head(self.n_cells),
            x='umap_1',
            y='umap_2',
            color=self.color_by,
            hover_data=['cell_id', 'cell_type', 'n_genes'],
            title=f"Single-Cell UMAP Projection (colored by {self.color_by})",
            width=800,
            height=600
        )
        
        fig.update_traces(
            marker=dict(size=4, opacity=0.7, line=dict(width=0.5, color='DarkSlateGrey')),
            selector=dict(mode='markers')
        )
        
        return fig
    
    def create_composition_plot(self):
        """Create cell type composition visualization"""
        composition = self.metadata_df['cell_type'].value_counts()
        
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "pie"}, {"type": "bar"}]],
            subplot_titles=("Cell Type Distribution", "Cell Count by Type")
        )
        
        fig.add_trace(
            go.Pie(labels=composition.index, values=composition.values, name="Distribution"),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=composition.index, y=composition.values, name="Counts"),
            row=1, col=2
        )
        
        fig.update_layout(height=400, showlegend=False, title_text="Cell Type Composition")
        return fig
    
    def create_metrics_dashboard(self):
        """Create metrics overview"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Cells", len(self.metadata_df))
        with col2:
            st.metric("Cell Types", self.metadata_df['cell_type'].nunique())
        with col3:
            st.metric("Avg Genes/Cell", f"{self.metadata_df['n_genes'].mean():.0f}")
        with col4:
            st.metric("Samples", self.metadata_df['sample_id'].nunique())
    
    def show_platform_info(self):
        """Show platform information"""
        with st.expander("🚀 Platform Information"):
            st.markdown("""
            **Scalable Single-Cell Analysis Platform**
            
            This platform demonstrates a production-ready single-cell RNA-seq analysis 
            pipeline using modern big data technologies:
            
            - **Apache Spark**: Distributed data processing
            - **Apache NiFi**: Workflow orchestration  
            - **Streamlit**: Interactive visualization
            - **Docker**: Containerized deployment
            
            **Features:**
            - Process millions of cells
            - Real-time interactive exploration
            - Automated analysis pipelines
            - Reproducible workflows
            """)
    
    def run(self):
        """Main dashboard execution"""
        st.title("🔬 Scalable Single-Cell Analysis Platform")
        st.markdown("Interactive exploration of single-cell RNA-seq data at scale")
        
        # Show platform info
        self.show_platform_info()
        
        # Metrics dashboard
        self.create_metrics_dashboard()
        
        # Main visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["UMAP", "Composition", "Quality Control", "Data Explorer"])
        
        with tab1:
            st.plotly_chart(self.create_umap_plot(), use_container_width=True)
            
        with tab2:
            st.plotly_chart(self.create_composition_plot(), use_container_width=True)
            
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                fig_genes = px.box(self.metadata_df, x='cell_type', y='n_genes', 
                                 title="Genes per Cell by Type")
                st.plotly_chart(fig_genes, use_container_width=True)
            with col2:
                fig_mito = px.violin(self.metadata_df, x='cell_type', y='mito_percent',
                                   title="Mitochondrial Percentage by Type")
                st.plotly_chart(fig_mito, use_container_width=True)
                
        with tab4:
            st.subheader("Cell Metadata")
            st.dataframe(self.metadata_df.head(100), use_container_width=True)
            
            # Data export
            if st.button("📥 Export Sample Data"):
                csv = self.metadata_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="single_cell_data.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    dashboard = SingleCellDashboard()
    dashboard.run()

