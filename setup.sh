#!/bin/bash

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete! To start the app, run:"
echo "source venv/bin/activate"
echo "uvicorn main:app --reload"
