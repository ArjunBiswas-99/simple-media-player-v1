#!/bin/bash

echo "======================================"
echo "Simple Media Player - Installation"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo ""

# Check if MPV is installed
echo "Checking for MPV..."
if command -v mpv &> /dev/null; then
    MPV_VERSION=$(mpv --version | head -n 1)
    echo "✓ Found: $MPV_VERSION"
else
    echo "✗ MPV not found."
    echo ""
    echo "Please install MPV first:"
    echo "  macOS:   brew install mpv"
    echo "  Linux:   sudo apt install mpv libmpv-dev"
    echo "  Windows: choco install mpv"
    echo ""
    echo "After installing MPV, run this script again."
    exit 1
fi

echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo "  python3 src/main.py"
echo ""
echo "See QUICKSTART.md for usage instructions."
echo ""
