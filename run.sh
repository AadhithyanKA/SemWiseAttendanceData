#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check arguments
if [ "$1" == "app" ]; then
    echo "Starting Streamlit App..."
    streamlit run src/app.py --browser.gatherUsageStats false --server.headless true
else
    echo "Running CLI Report Generator..."
    python src/generate_reports.py "$@"
fi
