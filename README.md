# Scalable Single-Cell RNA-Seq Analysis Platform

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17611614.svg)](https://doi.org/10.5281/zenodo.17611614)
[![Apache Spark](https://img.shields.io/badge/Apache-Spark-orange.svg)](https://spark.apache.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Container-Docker-blue.svg)](https://docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Docker%20Compose-brightgreen.svg)]()

> **A production-ready, containerized platform for distributed single-cell RNA sequencing analysis with Apache Spark, real-time visualization, and workflow orchestration**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Technology Stack](#technology-stack)
- [Access Points](#access-points)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Data Management](#data-management)
- [Troubleshooting](#troubleshooting)
- [API & Integration](#api--integration)
- [Performance](#performance)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## 🔬 Overview

The **Scalable Single-Cell RNA-Seq Analysis Platform** is a production-grade, containerized bioinformatics platform designed for distributed processing and interactive exploration of single-cell RNA sequencing data. Built on Apache Spark for high-performance computing and Streamlit for intuitive visualization, this platform enables researchers to analyze cellular heterogeneity at scale.

### Why This Platform?

Single-cell RNA sequencing presents unique computational challenges:
- **High dimensionality**: 20,000+ genes × thousands of cells
- **Distributed processing**: Memory-intensive operations requiring scalable solutions
- **Interactive exploration**: Real-time visualization of complex cellular data
- **Reproducible workflows**: Containerized environments with version control

This platform addresses these challenges through:
- **Apache Spark cluster** for distributed data processing
- **Streamlit web application** for interactive visualization
- **Docker Compose** for reproducible deployment
- **Real-time quality metrics** and UMAP projections

---
### Live Platform Demonstration

**Figure 1: Deployed Single-Cell Analysis Platform**

![Platform Screenshot](docs/images/platform-screenshot.png)

*Live Streamlit web application showing UMAP visualization of 5,000 cells across 8 cell types (CD4+ T-cell, CD8+ T-cell, B-cell, NK-cell, Monocyte, Dendritic, Stem Cell, Macrophage). The platform displays real-time interactive controls, quality metrics, and cluster visualization powered by Apache Spark distributed computing.*


## ✨ Key Features

### 🚀 Distributed Computing
- **Apache Spark 3.5.0 cluster** with master-worker architecture
- **Horizontal scaling** to handle 100K+ cells efficiently
- **Parallel processing** of quality metrics and transformations
- **In-memory computations** for rapid data access

### 📊 Interactive Visualization
- **Real-time UMAP projections** with 8+ cell type coloring
- **Quality control dashboards** with mitochondrial percentages and gene counts
- **Interactive filtering** and cell type exploration
- **Plotly-powered visualizations** with hover tooltips

### 🔄 Production Orchestration
- **Apache NiFi** for workflow automation and ETL pipelines
- **Docker containerization** for consistent environments
- **Multi-service coordination** with health monitoring
- **Persistent data volumes** for analysis results

### 🧬 Comprehensive Analysis
- **Cell quality metrics**: Mitochondrial percentage, gene counts, UMI distributions
- **Dimensionality reduction**: UMAP projections for cell type visualization
- **Cell type identification**: 8+ predefined cell types with custom annotation
- **Quality filtering**: Adaptive thresholds based on dataset characteristics

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Streamlit │ │ Apache Spark │ │ Apache NiFi │
│ Web App │ │ Cluster │ │ Orchestration │
│ │ │ │ │ │
│ • UMAP Viz │◄──►│ • Master:7077 │◄──►│ • Data Pipelines│
│ • Cell Type │ │ • Worker:2 cores │ │ • ETL Workflows │
│ Analysis │ │ • 2GB RAM each │ │ • Automation │
│ • QC Metrics │ │ │ │ │
└─────────────────┘ └──────────────────┘ └─────────────────┘
│ │ │
└───────────────────────────┼─────────────────────┘
│
┌─────────────────────────────┐
│ Shared Data Volume │
│ ./data/processed/ │
│ │
│ • cell_metadata.parquet │
│ • 5,000 cells, 8 types │
│ • Quality metrics │
└─────────────────────────────┘
```

### Data Flow Architecture

```
Raw Single-Cell Data
↓
[ Apache NiFi Data Ingestion ]
↓
[ Apache Spark Processing ]
├── Quality Control
├── Normalization
├── Feature Selection
└── Dimensionality Reduction
↓
Processed Parquet Files
↓
[ Streamlit Visualization ]
├── UMAP Projections
├── Cell Type Coloring
├── Quality Metrics
└── Interactive Filtering
```

### Container Architecture

```yaml
services:
  spark-master:
    image: apache/spark:3.5.0
    ports: ["7077:7077", "8081:8080"]
    networks: ["sc_network"]

  spark-worker:
    image: apache/spark:3.5.0
    depends_on: ["spark-master"]
    environment:
      - SPARK_WORKER_CORES=2
      - SPARK_WORKER_MEMORY=2g

  webapp:
    build: ./web_app
    ports: ["8501:8501"]
    environment:
      - SPARK_MASTER=spark://spark-master:7077

  nifi:
    image: apache/nifi:1.23.0
    ports: ["8080:8080"]
```

🚀 Quick Start
Prerequisites

    Docker Engine 20.10+

    Docker Compose 2.0+

    8GB RAM minimum, 16GB recommended

Deployment

```
# Clone the repository
git clone https://github.com/mtariqi/scalable-single-cell-platform
cd scalable-single-cell-platform

# Start the complete platform
./start_single_cell_platform.sh

# Verify deployment
./verify_platform.sh
```
Access Points
Service	URL	Purpose	Status
Web Application	http://localhost:8501	Interactive single-cell analysis	✅ Live
Spark Master UI	http://localhost:8081	Cluster monitoring & job tracking	✅ Live
NiFi	http://localhost:8080	Workflow orchestration	✅ Live

Sample Dataset
The platform includes a pre-loaded dataset:
```
    5,000 single cells across 8 cell types

    Complete quality metrics: UMAP coordinates, mitochondrial percentage

    Cell Types: CD4+ T-cell, CD8+ T-cell, B-cell, NK-cell, Monocyte, Dendritic, Stem Cell, Macrophage
```


🛠️ Technology Stack
Core Components
Component	Version	Purpose	Status
Apache Spark	3.5.0	Distributed data processing	✅ Running
Streamlit	1.28.0	Interactive web dashboard	✅ Running
Apache NiFi	1.23.0	Workflow orchestration	✅ Running
Docker Compose	2.0+	Container orchestration	✅ Configured
Analysis Libraries
Library	Purpose	Integration
Plotly	Interactive visualizations	Web app charts
Pandas	Data manipulation	Spark data processing
PySpark	Spark Python API	Distributed computations
NumPy	Numerical computing	Quality metrics
Container Stack
```
--------------------------------------------------------
    Base Images: Apache Spark, Apache NiFi, Python 3.9

    Network: Custom bridge network for service communication

    Volumes: Persistent data storage for processed results

    Orchestration: Docker Compose for multi-service management
-----------------------------------------------------------
```

📁 Project Structure

```
scalable-single-cell-platform/
├── 🐳 docker-compose.yml              # Multi-service container setup
├── 🚀 start_single_cell_platform.sh   # Platform deployment script
├── ✅ verify_platform.sh              # Health check and validation
├── 📊 web_app/                        # Streamlit application
│   ├── app.py                         # Main dashboard application
│   ├── download_data_simple.py        # Data generation utilities
│   └── Dockerfile                     # Container configuration
├── ⚡ pipelines/
│   └── spark_jobs/                    # Distributed data processing
│       ├── csv_data_processor.py      # CSV data ingestion
│       └── real_data_processor.py     # H5AD/LOOM processing
├── 📁 data/                           # Mounted data volume
│   └── processed/                     # Processed analysis results
│       └── cell_metadata.parquet      # Sample dataset (5,000 cells)
├── 🔧 scripts/                        # Utility scripts
│   ├── download_data_simple.py        # Data download
│   ├── create_sample_data.py          # Data generation
│   ├── fix_data_columns.py            # Data utilities
│   └── fix_all_columns.py             # Data schema management
└── 📄 Documentation/
    ├── README.md                      # This file
    └── REPORT.md                      # Technical documentation

```

⚙️ Configuration
Spark Cluster Configuration

```
# docker-compose.yml
spark-master:
  image: apache/spark:3.5.0
  ports:
    - "7077:7077"    # Spark master port
    - "8081:8080"    # Spark web UI (external:internal)
  command: >
    /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
    --host spark-master --port 7077 --webui-port 8080
  environment:
    - SPARK_LOCAL_IP=spark-master

spark-worker:
  image: apache/spark:3.5.0
  environment:
    - SPARK_WORKER_CORES=2
    - SPARK_WORKER_MEMORY=2g
    - SPARK_LOCAL_IP=spark-worker
  command: >
    /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker
    spark://spark-master:7077 --webui-port 8081
```

# Web Application Configuration

```
# Streamlit app configuration
class SingleCellDashboard:
    def __init__(self):
        self.spark_master = "spark://spark-master:7077"
        self.data_path = "/app/data/processed/cell_metadata.parquet"
        self.available_cell_types = [
            'CD4+ T-cell', 'CD8+ T-cell', 'B-cell', 'NK-cell',
            'Monocyte', 'Dendritic', 'Stem Cell', 'Macrophage'
        ]
```

# Data Schema

```
# Processed data structure
{
    'cell_id': 'str',           # Unique cell identifier
    'cell_type': 'str',         # Cell type annotation
    'sample_id': 'str',         # Sample origin
    'n_genes': 'int',           # Genes detected per cell
    'umap_1': 'float',          # UMAP first component
    'umap_2': 'float',          # UMAP second component
    'mito_percent': 'float',    # Mitochondrial percentage
    'total_counts': 'int',      # Total UMI counts
    'log_counts': 'float',      # Log-transformed counts
    'log_genes': 'float',       # Log-transformed gene counts
    'pct_counts_mito': 'float'  # Mitochondrial percentage
}
```

# 💻 Usage Examples
Basic Analysis Workflow

```
# Example: Distributed quality control with Spark
from pyspark.sql import SparkSession

def calculate_qc_metrics(spark_session, data_path):
    """Compute quality metrics using Spark distributed processing"""
    
    # Read processed data
    df = spark_session.read.parquet(data_path)
    
    # Calculate summary statistics
    summary = df.describe(['n_genes', 'total_counts', 'mito_percent'])
    
    # Compute cell type distributions
    cell_type_counts = df.groupBy('cell_type').count()
    
    return summary, cell_type_counts

# Initialize Spark session
spark = SparkSession.builder \
    .appName("SingleCellQC") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Run analysis
summary, counts = calculate_qc_metrics(spark, "/data/processed/cell_metadata.parquet")
```

# Interactive Visualization

```
# Streamlit dashboard component
def create_umap_plot(metadata_df, color_by='cell_type'):
    """Create interactive UMAP visualization"""
    
    fig = px.scatter(
        metadata_df,
        x='umap_1',
        y='umap_2',
        color=color_by,
        hover_data={
            'cell_id': True,
            'cell_type': True,
            'n_genes': ':.0f',
            'total_counts': ':.0f',
            'mito_percent': ':.1f'
        },
        title=f"Single-Cell UMAP Projection (colored by {color_by})",
        width=800,
        height=600
    )
    
    fig.update_traces(
        marker=dict(size=4, opacity=0.7, line=dict(width=0.5, color='DarkSlateGrey'))
    )
    
    return fig
```

# Data Processing Pipeline
```
# Submit custom Spark job
docker exec sc_spark_master /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 2g \
    /app/pipelines/spark_jobs/csv_data_processor.py

# Monitor job progress at http://localhost:8081
```

# 📊 Data Management
Adding Your Data

```
# Place your single-cell data in Parquet format
cp your_data.parquet data/processed/cell_metadata.parquet

# Update permissions
sudo chown -R $USER:$USER data/

# Restart web app to load new data
docker-compose restart webapp

```

# Generating Sample Data

```
# Create sample dataset with 8 cell types
python scripts/create_sample_data.py

# Verify data creation
python -c "
import pandas as pd
df = pd.read_parquet('data/processed/cell_metadata.parquet')
print(f'Cells: {len(df)}, Types: {df.cell_type.nunique()}')
print('Cell types:', df.cell_type.unique())
"
```

# Data Validation

```
# Data quality checks
def validate_single_cell_data(df):
    """Validate single-cell data structure and quality"""
    
    required_columns = ['cell_id', 'cell_type', 'umap_1', 'umap_2', 
                       'n_genes', 'total_counts', 'mito_percent']
    
    # Check required columns
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    # Check data quality
    assert df['n_genes'].min() > 0, "All cells must have genes detected"
    assert df['mito_percent'].between(0, 100).all(), "Invalid mitochondrial percentages"
    assert df['cell_type'].nunique() > 0, "Must have at least one cell type"
    
    return True
```

# 🐛 Troubleshooting
Common Issues & Solutions

Port Conflicts:

```
# Check port usage
netstat -tulpn | grep -E ':(8501|8081|8080)'

# Alternative ports
sed -i 's/8501:8501/8502:8501/g' docker-compose.yml
```

# Spark Worker Connection Issues:

```
# Check Spark master logs
docker logs sc_spark_master

# Verify worker registration
curl -s http://localhost:8081 | grep -i worker

# Restart worker
docker-compose restart spark-worker
```

# Data Loading Problems:

```
# Reset data permissions
sudo chown -R $USER:$USER data/

# Regenerate sample data
python scripts/create_sample_data.py

# Fix column names if needed
python scripts/fix_data_columns.py
python scripts/fix_all_columns.py
```
# Web App Visualization Issues:
```
# Check web app logs
docker logs sc_webapp --tail 20

# Verify data accessibility
docker exec sc_webapp python -c "
import pandas as pd
df = pd.read_parquet('/app/data/processed/cell_metadata.parquet')
print('Data loaded successfully:', df.shape)
"
```

# Logs and Monitoring
```
# View all service logs
docker-compose logs -f

# Monitor specific service
docker logs sc_spark_master --tail 10
docker logs sc_webapp --tail 10
docker logs sc_nifi --tail 10

# Resource monitoring
docker stats sc_webapp sc_spark_master sc_spark_worker sc_nifi

# Spark cluster status
curl -s http://localhost:8081/api/v1/applications | jq .
```
# 🔌 API & Integration
Spark Integration

```
# Connect to Spark cluster
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SingleCellAnalysis") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

# Submit analysis job
def analyze_single_cell_data(spark, data_path):
    df = spark.read.parquet(data_path)
    results = df.groupBy("cell_type").agg({
        "n_genes": "avg",
        "total_counts": "avg",
        "mito_percent": "avg"
    })
    return results.collect()
```
## Data Endpoints

    **Processed Data: data/processed/cell_metadata.parquet**

    **Spark Master: spark://spark-master:7077**

   ** REST API: http://localhost:8501 (Streamlit app)**

    **NiFi API: http://localhost:8080/nifi-api**

## Custom Analysis Integration
```
# Add new Spark processing job
cp new_analysis.py pipelines/spark_jobs/

# Submit to cluster
docker exec sc_spark_master /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    /app/pipelines/spark_jobs/new_analysis.py
```

# 📈 Performance
```
**Resource Requirements
Component	CPU	Memory	Storage	Network
Spark Master	1 core	1 GB	1 GB	1 Gbps
Spark Worker	2 cores	2 GB	2 GB	1 Gbps
Web App	1 core	1 GB	500 MB	1 Gbps
NiFi	1 core	1 GB	1 GB	1 Gbps
Total	5 cores	5 GB	4.5 GB	1 Gbps

Processing Performance
Dataset Size	Processing Time	Memory Usage	Spark Utilization
5,000 cells	2-3 minutes	2-3 GB	45-60%
50,000 cells	8-12 minutes	6-8 GB	75-90%
100,000+ cells	15-25 minutes	12-16 GB	85-95%
Optimization Tips**
```

## Optimization Tips
```
# Spark configuration for single-cell data
spark_conf = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.files.maxPartitionBytes": "134217728",  # 128MB
    "spark.sql.adaptive.advisoryPartitionSizeInBytes": "134217728",
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
}
```

## 🔧 Development
Adding New Features

New Visualization:

```
# Add to web_app/app.py
def create_gene_expression_plot(self, gene_name):
    """Create gene expression visualization"""
    if gene_name in self.metadata_df.columns:
        return px.scatter(self.metadata_df, x='umap_1', y='umap_2', 
                         color=gene_name, title=f"Expression: {gene_name}")
```

## Spark Processing Job:

```
# Add to pipelines/spark_jobs/
def calculate_cell_cycle_scores(spark_session, data_path):
    """Calculate cell cycle scores using Spark"""
    df = spark_session.read.parquet(data_path)
    # Add cell cycle scoring logic
    return scores_df
```

# NiFi Workflow:

    **Access http://localhost:8080

    Design data pipelines using drag-and-drop interface

    Configure processors for data ingestion and transformation**

Building Custom Images

```
# Rebuild web app with changes
docker-compose build webapp

# Update and restart
docker-compose up -d webapp

# Test changes
./verify_platform.sh
```

## Testing Framework
```
# Run data validation tests
python -m pytest tests/test_data_validation.py

# Test Spark connectivity
python tests/test_spark_connectivity.py

# Verify platform health
./verify_platform.sh
```

# 🤝 Contributing

We welcome contributions from the bioinformatics community!
Development Process

  1. **Fork the repository**

    ```
   ** git clone https://github.com/mtariqi/scalable-single-cell-platform
    cd scalable-single-cell-platform**
    ```

  2. **Create feature branch **
     ```
     **git checkout -b feature/new-analysis-method**
     ```
 3. Test your changes
    ```
    **./verify_platform.sh
    python -m pytest tests/**
```
 **4.     Submit pull request

        Include documentation updates

        Add tests for new functionality

        Verify platform still deploys correctly

Contribution Areas

    New analysis methods (Spark jobs)

    Visualization components (Streamlit apps)

    Data processing pipelines (NiFi workflows)

    Documentation improvements

    Performance optimizations

    Bug fixes and testing

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.**
```
es or substantial portions of the Software.
```
## 📞 Support
Resources

    Documentation: GitHub Wiki

    Issues: GitHub Issues

    Discussions: GitHub Discussions

Getting Help

    Check Troubleshooting Section above for common solutions

    Review Open Issues for known problems and workarounds

    Create New Issue with:

        Detailed description of the problem

        Steps to reproduce

        Platform logs and error messages

        System information

Community

    Bioinformatics Forum: BioStars

    Spark Community: Apache Spark Community

   Streamlit Community: Streamlit Forum

 
## 👤 Author
MD Tariqul Islam (Tariq)
GitHub: @mtariqi
LinkedIn: https://www.linkedin.com/in/mdtariqulscired
License: MIT
Version: 1.0.0
Last Updated: November 2025

## 📖 Citation

If you use this platform in your research, please cite:

```bibtex
@software{tariq_scalable_single_cell_2024,
  title = {Scalable Single-Cell RNA-Seq Analysis Platform},
  author = {Tariq, M.},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXX},
  url = {https://doi.org/10.5281/zenodo.XXXXXX}
}
```







































