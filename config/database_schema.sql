-- SaaS Security Signal Engine Database Schema
-- To be run in Supabase SQL Editor

-- Table 1: Hiring Signals
CREATE TABLE IF NOT EXISTS hiring_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    company_name_normalized TEXT, -- lowercase, trimmed for deduplication
    job_title TEXT NOT NULL,
    job_category TEXT NOT NULL, -- SSPM, SaaS Security, AI Agent Security, etc.
    source_platform TEXT NOT NULL, -- HackerNews, Reddit, GitHub
    source_url TEXT,
    posted_date TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT NOW(),
    relevance_score FLOAT, -- 0.0 to 1.0 from GPT-4 Mini
    is_active BOOLEAN DEFAULT TRUE,
    week_id TEXT NOT NULL, -- Format: "2025-W48"
    raw_text TEXT, -- original job post text for debugging
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table 2: Conversation Signals
CREATE TABLE IF NOT EXISTS conversation_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform TEXT NOT NULL, -- Reddit, Twitter, Publisher
    author_username TEXT,
    author_url TEXT,
    post_title TEXT,
    post_content TEXT,
    topic_category TEXT NOT NULL, -- SaaS Security, Salesforce Breach, etc.
    mentioned_companies JSONB, -- array of extracted company names
    engagement_score INT DEFAULT 0, -- upvotes, likes, retweets
    post_url TEXT,
    posted_date TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT NOW(),
    week_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table 3: Publisher Rankings
CREATE TABLE IF NOT EXISTS publisher_rankings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    publisher_name TEXT NOT NULL,
    publisher_url TEXT,
    platform TEXT DEFAULT 'RSS',
    relevance_score FLOAT,
    weekly_post_count INT DEFAULT 0,
    total_engagement INT DEFAULT 0,
    week_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table 4: Weekly Summary Stats
CREATE TABLE IF NOT EXISTS weekly_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    week_id TEXT NOT NULL UNIQUE,
    total_hiring_signals INT DEFAULT 0,
    total_companies INT DEFAULT 0,
    total_conversation_signals INT DEFAULT 0,
    top_category TEXT,
    trending_topic TEXT,
    run_timestamp TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_hiring_signals_week ON hiring_signals(week_id);
CREATE INDEX IF NOT EXISTS idx_hiring_signals_company ON hiring_signals(company_name_normalized);
CREATE INDEX IF NOT EXISTS idx_hiring_signals_category ON hiring_signals(job_category);
CREATE INDEX IF NOT EXISTS idx_hiring_signals_active ON hiring_signals(is_active);

CREATE INDEX IF NOT EXISTS idx_conversation_signals_week ON conversation_signals(week_id);
CREATE INDEX IF NOT EXISTS idx_conversation_signals_platform ON conversation_signals(platform);
CREATE INDEX IF NOT EXISTS idx_conversation_signals_topic ON conversation_signals(topic_category);

CREATE INDEX IF NOT EXISTS idx_publisher_rankings_week ON publisher_rankings(week_id);

-- Function to normalize company names
CREATE OR REPLACE FUNCTION normalize_company_name(name TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN LOWER(TRIM(REGEXP_REPLACE(name, '\s+', ' ', 'g')));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Trigger to auto-normalize company names
CREATE OR REPLACE FUNCTION set_normalized_company_name()
RETURNS TRIGGER AS $$
BEGIN
    NEW.company_name_normalized := normalize_company_name(NEW.company_name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER normalize_company_trigger
    BEFORE INSERT OR UPDATE ON hiring_signals
    FOR EACH ROW
    EXECUTE FUNCTION set_normalized_company_name();

-- View: Top 1000 Companies (by hiring activity)
CREATE OR REPLACE VIEW top_1000_companies AS
SELECT
    company_name,
    COUNT(DISTINCT job_category) as category_count,
    COUNT(*) as total_roles,
    MAX(posted_date) as last_posted,
    AVG(relevance_score) as avg_relevance,
    ARRAY_AGG(DISTINCT job_category) as categories,
    week_id
FROM hiring_signals
WHERE is_active = TRUE
GROUP BY company_name, week_id
ORDER BY total_roles DESC, last_posted DESC
LIMIT 1000;

-- View: Top Contributors (by engagement)
CREATE OR REPLACE VIEW top_contributors AS
SELECT
    author_username,
    platform,
    COUNT(*) as post_count,
    SUM(engagement_score) as total_engagement,
    ARRAY_AGG(DISTINCT topic_category) as topics_covered,
    week_id
FROM conversation_signals
WHERE author_username IS NOT NULL
GROUP BY author_username, platform, week_id
ORDER BY total_engagement DESC, post_count DESC
LIMIT 100;

-- View: Trending Topics
CREATE OR REPLACE VIEW trending_topics AS
SELECT
    topic_category,
    COUNT(*) as mention_count,
    SUM(engagement_score) as total_engagement,
    week_id
FROM conversation_signals
GROUP BY topic_category, week_id
ORDER BY total_engagement DESC, mention_count DESC;
