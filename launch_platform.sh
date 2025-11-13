#!/bin/bash

echo "🔬 Launching Single-Cell Platform"
echo "================================="

# Check if platform is running
if ! curl -s http://localhost:8501 > /dev/null; then
    echo "❌ Platform is not running. Starting services..."
    docker-compose up -d
    sleep 15
fi

echo "✅ Platform is running at http://localhost:8501"
echo ""
echo "🚀 Attempting to open in browser..."

# Try different methods to open browser
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8501
elif command -v gnome-open > /dev/null; then
    gnome-open http://localhost:8501
elif command -v kde-open > /dev/null; then
    kde-open http://localhost:8501
elif command -v open > /dev/null; then
    open http://localhost:8501
else
    echo "📝 Please manually open: http://localhost:8501"
fi

echo ""
echo "🔧 If the page appears blank or doesn't load:"
echo "   1. Wait 30 seconds for Streamlit to fully initialize"
echo "   2. Refresh the page"
echo "   3. Try a different browser"
echo "   4. Check browser console for errors (F12)"
echo ""
echo "📊 Service Status:"
docker-compose ps

chmod +x launch_platform.sh
./launch_platform.sh
