#!/bin/bash
# Quick test of weekly refresh with OpenAI

echo "========================================================================"
echo "🧪 TESTING WEEKLY REFRESH WITH OpenAI GPT-4o-mini API"
echo "========================================================================"
echo ""
echo "This will:"
echo "  1. Collect hiring signals (80 jobs)"
echo "  2. Collect conversation signals (450+ items)"
echo "  3. Classify with OpenAI GPT-4o-mini"
echo "  4. Generate GTM insights"
echo "  5. Export to data/weekly/YYYY_WXX/"
echo ""
echo "⏱️  Estimated time: 5-10 minutes (due to API rate limits)"
echo "💰 Cost: Varies by OpenAI plan and model usage"
echo ""
echo "Starting in 3 seconds..."
sleep 3

cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
source venv/bin/activate
python orchestration/weekly_refresh.py

echo ""
echo "========================================================================"
echo "✅ WEEKLY REFRESH COMPLETE!"
echo "========================================================================"
echo ""
echo "📁 Check your data at:"
ls -la data/weekly/
echo ""
echo "📊 View in dashboard:"
echo "   streamlit run streamlit_app.py"
echo ""
