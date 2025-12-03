# OpenAI Setup Checklist

## ✅ Configuration Status

### 1. Local Setup (`.env` file)
**Status:** ✅ CONFIGURED
```
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
```

### 2. GitHub Secrets
**Status:** ⚠️ NEEDS UPDATE

You need to update your GitHub Secret:

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`
2. Find the secret named: `OPENAI_API_KEY`
   - If it exists: Click "Update"
   - If it doesn't exist: Click "New repository secret"
3. **Name box:** `OPENAI_API_KEY` (exactly this, no quotes)
4. **Secret box:** `[Your OpenAI API key from .env file]`
5. Click "Add secret" or "Update secret"

### 3. Code Configuration
**Status:** ✅ ALREADY CONFIGURED

The code is already set up to use OpenAI:
- ✅ `processors/classification_gemini.py` - Uses OpenAI GPT-4o-mini by default
- ✅ `.github/workflows/weekly_refresh.yml` - Reads `OPENAI_API_KEY` from secrets
- ✅ `orchestration/weekly_refresh.py` - Uses JobClassifier (which uses OpenAI)

---

## 🧪 How to Test

### Option 1: Quick API Test (2 minutes)
Test just the OpenAI API connection:

```bash
python test_openai_setup.py
```

**Expected output:**
```
🧪 Testing OpenAI API Setup
✅ API Key found: sk-proj-lQaWmOQfT_Bo...5EIA
✅ OpenAI API Response: API working
   Model: gpt-4o-mini
   Tokens used: 15
✅ OpenAI API Setup VERIFIED!
```

### Option 2: Full Pipeline Test (5-10 minutes)
Test the complete system (1,000+ jobs with OpenAI classification):

```bash
./test_full_pipeline.sh
```

**This will:**
1. Test OpenAI API connection
2. Test job classification with OpenAI
3. Run complete weekly refresh (collect 1,000+ jobs)
4. Classify all jobs with OpenAI GPT-4o-mini
5. Export to CSV files

**Expected output location:**
- `data/weekly/YYYY_WXX/` - folder with all results
- `hiring_signals_*.csv` - 1,000+ classified jobs
- `conversation_signals_*.csv` - discussion signals

### Option 3: Test on GitHub Actions
After updating GitHub Secrets, manually trigger the workflow:

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
2. Click "Weekly Data Refresh" workflow
3. Click "Run workflow" button
4. Watch it run (takes 5-10 minutes)

---

## 📊 What Changed from Gemini to OpenAI

| Aspect | Gemini (Old) | OpenAI (New) |
|--------|--------------|--------------|
| **Model** | gemini-1.5-flash | gpt-4o-mini |
| **Free Tier** | 1,500 requests/day | Paid (requires credits) |
| **API Key Format** | `AIza...` | `sk-proj-...` |
| **Environment Variable** | `GOOGLE_API_KEY` | `OPENAI_API_KEY` |
| **Code Changes** | ❌ None needed | ✅ Already configured |
| **Quota Handling** | Automatic fallback | Automatic fallback |

---

## ⚡ Quick Reference

### Where is OpenAI API Key Used?

1. **Local testing:** `.env` file → `OPENAI_API_KEY`
2. **GitHub Actions:** GitHub Secrets → `OPENAI_API_KEY`
3. **Code reads from:** `os.getenv("OPENAI_API_KEY")`

### What Uses the API Key?

- `processors/classification_gemini.py` - Job classification (0.8-1.0 relevance scoring)
- `processors/conversation_classification.py` - Conversation signal classification
- `orchestration/weekly_refresh.py` - Orchestrator (calls the classifiers)

### Cost Estimation (OpenAI GPT-4o-mini)

**For 1,000 jobs/week:**
- Input: ~150 tokens/job × 1,000 jobs = 150,000 tokens
- Output: ~50 tokens/job × 1,000 jobs = 50,000 tokens
- **Cost:** ~$0.02-0.03 per 1,000 jobs
- **Monthly:** ~$0.08-0.12 (4 weeks)

**Very affordable!** OpenAI GPT-4o-mini is extremely cheap.

---

## 🔒 Security Note

**⚠️ IMPORTANT:** Your OpenAI API key is visible in this document and in `.env`.

**What to do:**
1. ✅ `.env` is in `.gitignore` - safe for local use
2. ⚠️ This document (`OPENAI_SETUP_CHECKLIST.md`) will be committed to git
3. 🔄 Consider regenerating your API key after testing if this gets pushed to public repo

**Best practice:**
- Never commit API keys to git
- Use GitHub Secrets for automation
- Regenerate keys if accidentally exposed

---

## ✅ Final Checklist

Before running on GitHub Actions:

- [x] OpenAI API key added to `.env` file
- [ ] OpenAI API key added to GitHub Secrets (Name: `OPENAI_API_KEY`)
- [ ] Tested locally with `python test_openai_setup.py`
- [ ] (Optional) Tested full pipeline with `./test_full_pipeline.sh`
- [ ] Ready to trigger GitHub Actions workflow

Once all boxes are checked, you're ready to run automated weekly refreshes! 🚀
