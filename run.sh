#!/bin/bash

# Matrix Dynamic Visualizer Setup and Run Script

echo "Setting up Matrix Dynamic Visualizer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Starting Matrix Dynamic Visualizer..."
python transformation_visualizer.py

# Deactivate virtual environment (when the app closes)
deactivate