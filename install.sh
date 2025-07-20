#!/bin/bash
# Simple installation script for Financial Tools

echo "🚀 Installing Financial Tools..."
echo "================================"

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
    python3 setup.py
elif command -v python &> /dev/null; then
    echo "✅ Python found"
    python setup.py
else
    echo "❌ Error: Python 3 is required but not found"
    echo "   Please install Python 3.7 or higher"
    exit 1
fi 