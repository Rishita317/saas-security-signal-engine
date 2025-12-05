# 🚀 Deployment Guide - Streamlit Cloud

## Quick Deployment (5 Minutes)

### Step 1: Go to Streamlit Cloud
1. Visit: https://share.streamlit.io/
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit to access your GitHub account

### Step 2: Deploy Your App
1. Click **"New app"** button
2. Select your repository: `Rishita317/saas-security-signal-engine`
3. Set Main file path: `streamlit_app_v2.py`
4. Click **"Deploy!"**

### Step 3: Share the Link
After ~2-3 minutes, your app will be live at:
```
https://[your-app-name].streamlit.app
```

You can share this link with your boss/interviewers!

---

## ✅ What Happens After Deployment

### Auto-Updates
- **Every time you push to GitHub**, Streamlit Cloud auto-deploys
- Changes appear live within 2-3 minutes
- No manual redeployment needed!

### Weekly Data Refresh
- GitHub Actions runs every **Saturday at 8 AM PDT**
- New data automatically appears on your deployed app
- No action needed - it's fully automated!

---

## 🔧 Making Changes After Deployment

### Update Dashboard Code
```bash
# Make changes to streamlit_app_v2.py locally
# Test: streamlit run streamlit_app_v2.py

# Push to GitHub
git add streamlit_app_v2.py
git commit -m "Update: [describe your change]"
git push origin main

# Streamlit Cloud will auto-deploy in ~2 minutes!
```

### Update Data
Your data updates automatically via GitHub Actions every Saturday.

To manually trigger a data refresh:
```bash
# Go to GitHub Actions tab in your repo
# Click "Weekly Data Refresh"
# Click "Run workflow"
# New data will appear on deployed app automatically!
```

### Update Dependencies
```bash
# Edit requirements.txt
git add requirements.txt
git commit -m "Update: Add new dependency"
git push origin main

# Streamlit Cloud will rebuild with new dependencies
```

---

## 📊 Current Deployment Status

### Files Prepared ✅
- ✅ `requirements.txt` - Minimal dependencies for fast deployment
- ✅ `.streamlit/config.toml` - Theme and server configuration
- ✅ `packages.txt` - System packages (none needed)
- ✅ `streamlit_app_v2.py` - Your dashboard app

### Data Available ✅
- ✅ **418 companies** in `data/weekly/2025_W48/`
- ✅ **BAE Systems** (13 jobs) from recent GitHub Actions run
- ✅ LinkedIn Resources bonus feature
- ✅ 4 tabs: Company Tracker, Hiring Signals, Conversations, LinkedIn

### Automation Status ✅
- ✅ GitHub Actions workflow configured
- ✅ Cron schedule: Every Saturday 8 AM PDT
- ✅ Manual trigger available anytime
- ✅ Auto-commits new data to repo

---

## 🎯 For Your Take-Home Assignment

### What to Share with Interviewers

1. **Deployed App URL**: `https://[your-app-name].streamlit.app`
2. **GitHub Repo**: `https://github.com/Rishita317/saas-security-signal-engine`
3. **Key Features to Highlight**:
   - ✅ 418 real companies discovered
   - ✅ 10 data sources (Indeed, VCs, Security Boards, RSS, etc.)
   - ✅ Weekly automation via GitHub Actions
   - ✅ LinkedIn bonus feature (TOS-compliant)
   - ✅ Real job URLs and company data

### Pro Tips
- The deployed app shows **live data** from your GitHub repo
- Interviewers can see your **418 companies** immediately
- They can visit **real job URLs** from the hiring details
- The **GitHub Actions history** shows your automation works
- **Code quality** is visible in your repo

---

## 🔒 Security Notes

### No Secrets Exposed
- ✅ No API keys in the deployed app
- ✅ API keys stay in GitHub Secrets (never in code)
- ✅ Data collection happens in GitHub Actions (isolated)
- ✅ Dashboard only reads CSV files (no credentials needed)

### Public vs Private
Your repo is currently **public**, which is:
- ✅ **Required** for free Streamlit Cloud hosting
- ✅ **Good** for showcasing your work to employers
- ✅ **Safe** because no secrets are exposed

---

## 🆘 Troubleshooting

### Deployment Fails
1. Check Streamlit Cloud logs (click "Manage app" → "Logs")
2. Most common issue: Missing dependency in `requirements.txt`
3. Fix: Add missing package, push to GitHub

### App Shows "No Data"
1. Check if `data/weekly/` folder exists in repo
2. Verify CSV files are committed to GitHub
3. Run: `git add data/weekly/* && git commit -m "Add data" && git push`

### Auto-Deploy Not Working
1. Go to Streamlit Cloud → "Settings" → "Advanced"
2. Click "Reboot app" to force redeploy
3. Check GitHub for recent commits

---

## 📝 Next Steps

1. **Deploy Now**: Follow Step 1-3 above (5 minutes)
2. **Test Live App**: Visit your deployed URL
3. **Share with Boss**: Send the Streamlit URL
4. **Monitor**: Check GitHub Actions runs every Saturday
5. **Iterate**: Push updates anytime, they auto-deploy!

---

**Ready to deploy?** Just follow Step 1-3 above! 🚀

Questions? Check Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud
