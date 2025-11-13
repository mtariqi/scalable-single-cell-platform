#!/usr/bin/env sql
-- Single-Cell Database Schema
CREATE TABLE IF NOT EXISTS cell_metadata (
    cell_id VARCHAR(100) PRIMARY KEY,
    cell_type VARCHAR(50),
    n_genes INTEGER,
    total_counts INTEGER,
    mito_percent FLOAT,
    umap_1 FLOAT,
    umap_2 FLOAT,
    cluster_id INTEGER,
    sample_id VARCHAR(50),
    dataset_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS gene_expression (
    cell_id VARCHAR(100),
    gene_name VARCHAR(50),
    expression_value FLOAT,
    PRIMARY KEY (cell_id, gene_name)
);

CREATE TABLE IF NOT EXISTS differential_expression (
    comparison_id VARCHAR(100),
    gene_name VARCHAR(50),
    log2_fold_change FLOAT,
    p_value FLOAT,
    adjusted_p_value FLOAT,
    cluster_1 VARCHAR(50),
    cluster_2 VARCHAR(50)
);
