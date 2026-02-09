#!/bin/bash
################################################################################
# Launch Script for Best-Worst Scaling (aka MaxDiff) Tools Streamlit GUI
################################################################################

echo "=========================================="
echo "Best-Worst Scaling (aka MaxDiff) Tools - Streamlit GUI"
echo "=========================================="
echo ""
echo "Starting the web interface..."
echo ""
echo "The app will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "To stop the app, press Ctrl+C"
echo ""
echo "=========================================="
echo ""

# Run streamlit
streamlit run app.py
