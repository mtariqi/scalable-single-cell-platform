#!/bin/bash

echo "🔬 Starting Scalable Single-Cell Platform"
echo "========================================="

# Clean up
docker-compose down

# Build and start
echo "🐳 Building and starting services..."
docker-compose up -d --build

echo "⏳ Waiting for services to initialize..."
sleep 25

# Run Spark processing job
echo "⚡ Running single-cell analysis pipeline..."
docker exec sc_spark_master python /app/scRNA_processor.py

echo ""
echo "✅ PLATFORM READY!"
echo "=================="
echo ""
echo "🌐 Access Points:"
echo "   🔬 Dashboard: http://localhost:8501"
echo "   ⚡ Spark UI:  http://localhost:8081"
echo ""
echo "📊 Platform Status:"
docker-compose ps
echo ""
echo "🚀 To stop the platform: docker-compose down"

chmod +x run_platform.sh

# Run the complete platform
./run_platform.sh
