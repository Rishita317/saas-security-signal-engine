# Quick Wins Checklist

## ✅ Quick Win #1: Add GitHub Secrets (5 minutes)

### Step 1: Navigate to Settings

1. Go to your GitHub repository
2. Click **Settings** tab (top navigation)
3. In left sidebar: **Secrets and variables** → **Actions**

### Step 2: Add Required Secret

Click **New repository secret** and add:

**OPENAI_API_KEY**

- Name: `OPENAI_API_KEY`
- Value: `sk-your-openai-api-key-here`
- Click **Add secret**
- Click **Add secret**

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab
2. Click **I understand my workflows, go ahead and enable them** (if prompted)
3. You should see "Weekly Data Refresh" workflow

### Step 4: Test Manual Trigger (Optional)

1. Click on **Weekly Data Refresh** workflow
2. Click **Run workflow** button (right side)
3. Click green **Run workflow**
4. Watch it run! (~5 minutes)

---

## ✅ Quick Win #2: Test Manual Weekly Refresh (5-10 minutes)

### Option A: Run Test Script (Easiest)

```bash
cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
./test_weekly_refresh.sh
```

### Option B: Run Directly

```bash
cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
source venv/bin/activate
python orchestration/weekly_refresh.py
```

### What This Does:

- ✅ Collects 80 job postings (HackerNews)
- ✅ Collects 450+ conversations/articles (Reddit, RSS, TLDR, Company blogs)
- ✅ Classifies with OpenAI GPT-4o-mini (not mock data)
- ✅ Generates GTM insights (hot companies)
- ✅ Exports to `data/weekly/YYYY_WXX/`

### Expected Output:

```
======================================================================
🔐 WEEKLY REFRESH - Week 2025_W48
======================================================================

📊 PHASE 1: Hiring Signal Collection
----------------------------------------------------------------------
   Collected: 80 jobs
✅ OpenAI GPT-4o-mini initialized
🤖 Classifying 80 jobs with OpenAI GPT-4o-mini...
✅ Classification complete!

💬 PHASE 2: Conversation Signal Collection
----------------------------------------------------------------------
   Total: 446 items
🤖 Classifying 446 conversations with OpenAI GPT-4o-mini...
✅ Classification complete!

🎯 PHASE 3: GTM Intelligence Generation
----------------------------------------------------------------------
📈 Top 20 companies hiring
👥 Top 20 contributors
📰 Top 15 publishers
🔥 5 hot targets (hiring AND discussed)

💾 PHASE 4: Data Export
----------------------------------------------------------------------
✅ Exported to: data/weekly/2025_W48/
```

### Verify Results:

```bash
# Check weekly folder created
ls -la data/weekly/

# View top companies
head -20 data/weekly/2025_W48/top_companies.csv

# View GTM insights
cat data/weekly/2025_W48/gtm_insights.csv

# View in dashboard
streamlit run streamlit_app.py
```

---

## 🎉 After Quick Wins Complete

You'll have:

- ✅ GitHub Actions configured for automatic weekly refresh
- ✅ Fresh data generated with real AI classification
- ✅ GTM insights identifying hot target companies
- ✅ All 6 CSV files exported
- ✅ System fully tested end-to-end

**Total time:** ~15 minutes
**Cost:** $0
**Result:** Production-ready automated system!

---

## 🚨 Troubleshooting

### Issue: Rate Limiting (429 errors)

**Solution:** System handles this gracefully. Classification continues with fallback scores.

### Issue: No GitHub Actions Tab

**Solution:** Make sure you pushed the `.github/workflows/weekly_refresh.yml` file to your repo.

### Issue: API Key 403 Error

**Solution:** Double-check the API key in GitHub Secrets matches the one in .env (without quotes or spaces). If the key has been exposed or leaked, rotate the key immediately from OpenAI's dashboard.

---

## 📋 Optional Next Steps

After quick wins, consider:

- [ ] Deploy dashboard to Streamlit Cloud
- [ ] Set up Supabase database
- [ ] Connect live Reddit API
- [ ] Add email alerts

But for the interview demo, **you're already done!** 🎉

---

**Ready to demonstrate your SaaS Security Signal Engine to Obsidian Security!**
