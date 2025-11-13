#!/bin/bash

echo "🔬 Starting Scalable Single-Cell Platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose down

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/raw data/processed data/results

# Build the webapp first
echo "🐳 Building web application..."
docker-compose build webapp

# Start all services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to initialize
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check status
echo "🔍 Checking service status..."
docker-compose ps

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=20

echo ""
echo "✅ If all services are running, access the platform at:"
echo "   🌐 Dashboard: http://localhost:8501"
echo ""
echo "🔧 If you encounter issues, check logs with: docker-compose logs [service]"

chmod +x start_platform.sh
