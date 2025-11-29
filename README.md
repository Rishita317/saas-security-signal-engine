# SaaS Security Signal Engine

A lightweight, automated GTM intelligence system that identifies **hiring signals** (companies actively hiring) and **conversation signals** (people/publishers discussing SaaS security topics), refreshing weekly to surface actionable insights for sales, marketing, and GTM teams.

## Problem Statement

For SaaS security companies like Obsidian Security, identifying who is actively hiring for or talking about SaaS security topics is critical for GTM strategy. This system automates the collection and analysis of these signals from multiple sources.

## What This System Does

### 1. Hiring Signals
Tracks the **Top 1,000 companies** hiring for roles related to:
- SaaS Security
- SSPM (SaaS Security Posture Management)
- AI Agent Security
- SaaS Compliance
- AI Compliance

### 2. Conversation Signals
Identifies people, accounts, and publishers discussing:
- SaaS Security / SSPM
- SaaS Compliance
- AI Agent Security
- Recent breaches (Salesforce, Gainsight, Salesloft)

Across platforms:
- Reddit (r/netsec, r/cybersecurity, etc.)
- Top 10 cybersecurity publishers
- Twitter/X (via Apify)

## Tech Stack

- **Data Collection**: Scrapy, PRAW (Reddit API), RSS parsers
- **NLP & Classification**: spaCy (entity extraction), GPT-4 Mini (relevance scoring)
- **Database**: Supabase (PostgreSQL)
- **Orchestration**: Modal (serverless Python)
- **Dashboard**: Streamlit
- **Hosting**: Streamlit Cloud (free)

## Project Structure

```
saas-security-signal-engine/
├── scrapers/
│   ├── hackernews_hiring.py      # HackerNews "Who's Hiring" threads
│   ├── reddit_hiring.py          # Reddit job posts
│   ├── reddit_conversations.py   # Reddit discussions
│   ├── publisher_rss.py          # Top 10 publisher RSS feeds
│   └── twitter_apify.py          # Twitter/X via Apify
├── processors/
│   ├── entity_extraction.py      # spaCy NER for companies/titles
│   ├── classification.py         # GPT-4 Mini relevance scoring
│   └── deduplication.py          # Remove duplicate signals
├── analytics/
│   ├── top_companies.py          # Generate Top 1000 list
│   ├── top_contributors.py       # Rank people/publishers
│   └── insights.py               # Weekly trends & metrics
├── config/
│   ├── keywords.py               # Target keywords & topics
│   └── database_schema.sql       # Supabase schema
├── modal_app.py                  # Weekly scheduled job
├── streamlit_app.py              # Dashboard
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- Git

### 2. Clone & Install
```bash
git clone <your-repo-url>
cd Sass_Security_Engine(SSE)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 3. Set Up API Keys
Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required API keys:
- **OpenAI API Key** (for GPT-4 Mini classification)
- **Supabase URL & Key** (create free account at supabase.com)
- **Reddit API credentials** (register app at reddit.com/prefs/apps)

Optional:
- **Apify API Token** (for Twitter scraping)
- **Perplexity API Key** (for enrichment)

### 4. Set Up Supabase Database

1. Create a free Supabase account: https://supabase.com
2. Create a new project
3. Go to SQL Editor
4. Copy/paste the contents of `config/database_schema.sql`
5. Run the SQL to create tables and indexes
6. Copy your project URL and anon key to `.env`

### 5. Test Individual Scrapers (Coming Soon)
```bash
# Test HackerNews scraper
python scrapers/hackernews_hiring.py

# Test Reddit scraper
python scrapers/reddit_hiring.py
```

### 6. Run Weekly Job Locally (Coming Soon)
```bash
python modal_app.py
```

### 7. View Dashboard (Coming Soon)
```bash
streamlit run streamlit_app.py
```

## Data Sources

### Hiring Signals
- **HackerNews**: Monthly "Who's Hiring" threads (free API)
- **Reddit**: Job posts from r/netsec, r/cybersecurity, etc. (free PRAW API)
- **GitHub Jobs**: Scraped job boards (free)

### Conversation Signals
- **Reddit**: Discussions from security subreddits (free PRAW API)
- **Top 10 Publishers**: RSS feeds from Dark Reading, BleepingComputer, The Hacker News, etc.
- **Twitter/X**: Tweets via Apify (2k free credits/month = ~500 tweets)

## Weekly Refresh Mechanism

- **Orchestration**: Modal serverless Python (cron schedule: every Monday 9 AM)
- **Data Retention**: 4 weeks of historical data
- **Deduplication**: Fuzzy matching on company names + URL deduplication
- **Weekly ID Format**: "2025-W48" (ISO week format)

## Key Metrics & Insights

### Hiring Signals
- Top 1,000 companies ranked by:
  - Number of active job postings
  - Category diversity (SSPM + AI Security = higher score)
  - Recency (posted this week = 2x weight)
  - Relevance score from GPT-4 Mini

### Conversation Signals
- Top contributors by engagement (upvotes + comment count)
- Top publishers by SaaS security coverage
- Trending topics (which breach is most discussed?)
- Week-over-week growth in hiring activity

## Cost Estimate

- **OpenAI GPT-4 Mini**: ~$1-2/month (processing 100-200 posts/week)
- **Supabase**: Free tier (500MB database)
- **Modal**: Free tier (generous CPU credits)
- **Reddit API**: Free
- **Streamlit Cloud**: Free hosting
- **Apify**: Free tier (2k credits/month)

**Total: $1-2/month**

## Known Limitations

1. **No LinkedIn data**: LinkedIn API requires paid enterprise access and aggressively blocks scrapers
2. **Twitter rate limits**: Apify free tier limited to ~500 tweets/week
3. **Company name normalization**: Not 100% accurate (e.g., "Google" vs "Google Inc.")
4. **Publisher list is subjective**: "Top 10" defined based on industry reputation, not algorithmic
5. **Weekly refresh only**: Not real-time (by design for cost efficiency)

## Development Status

**Current Phase**: Phase 1 - Project Setup ✅
- [x] Git repository initialized
- [x] Python environment set up
- [x] Dependencies installed
- [x] Configuration files created
- [x] Database schema designed

**Next Steps**:
- [ ] Phase 2: Build hiring signal scrapers
- [ ] Phase 3: Build conversation signal scrapers
- [ ] Phase 4: Orchestration & automation
- [ ] Phase 5: Analytics layer
- [ ] Phase 6: Streamlit dashboard
- [ ] Phase 7: Deployment & documentation

## Contributing

This is a demo project for Obsidian Security's AI GTM Engineer role. Not accepting external contributions at this time.

## License

Private project - All rights reserved
