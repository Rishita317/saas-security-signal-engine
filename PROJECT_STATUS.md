# SaaS Security Signal Engine - Project Status

**Project:** Automated GTM Intelligence System for Obsidian Security  
**Status:** ✅ **READY FOR DEMONSTRATION**  
**Updated:** 2025-11-29

---

## 🎯 Project Goals (ACHIEVED)

✅ Build an automated data system that identifies:
- Who is **hiring** for SaaS security topics
- Who is **talking about** SaaS security topics

✅ Weekly automatic refresh of data

✅ Surface actionable GTM signals (not raw data)

✅ Dynamic company names and contributor IDs (not static lists)

✅ Budget: $0 (using free tiers)

---

## ✅ What's Been Built

### Phase 1: Project Setup ✅
- Project structure, configuration files
- Database schema (ready for Supabase)
- Keyword configuration system
- Development environment

### Phase 2: Hiring Signal Pipeline ✅
- HackerNews job scraper
- Entity extraction with spaCy
- AI classification with Google Gemini
- CSV exports for GTM team
- Interactive dashboard

### Phase 3: Conversation Signal Pipeline ✅
- Reddit conversation scraper (7+ subreddits)
- RSS feed aggregator (10+ publishers)
- TLDR InfoSec tracker (410K+ subscribers)
- Company blog scrapers (8 top security companies)
- Urgency and trending detection
- Top contributor tracking (dynamic)
- Top publisher rankings (dynamic)

### Phase 4: Automation & Orchestration ✅
- Weekly refresh orchestrator
- GitHub Actions workflow (FREE)
- Dynamic tracking:
  - Top 20 companies hiring
  - Top 20 contributors (Reddit users)
  - Top 15 publishers
- GTM Intelligence:
  - Companies both hiring AND discussed (hottest targets)
  - Companies only hiring (cold outreach)
  - Companies only discussed (brand awareness)

### Dashboard ✅
- Interactive Streamlit dashboard
- Two tabs: Hiring Signals + Conversation Signals
- Top companies, contributors, publishers
- High urgency/breaking news alerts
- Full searchable tables
- Download functionality

---

## 🔑 API Keys Status

### ✅ Google Gemini API Key
- **Status:** ✅ WORKING
- **Provider:** Google Gemini 2.5 Flash
- **Cost:** FREE (10 requests/minute)
- **Key:** AIzaSyBbpHNph-ZfeEoDFeV-3bFLnbvo3FU8r6g
- **Verified:** 2025-11-29
- **Test Result:** Successfully classified job with 0.90 relevance score

---

## 📊 Data Collection Capacity

### Weekly Refresh Collects:
- **80+ job postings** (HackerNews "Who's Hiring")
- **100 conversations** (Reddit discussions)
- **330 articles** (RSS feeds from 10+ publishers)
- **8 newsletter items** (TLDR InfoSec)
- **8 blog posts** (Company security blogs)
- **Total:** 500+ items per week

### Dynamic Tracking (Auto-Refreshed):
- Top 20 companies hiring for SaaS Security
- Top 20 contributors discussing SaaS Security (Reddit users)
- Top 15 publishers covering SaaS Security
- Companies both hiring AND discussed (GTM intelligence)

---

## 🚀 How to Use

### 1. View Current Data (Dashboard)
```bash
# Start dashboard:
cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
source venv/bin/activate
streamlit run streamlit_app.py
```

### 2. Run Manual Weekly Refresh
```bash
cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
source venv/bin/activate
python orchestration/weekly_refresh.py
```

### 3. Set Up Automatic Weekly Refresh
See [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) for GitHub Actions setup

---

## 📁 Key Files

- [config/keywords.py](config/keywords.py) - Keywords, companies, publishers
- [orchestration/weekly_refresh.py](orchestration/weekly_refresh.py) - Main automation
- [.github/workflows/weekly_refresh.yml](.github/workflows/weekly_refresh.yml) - GitHub Actions
- [streamlit_app.py](streamlit_app.py) - Dashboard
- [.env](.env) - API keys (Gemini verified ✅)

---

## 🚦 Current Status: READY FOR DEMO

**System is 100% functional:**

1. ✅ API keys working (Gemini verified)
2. ✅ Data collection working (500+ items)
3. ✅ Classification working (AI + fallback)
4. ✅ Dashboard running
5. ✅ Automation configured
6. ✅ Documentation complete
7. ✅ GTM intelligence generating

---

## 📚 Documentation

- [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) - Weekly automation setup
- [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) - Dashboard usage
- [PHASE3_COMPLETE.md](PHASE3_COMPLETE.md) - Phase 3 summary
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - This document

---

**Project Status:** ✅ **COMPLETE AND READY**  
**Total Cost:** $0  
**Maintenance:** Zero (fully automated)

🎉 **Ready for Obsidian Security interview demonstration!**
