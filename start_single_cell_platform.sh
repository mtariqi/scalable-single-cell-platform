#!/bin/bash
echo "🚀 Starting Single-Cell Analysis Platform..."
docker-compose up -d
sleep 20
echo "✅ Platform ready at: http://localhost:8501"
echo "   Open this URL in your browser to start analyzing single-cell data!"

