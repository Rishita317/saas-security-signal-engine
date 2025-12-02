#!/bin/bash
# Quick test of weekly refresh with real Gemini API

echo "========================================================================"
echo "🧪 TESTING WEEKLY REFRESH WITH REAL GEMINI API"
echo "========================================================================"
echo ""
echo "This will:"
echo "  1. Collect hiring signals (80 jobs)"
echo "  2. Collect conversation signals (450+ items)"
echo "  3. Classify with Gemini AI"
echo "  4. Generate GTM insights"
echo "  5. Export to data/weekly/YYYY_WXX/"
echo ""
echo "⏱️  Estimated time: 5-10 minutes (due to Gemini rate limits)"
echo "💰 Cost: \$0 (using free tier)"
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
