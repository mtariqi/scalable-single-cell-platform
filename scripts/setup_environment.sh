#!/bin/bash

# Scalable Single-Cell Platform Setup Script
echo "🔬 Setting up Scalable Single-Cell Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create data directory
echo "📁 Creating data directories..."
mkdir -p data/raw data/processed data/results

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your specific configuration"
fi

# Build and start services
echo "🐳 Building and starting Docker containers..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

echo "✅ Setup complete!"
echo ""
echo "🌐 Access your services:"
echo "   - Dashboard: http://localhost:8501"
echo "   - NiFi: http://localhost:8080/nifi"
echo "   - Spark Master: http://localhost:8081"
echo ""
echo "🚀 Next steps:"
echo "   1. Load example data: docker exec -it sc_spark_master python /app/load_example_data.py"
echo "   2. Open the dashboard and start exploring!"

chmod +x scripts/setup_environment.sh
