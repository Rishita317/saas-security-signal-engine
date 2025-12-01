# Weekly Automation Setup Guide

This guide explains how to set up **automatic weekly data refresh** for the SaaS Security Signal Engine.

---

## 🔄 Automation Options

### Option 1: GitHub Actions (Recommended - FREE)

**Pros:**
- Completely free for public repos
- Automatically commits new data to repo
- Runs every Monday at 8 AM UTC
- Can trigger manually anytime
- No infrastructure needed

**Setup Steps:**

1. **Push Code to GitHub**
   ```bash
   cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
   git add .
   git commit -m "Add weekly automation"
   git push origin main
   ```

2. **Add GitHub Secrets**

   Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret

   Add these secrets:
   - `GOOGLE_API_KEY` = `AIzaSyBbpHNph-ZfeEoDFeV-3bFLnbvo3FU8r6g`
   - `OPENAI_API_KEY` = (optional - your OpenAI key if you have one)
   - `REDDIT_CLIENT_ID` = (your Reddit client ID when you get one)
   - `REDDIT_CLIENT_SECRET` = (your Reddit secret when you get one)

3. **Enable Actions**

   Go to Actions tab → Enable GitHub Actions if not already enabled

4. **Manual Trigger Test**

   Go to Actions → Weekly Data Refresh → Run workflow

   This will trigger the weekly refresh immediately to test it works.

5. **Automatic Schedule**

   The workflow will now run automatically **every Monday at 8 AM UTC** (midnight PST)

---

### Option 2: Cron Job (Local/Server)

**Pros:**
- Runs on your local machine or server
- No GitHub dependency
- Good for private data

**Setup:**

1. **Create cron script**
   ```bash
   # Edit crontab
   crontab -e

   # Add this line (runs every Monday at 8 AM)
   0 8 * * 1 cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\) && source venv/bin/activate && python orchestration/weekly_refresh.py >> logs/cron.log 2>&1
   ```

2. **Create logs directory**
   ```bash
   mkdir -p logs
   ```

3. **Test manually**
   ```bash
   cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
   source venv/bin/activate
   python orchestration/weekly_refresh.py
   ```

---

### Option 3: Modal Cron (Cloud - Paid)

**Pros:**
- Serverless, no infrastructure
- Scales automatically
- Pay-per-use

**Cost:** ~$0.10-$1/month

**Setup:**

1. **Install Modal**
   ```bash
   pip install modal
   modal token new
   ```

2. **Create Modal script** (see `orchestration/modal_cron.py` - to be created)

3. **Deploy**
   ```bash
   modal deploy orchestration/modal_cron.py
   ```

---

## 📊 What Happens During Weekly Refresh

The automation runs `orchestration/weekly_refresh.py` which:

1. **Collects Hiring Signals**
   - Scrapes HackerNews "Who's Hiring" (80+ jobs)
   - Extracts companies, job titles, locations
   - Classifies relevance with Gemini AI
   - Identifies top 20 companies hiring

2. **Collects Conversation Signals**
   - Scrapes Reddit discussions (50+ conversations)
   - Aggregates RSS articles (220+ articles)
   - Fetches TLDR InfoSec newsletter
   - Classifies urgency and trending potential
   - Identifies top 20 contributors (Reddit users)
   - Identifies top 15 publishers

3. **Generates GTM Insights**
   - Companies hiring AND discussed (hottest targets)
   - Companies only hiring (cold outreach)
   - Companies only discussed (brand awareness)

4. **Exports Data**
   - Creates weekly folder: `data/weekly/2025_W47/`
   - Exports 6 CSV files:
     - `hiring_signals.csv` - All job postings
     - `top_companies.csv` - Top 20 hiring
     - `conversation_signals.csv` - All conversations
     - `top_contributors.csv` - Top 20 Reddit users
     - `top_publishers.csv` - Top 15 publishers
     - `gtm_insights.csv` - Hot companies

5. **Updates Dashboard**
   - Dashboard automatically loads latest data
   - No manual refresh needed

---

## 🧪 Testing the Automation

### Manual Test (Recommended First)

```bash
cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
source venv/bin/activate
python orchestration/weekly_refresh.py
```

