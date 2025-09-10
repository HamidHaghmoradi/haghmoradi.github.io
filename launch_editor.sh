#!/bin/bash

# Website Template Editor Launcher
# Quick launch script for the website editor

echo "🚀 Starting Website Template Editor..."
echo "📍 Working directory: $(pwd)"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 to use the website editor"
    exit 1
fi

# Check if the editor file exists
if [ ! -f "website_editor_simple.py" ]; then
    echo "❌ Error: website_editor_simple.py not found in current directory"
    echo "Please ensure you're running this script from the website template directory"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo "✅ Editor file found"
echo ""
echo "🎨 Launching Website Template Editor..."
echo "   • Complete visual control over your website"
echo "   • Real-time preview with live server"
echo "   • Professional version control & export"
echo ""

# Launch the editor
python3 website_editor_simple.py

echo ""
echo "👋 Website Template Editor closed"
echo "Thanks for using the editor!"
