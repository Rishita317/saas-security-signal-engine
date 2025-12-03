#!/bin/bash

# Test Full Pipeline with OpenAI
# This script tests the complete weekly refresh pipeline

echo "========================================================================"
echo "🧪 Testing Complete Pipeline with OpenAI"
echo "========================================================================"
echo ""

# Step 1: Test OpenAI API
echo "📝 Step 1: Testing OpenAI API connection..."
python test_openai_setup.py
if [ $? -ne 0 ]; then
    echo "❌ OpenAI API test failed. Fix API key before continuing."
    exit 1
fi
echo ""

# Step 2: Test Job Classification
echo "📝 Step 2: Testing job classification with OpenAI..."
python processors/classification_gemini.py
if [ $? -ne 0 ]; then
    echo "⚠️  Job classification test had issues (continuing...)"
fi
echo ""

# Step 3: Run Weekly Refresh (this is the full pipeline)
echo "📝 Step 3: Running weekly refresh (FULL PIPELINE)..."
echo "   This will collect 1,000+ jobs and classify them with OpenAI"
echo ""
python orchestration/weekly_refresh.py
if [ $? -ne 0 ]; then
    echo "❌ Weekly refresh failed"
    exit 1
fi
echo ""

echo "========================================================================"
echo "✅ FULL PIPELINE TEST COMPLETE!"
echo "========================================================================"
echo ""
echo "📊 Check the results:"
echo "   - data/weekly/ folder for CSV exports"
echo "   - Look for hiring_signals and conversation_signals files"
echo ""
