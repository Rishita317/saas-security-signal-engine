"""
Configuration file for SaaS Security Signal Engine
Defines keywords, topics, and publishers for data collection
"""

# Hiring Signal Keywords - organized by category
HIRING_KEYWORDS = {
    "SaaS Security": [
        "saas security",
        "cloud app security",
        "cloud application security",
        "sanctioned it",
        "shadow it",
        "saas risk",
    ],
    "SSPM": [
        "sspm",
        "saas security posture",
        "saas posture management",
        "security posture management",
    ],
    "AI Agent Security": [
        "ai agent security",
        "ai security",
        "llm security",
        "autonomous agent security",
        "ai agent risk",
        "genai security",
    ],
    "SaaS Compliance": [
        "saas compliance",
        "cloud compliance",
        "saas governance",
        "cloud governance",
        "saas audit",
    ],
    "AI Compliance": [
        "ai compliance",
        "ai governance",
        "llm compliance",
        "generative ai compliance",
        "ai policy",
    ],
}

# Conversation Topics for monitoring discussions
CONVERSATION_TOPICS = {
    "SaaS Security": [
        "saas security",
        "sspm",
        "cloud app security",
        "saas posture",
        "obsidian security",
    ],
    "SaaS Compliance": [
        "saas compliance",
        "cloud governance",
        "saas audit",
    ],
    "AI Agent Security": [
        "ai agent security",
        "autonomous agent risk",
        "llm security",
        "ai security",
    ],
    "Salesforce Breach": [
        "salesforce breach",
        "salesforce hack",
        "salesforce compromised",
        "salesforce security",
    ],
    "Gainsight Breach": [
        "gainsight breach",
        "gainsight hack",
        "gainsight compromised",
    ],
    "Salesloft Breach": [
        "salesloft breach",
        "salesloft hack",
        "salesloft compromised",
    ],
}

# Top 10 Cybersecurity Publishers (with RSS feed URLs)
TOP_PUBLISHERS = {
    "Dark Reading": {
        "url": "https://www.darkreading.com",
        "rss": "https://www.darkreading.com/rss.xml",
    },
    "BleepingComputer": {
        "url": "https://www.bleepingcomputer.com",
        "rss": "https://www.bleepingcomputer.com/feed/",
    },
    "The Hacker News": {
        "url": "https://thehackernews.com",
        "rss": "https://feeds.feedburner.com/TheHackersNews",
    },
    "SecurityWeek": {
        "url": "https://www.securityweek.com",
        "rss": "https://www.securityweek.com/feed/",
    },
    "Threatpost": {
        "url": "https://threatpost.com",
        "rss": "https://threatpost.com/feed/",
    },
    "Krebs on Security": {
        "url": "https://krebsonsecurity.com",
        "rss": "https://krebsonsecurity.com/feed/",
    },
    "CSO Online": {
        "url": "https://www.csoonline.com",
        "rss": "https://www.csoonline.com/feed/",
    },
    "Cyber Security Hub": {
        "url": "https://www.cshub.com",
        "rss": "https://www.cshub.com/rss/",
    },
    "Security Boulevard": {
        "url": "https://securityboulevard.com",
        "rss": "https://securityboulevard.com/feed/",
    },
    "InfoSecurity Magazine": {
        "url": "https://www.infosecurity-magazine.com",
        "rss": "https://www.infosecurity-magazine.com/rss/news/",
    },
    "TLDR InfoSec": {
        "url": "https://tldr.tech/infosec",
        "rss": None,  # No public RSS - requires web scraping
        "subscribers": "410,000+",
    },
}

# Reddit subreddits to monitor
TARGET_SUBREDDITS = [
    "netsec",
    "cybersecurity",
    "AskNetsec",
    "InformationSecurity",
    "SaaS",
    "CloudSecurity",
    "cybersecurity_help",
]

# Job title patterns to extract
JOB_TITLE_PATTERNS = [
    r"(?i)(security\s+engineer)",
    r"(?i)(security\s+analyst)",
    r"(?i)(compliance\s+engineer)",
    r"(?i)(security\s+architect)",
    r"(?i)(cloud\s+security)",
    r"(?i)(application\s+security)",
    r"(?i)(infosec)",
    r"(?i)(governance.*risk.*compliance)",
    r"(?i)(grc\s+)",
]

# Minimum relevance score threshold (0.0 to 1.0)
MIN_RELEVANCE_SCORE = 0.6

# Data retention period (weeks)
DATA_RETENTION_WEEKS = 4
