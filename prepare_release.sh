#!/bin/bash

echo "🚀 Preparing release for Zenodo..."

# Create release directory
mkdir -p release/v1.0.0
cd release/v1.0.0

# Copy all source files (excluding large data and cache)
cp -r ../../web_app .
cp -r ../../pipelines .
cp -r ../../scripts .
cp -r ../../docs .
cp ../../*.py .
cp ../../*.sh .
cp ../../*.yml .
cp ../../*.md .
cp ../../.gitignore .

# Remove large data files if any
find . -name "*.parquet" -delete
find . -name "*.h5ad" -delete
find . -name "*.loom" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Create version file
echo "v1.0.0" > VERSION
date > BUILD_DATE

# Create checksums
find . -type f -name "*" | grep -v "./checksums" | sort | xargs sha256sum > checksums.txt

echo "✅ Release prepared in release/v1.0.0/"
echo "📦 Total size: $(du -sh . | cut -f1)"
echo "📁 File count: $(find . -type f | wc -l)"

