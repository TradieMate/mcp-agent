#!/bin/bash

# Start script for local development
# Make sure you have OPENAI_API_KEY set in your environment

echo "Starting MCP Agent Streamlit App..."
echo "Make sure you have set OPENAI_API_KEY environment variable"

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start the Streamlit app
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=false