# Architecture Overview

## System Design

The Scalable Single-Cell Platform is built on a microservices architecture using Apache technologies for workflow orchestration, distributed computing, and real-time analytics.

## Components

### 1. Apache NiFi - Workflow Orchestration
- **Purpose**: Automated data ingestion and pipeline orchestration
- **Features**: Data provenance, visual workflow management, fault tolerance
- **Port**: 8080

### 2. Apache Spark - Distributed Computation
- **Purpose**: Large-scale data processing and machine learning
- **Features**: Distributed processing, in-memory computations, MLlib
- **Ports**: 7077 (Master), 8081 (Web UI)

### 3. Apache Doris - Analytical Database
- **Purpose**: High-performance querying and real-time analytics
- **Features**: Columnar storage, vectorized execution, SQL support
- **Port**: 8030 (Web UI), 9030 (MySQL Protocol)

### 4. Streamlit Dashboard - User Interface
- **Purpose**: Interactive data exploration and visualization
- **Features**: Real-time filtering, UMAP visualization, gene expression analysis
- **Port**: 8501

## Data Flow

1. **Ingestion**: Raw sequencing data (FASTQ) → NiFi
2. **Preprocessing**: NiFi triggers preprocessing tools (Cell Ranger)
3. **Processing**: Processed data → Spark for normalization, clustering, etc.
4. **Storage**: Results → Doris for fast querying
5. **Visualization**: Users interact via Streamlit dashboard

## Scalability

- **Vertical**: Increase container resources
- **Horizontal**: Add more Spark workers, Doris nodes
- **Cloud**: Deploy on Kubernetes across multiple cloud providers

