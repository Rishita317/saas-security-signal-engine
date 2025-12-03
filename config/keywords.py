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
    "Microsoft Security": {
        "url": "https://www.microsoft.com/security/blog",
        "rss": "https://www.microsoft.com/security/blog/feed/",
    },
    "IBM Security": {
        "url": "https://securityintelligence.com",
        "rss": "https://securityintelligence.com/feed/",
    },
    "Palo Alto Networks": {
        "url": "https://www.paloaltonetworks.com/blog",
        "rss": "https://www.paloaltonetworks.com/blog/feed/",
    },
    "CrowdStrike": {
        "url": "https://www.crowdstrike.com/blog",
        "rss": "https://www.crowdstrike.com/blog/feed/",
    },
    "Cisco Security": {
        "url": "https://blogs.cisco.com/security",
        "rss": "https://blogs.cisco.com/security/feed",
    },
    "TLDR Cybersecurity": {
        "url": "https://www.cybersecuritytldr.com",
        "rss": "https://www.cybersecuritytldr.com/feed/",
    },
    "Fortinet": {
        "url": "https://www.fortinet.com/blog",
        "rss": "https://www.fortinet.com/blog/rss.xml",
    },
    "Check Point Software": {
        "url": "https://blog.checkpoint.com",
        "rss": "https://blog.checkpoint.com/feed/",
    },
    "Okta": {
        "url": "https://www.okta.com/blog",
        "rss": "https://www.okta.com/blog/feed/",
    },
    "Broadcom Security": {
        "url": "https://www.broadcom.com/blog/security",
        "rss": "https://www.broadcom.com/blog/feed",
    },
}

# Top Cybersecurity Companies (for blog/RSS monitoring)
TOP_SECURITY_COMPANIES = {
    "CrowdStrike": {
        "url": "https://www.crowdstrike.com",
        "blog_rss": "https://www.crowdstrike.com/blog/feed/",
        "twitter": "@CrowdStrike",
    },
    "Palo Alto Networks": {
        "url": "https://www.paloaltonetworks.com",
        "blog_rss": "https://www.paloaltonetworks.com/blog/feed/",
        "twitter": "@PaloAltoNtwks",
    },
    "Okta": {
        "url": "https://www.okta.com",
        "blog_rss": "https://www.okta.com/blog/feed/",
        "twitter": "@Okta",
    },
    "Cloudflare": {
        "url": "https://www.cloudflare.com",
        "blog_rss": "https://blog.cloudflare.com/rss/",
        "twitter": "@Cloudflare",
    },
    "Microsoft Security": {
        "url": "https://www.microsoft.com/security",
        "blog_rss": "https://www.microsoft.com/en-us/security/blog/feed/",
        "twitter": "@MSSecurity",
    },
    "IBM Security": {
        "url": "https://www.ibm.com/security",
        "blog_rss": "https://securityintelligence.com/feed/",
        "twitter": "@IBMSecurity",
    },
    "Cisco Security": {
        "url": "https://www.cisco.com/c/en/us/products/security/index.html",
        "blog_rss": "https://blogs.cisco.com/security/feed",
        "twitter": "@CiscoSecurity",
    },
    "Broadcom (Symantec)": {
        "url": "https://www.broadcom.com/products/cybersecurity",
        "blog_rss": "https://symantec-enterprise-blogs.security.com/blogs/feed",
        "twitter": "@Broadcom",
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