**Expected Output:**
```
======================================================================
🔐 SAAS SECURITY SIGNAL ENGINE - WEEKLY REFRESH
======================================================================
Week ID: 2025_W48
Timestamp: 2025-11-29_153045

📥 PHASE 1: Hiring Signal Collection
----------------------------------------------------------------------
✅ Reddit: 80 job postings
🤖 Classifying 80 jobs with Google Gemini...
✅ Classification complete!
🔍 Filtered: 72/80 jobs above 0.7 relevance score

💬 PHASE 2: Conversation Signal Collection
----------------------------------------------------------------------
✅ Reddit: 50 conversations
✅ RSS: 220 articles
✅ TLDR InfoSec: 8 articles
📊 Total collected: 278 items
🤖 Classifying 278 conversations with Google Gemini...

🎯 PHASE 3: GTM Intelligence Generation
----------------------------------------------------------------------
📈 Top 20 companies hiring for SaaS Security roles
👥 Top 20 contributors discussing SaaS Security
📰 Top 15 publishers covering SaaS Security
🔥 Companies both hiring AND discussed: 5 hot targets

💾 PHASE 4: Data Export
----------------------------------------------------------------------
💾 Exported to: data/weekly/2025_W48/
   Files created: 6 CSVs

✅ WEEKLY REFRESH COMPLETE!
```

### Verify Data

```bash
# Check the weekly folder was created
ls -la data/weekly/2025_W48/

# View top companies
head -20 data/weekly/2025_W48/top_companies.csv

# View GTM insights
cat data/weekly/2025_W48/gtm_insights.csv
```

---

## 🚨 Troubleshooting

### Issue 1: Rate Limiting

**Error:** `429 Too Many Requests` from Gemini API

**Solution:**
- Free tier: 10 requests/minute
- The script handles this automatically
- Adds delays between batches
- For large datasets, upgrade to paid tier ($0.001/request)

### Issue 2: No Data Collected

**Error:** `0 job postings found`

**Solution:**
- Check if it's the first Monday of the month (HackerNews posts monthly)
- System uses mock data as fallback
- Real scraping requires API keys (Reddit)

### Issue 3: API Key Issues

**Error:** `403 Your API key was reported as leaked`

**Solution:**
- Generate new key at https://aistudio.google.com/apikey
- Update `.env` file with new key
- Or update GitHub Secret `GOOGLE_API_KEY`

### Issue 4: GitHub Actions Not Running

**Solution:**
- Check Actions tab → Enable workflows
- Verify secrets are set correctly
- Try manual trigger first: Actions → Run workflow

---

## 📈 Monitoring

### Check Last Run

**GitHub Actions:**
- Go to Actions tab
- Click on "Weekly Data Refresh"
- View latest run logs

**Local Cron:**
```bash
tail -f logs/cron.log
```

### View Weekly Data History

```bash
# List all weeks
ls -la data/weekly/

# Compare week-over-week
python -c "
import pandas as pd
df1 = pd.read_csv('data/weekly/2025_W47/top_companies.csv')
df2 = pd.read_csv('data/weekly/2025_W48/top_companies.csv')
print('New companies this week:')
print(set(df2['company']) - set(df1['company']))
"
```

---

## 🎯 Next Steps

After automation is set up:

1. **Verify First Run**
   - Wait for Monday or trigger manually
   - Check data/weekly/ folder for new data
   - View dashboard to confirm data loads

2. **Set Up Alerts** (Optional)
   - Email digest of hot companies
   - Slack notification for breaking breaches
   - Weekly summary report

3. **Add More Data Sources**
   - Twitter/X via Apify
   - LinkedIn company posts
   - Company blogs (Okta, Cloudflare, etc.)

4. **Database Integration**
   - Store in Supabase for historical tracking
   - Query trends over time
   - Build advanced analytics

5. **Deploy Dashboard**
   - Push to Streamlit Cloud (free)
   - Share with GTM team
   - Enable automatic updates

---

## 📋 Summary

**Recommended Setup (GitHub Actions):**

1. Push code to GitHub ✅
2. Add API key secrets (5 min)
3. Enable Actions (1 click)
4. Test manual trigger (5 min)
5. Done! Runs automatically every Monday

**Total Setup Time:** ~15 minutes

**Cost:** $0 (using free tiers)

**Maintenance:** Zero - fully automated

---

## 📚 Related Files

- [orchestration/weekly_refresh.py](orchestration/weekly_refresh.py) - Main automation script
- [.github/workflows/weekly_refresh.yml](.github/workflows/weekly_refresh.yml) - GitHub Actions config
- [PHASE3_COMPLETE.md](PHASE3_COMPLETE.md) - Phase 3 completion summary
- [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) - Dashboard usage guide

---

**Project:** SaaS Security Signal Engine for Obsidian Security
**Automation Status:** ✅ Ready to Deploy
**Next Action:** Push to GitHub and add secrets
