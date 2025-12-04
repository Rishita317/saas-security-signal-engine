# Cleanup Summary - December 4, 2025

## ✅ Archived 61 Outdated Files

All outdated/unused files have been safely moved to `_archive/20251204_151003/`

---

## 📂 Current Active Project Structure

### **Core Application Files:**
- `streamlit_app_v2.py` - **Active Dashboard** (4 tabs: Company Tracker, Hiring Signals, Conversation Signals, LinkedIn Resources)
- `linkedin_resources.py` - LinkedIn bonus feature (isolated, TOS-compliant)

### **Active Scrapers:**
- `scrapers/company_discovery_v3.py` - **V3 Discovery Engine** (25+ VCs, 10 data sources)
- `scrapers/multi_source_jobs.py` - Multi-source job board scraper
- `scrapers/rss_publishers.py` - RSS feed scraper for blog posts

### **Orchestration:**
- `orchestration/weekly_refresh.py` - **GitHub Actions automation** (runs every Monday)

### **Documentation:**
- `README.md` - Main project documentation
- `SETUP_GUIDE.md` - Setup instructions
- `DASHBOARD_GUIDE.md` - Dashboard usage guide
- `AUTOMATION_SETUP.md` - GitHub Actions setup

---

## 🗑️ What Was Archived

### **Old Versions (Replaced):**
- `streamlit_app.py` → replaced by `streamlit_app_v2.py`
- `scrapers/company_discovery.py` → replaced by `scrapers/company_discovery_v3.py`
- `orchestration/weekly_refresh_v2.py` → replaced by using V3 directly

### **Unused Scrapers (Never Integrated):**
- `scrapers/hackernews_hiring.py`
- `scrapers/reddit_conversations.py`
- `scrapers/tldr_infosec.py`
- `scrapers/multi_ats_scraper.py` (logic moved to V3)

### **Test Scripts (One-Time Use):**
- `run_indeed_expanded.py` - Test script for expanded keywords
- `run_internships_only.py` - Test script for internships
- `run_v3_with_existing_data.py` - One-time migration script

### **14 Test Files:**
All `test_*.py` files moved to archive

### **13 Documentation Files:**
Old status reports, phase summaries, and setup checklists

### **17 Log Files:**
Old scraping logs and output files

### **5 JSON Test Outputs:**
Test data from development phase

---

## 🔄 How to Restore Files

If you need any archived file back:

```bash
# View archived files
ls -R _archive/20251204_151003/

# Restore a specific file (example)
cp _archive/20251204_151003/test_v3_discovery.py .

# Restore all files (if needed)
cp -r _archive/20251204_151003/* .
```

---

## 🗑️ Permanently Delete Archive

Once you're confident you don't need the archived files:

```bash
rm -rf _archive/
```

**Note:** This will permanently delete all 61 archived files. Only do this when you're 100% sure!

---

## 📊 Current System Status

- **Total Companies:** 418
- **Active Dashboard:** localhost:8501
- **Data Sources:** 10 (Indeed, VC Portfolios, Security Job Boards, Greenhouse, Lever, Workday, RSS Feeds, etc.)
- **Weekly Automation:** Enabled (GitHub Actions, every Monday 8 AM UTC)
- **LinkedIn Integration:** Bonus feature available (optional, TOS-compliant)

---

## ✨ Benefits of Cleanup

1. **Cleaner Repository** - Easier to navigate and understand
2. **Reduced Confusion** - No duplicate versions of files
3. **Faster Searches** - Less noise when searching for code
4. **Clear Structure** - Obvious which files are active
5. **Safe Archiving** - All files preserved in `_archive/` if needed

---

*Generated: 2025-12-04 15:10:03*
