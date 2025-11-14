# Scalable Single-Cell Analysis Platform

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://www.docker.com/)
[![Apache](https://img.shields.io/badge/Apache-Spark%2C%20NiFi%2C%20Doris-orange)](https://www.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)](LICENSE)

A production-grade, end-to-end platform for automated and interactive analysis of single-cell RNA-seq data. Built with Apache Spark, NiFi, and Streamlit to handle datasets from thousands to millions of cells.

![Platform Architecture](docs/images/architecture.png)
*Platform architecture showing the integrated data processing pipeline*

## 🎯 Key Features

- **⚡ Distributed Processing**: Apache Spark for scalable analysis of millions of cells
- **🔍 Interactive Exploration**: Streamlit dashboard for real-time data visualization
- **🔄 Automated Workflows**: Apache NiFi for reproducible pipeline orchestration
- **📊 Production Ready**: Docker-based deployment with full containerization
- **🔬 Multi-Format Support**: 10X Genomics, H5AD, H5, and MTX file formats

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 8GB+ RAM recommended
- 50GB+ free disk space for large datasets

### Installation & Deployment

```bash
# Clone repository
git clone https://github.com/mtariqi/scalable-single-cell-platform
cd scalable-single-cell-platform

# Start the platform
./run_platform.sh

# Access the dashboard at http://localhost:8501
