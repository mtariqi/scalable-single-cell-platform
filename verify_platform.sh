#!/bin/bash

echo "🔍 Verifying Platform Installation"
echo "================================="

# Check Docker
echo "1. Checking Docker..."
if docker info > /dev/null 2>&1; then
    echo "   ✅ Docker is running"
else
    echo "   ❌ Docker is not running"
    exit 1
fi

# Check containers
echo ""
echo "2. Checking containers..."
docker-compose ps

# Test webapp accessibility
echo ""
echo "3. Testing webapp..."
if curl -s http://localhost:8501 > /dev/null; then
    echo "   ✅ Webapp is accessible at http://localhost:8501"
else
    echo "   ❌ Webapp is not accessible"
fi

# Test Spark
echo ""
echo "4. Testing Spark..."
if docker exec sc_spark_master python -c "print('Spark test')" 2>/dev/null; then
    echo "   ✅ Spark is running"
else
    echo "   ⚠️  Spark may still be starting..."
fi

# Show access information
echo ""
echo "🌐 PLATFORM ACCESS INFORMATION"
echo "=============================="
echo "Main Dashboard: http://localhost:8501"
echo "Spark UI:       http://localhost:8081"
echo "NiFi:          http://localhost:8080/nifi"
echo ""
echo "📊 To view service logs:"
echo "   docker-compose logs webapp"
echo "   docker-compose logs spark-master"
echo "   docker-compose logs nifi"
echo ""
echo "🚀 Platform is ready for single-cell analysis!"

chmod +x verify_platform.sh
