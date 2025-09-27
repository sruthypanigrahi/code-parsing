#!/bin/bash
# Quick demo script for USB PD Parser

echo "🚀 USB PD Parser Demo"
echo "====================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch .venv/installed
fi

# Run extraction on sample PDF (mode 3 for quick demo)
echo "Running extraction (mode 3 - first 200 pages)..."
python main.py --mode 3

# Show results
echo ""
echo "📊 Results:"
echo "==========="
if [ -f "outputs/usb_pd_content.jsonl" ]; then
    echo "✅ Content extracted successfully!"
    echo "First 3 content items:"
    head -n 3 outputs/usb_pd_content.jsonl
    echo ""
    echo "📈 Statistics:"
    echo "Content items: $(wc -l < outputs/usb_pd_content.jsonl)"
    if [ -f "outputs/usb_pd_toc.jsonl" ]; then
        echo "TOC entries: $(wc -l < outputs/usb_pd_toc.jsonl)"
    fi
else
    echo "❌ No output files found. Check for errors above."
fi

echo ""
echo "🔍 Try searching content:"
echo "python search_content.py \"USB\""
echo "python search_content.py \"Power Delivery\""