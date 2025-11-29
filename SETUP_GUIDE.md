# Setup Guide: SaaS Security Signal Engine

## Step-by-Step Setup Instructions

### Step 1: Supabase Database Setup (5 minutes)

#### 1.1 Create Supabase Account
1. Go to https://supabase.com
2. Click "Start your project" (it's free!)
3. Sign up with GitHub or email

#### 1.2 Create a New Project
1. Click "New Project"
2. Choose:
   - **Organization**: Your account name
   - **Name**: `saas-security-signals` (or any name you prefer)
   - **Database Password**: Generate a strong password (save this!)
   - **Region**: Choose closest to you
   - **Pricing Plan**: Free tier is perfect
3. Click "Create new project"
4. Wait ~2 minutes for database to provision

#### 1.3 Get Your API Credentials
1. In your Supabase project dashboard, click "Project Settings" (gear icon in sidebar)
2. Go to "API" section
3. Copy these two values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon/public key** (under "Project API keys")

#### 1.4 Run Database Schema
1. In Supabase dashboard, click "SQL Editor" in sidebar
2. Click "New Query"
3. Open `config/database_schema.sql` from this project
4. Copy the entire contents
5. Paste into the SQL Editor
6. Click "Run" (or press Cmd/Ctrl + Enter)
7. You should see: "Success. No rows returned"
8. Go to "Table Editor" in sidebar - you should now see 4 tables:
   - `hiring_signals`
   - `conversation_signals`
   - `publisher_rankings`
   - `weekly_stats`

### Step 2: API Keys Setup (10 minutes)

#### 2.1 Create .env File
```bash
cp .env.example .env
```

Now edit the `.env` file:

#### 2.2 Add Supabase Credentials
```bash
SUPABASE_URL=https://xxxxx.supabase.co  # From Step 1.3
SUPABASE_KEY=your-anon-key-here          # From Step 1.3
```

#### 2.3 Get OpenAI API Key (Required)
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Name it: "SaaS Security Signals"
5. Copy the key (starts with `sk-...`)
6. Add to `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```

**Cost**: GPT-4 Mini is ~$0.15 per 1M tokens. For this project: **$1-2/month**

#### 2.4 Get Reddit API Credentials (Required)
1. Go to https://www.reddit.com/prefs/apps
2. Log in to Reddit
3. Scroll down, click "create another app"
4. Fill in:
   - **name**: SaaS Security Signal Engine
   - **type**: Select "script"
   - **description**: (optional)
   - **about url**: (leave blank)
   - **redirect uri**: http://localhost:8080
5. Click "create app"
6. Copy these values:
   - **client_id**: Under "personal use script" (14 characters)
   - **client_secret**: Next to "secret" (27 characters)
7. Add to `.env`:
```bash
REDDIT_CLIENT_ID=your-14-char-id
REDDIT_CLIENT_SECRET=your-27-char-secret
REDDIT_USER_AGENT=SaaS-Security-Signal-Engine/1.0
```

**Cost**: Free!

#### 2.5 Get Apify API Token (Optional - for Twitter)
1. Go to https://console.apify.com/sign-up
2. Sign up (free tier: 2k credits/month)
3. Go to Settings > Integrations
4. Copy your API token
5. Add to `.env`:
```bash
APIFY_API_TOKEN=your-token-here
```

**Cost**: Free tier (500 tweets/week)

### Step 3: Test Your Setup

#### 3.1 Test Database Connection
```bash
source venv/bin/activate
python config/database.py
```

You should see:
```
✅ Successfully connected to Supabase!
   Current week ID: 2025-W48
```

If you see an error:
- Check your `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Make sure you ran the database schema SQL

#### 3.2 Test Dependencies
```bash
python -c "import scrapy, spacy, openai, supabase, praw; print('✅ All dependencies installed!')"
```

### Step 4: Next Steps

Phase 1 is complete! You now have:
- ✅ Project structure set up
- ✅ Database created and schema loaded
- ✅ API keys configured
- ✅ Dependencies installed

**Ready to build the scrapers?**

Next up: Phase 2 - Build Hiring Signal Scrapers
- HackerNews "Who's Hiring" scraper
- Reddit job post scraper
- Entity extraction with spaCy
- Relevance classification with GPT-4 Mini

### Troubleshooting

#### "ValueError: Missing Supabase credentials"
- Make sure you created `.env` file (copy from `.env.example`)
- Check that `SUPABASE_URL` and `SUPABASE_KEY` are set
- Make sure you're in the project directory

#### "No module named 'scrapy'"
- Activate virtual environment: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

#### "Can't find spaCy model en_core_web_sm"
- Run: `python -m spacy download en_core_web_sm`

#### Supabase SQL errors
- Make sure you're using the SQL Editor (not Table Editor)
- Copy the ENTIRE `database_schema.sql` file
- If tables already exist, you can drop them first (be careful!):
  ```sql
  DROP TABLE IF EXISTS hiring_signals CASCADE;
  DROP TABLE IF EXISTS conversation_signals CASCADE;
  DROP TABLE IF EXISTS publisher_rankings CASCADE;
  DROP TABLE IF EXISTS weekly_stats CASCADE;
  ```

### Budget Summary

| Service | Cost | Required? |
|---------|------|-----------|
| OpenAI GPT-4 Mini | $1-2/month | ✅ Yes |
| Supabase | Free | ✅ Yes |
| Reddit API | Free | ✅ Yes |
| Apify (Twitter) | Free | ⚠️ Optional |
| Modal | Free | ⚠️ Later |
| Streamlit Cloud | Free | ⚠️ Later |
| **Total** | **$1-2/month** | |

### Questions?

If you get stuck, check:
1. All API keys are correctly copied to `.env`
2. Virtual environment is activated
3. You ran the database schema SQL
4. All dependencies installed successfully

Ready to continue? Let me know and we'll build the first scraper!
