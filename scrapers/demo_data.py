"""
Demo/Mock data for testing the pipeline without live scraping

This allows you to test the full pipeline (entity extraction, classification, database storage)
without depending on live APIs during development.
"""

from datetime import datetime, timedelta
import random


def get_mock_hackernews_jobs() -> list:
    """Generate realistic mock HackerNews job posts for SaaS security"""

    companies = [
        "Wiz", "Obsidian Security", "Normalyze", "Nudge Security", "Valence Security",
        "AppOmni", "Grip Security", "Adaptive Shield", "DoControl", "Spin.AI",
        "CrowdStrike", "Palo Alto Networks", "Okta", "Zscaler", "Netskope",
        "Lacework", "Sysdig", "Snyk", "Aqua Security", "Prisma Cloud"
    ]

    roles = [
        "Security Engineer - SSPM",
        "Senior SaaS Security Engineer",
        "Staff Security Engineer (Cloud Security)",
        "Security Architect - SaaS Applications",
        "Principal Engineer - AI Security",
        "Security Engineer - Compliance Automation",
        "Senior Security Engineer - SSPM Platform",
        "Cloud Security Engineer",
        "Application Security Engineer - SaaS",
        "Senior Security Compliance Engineer"
    ]

    locations = ["Remote", "San Francisco, CA", "New York, NY", "Tel Aviv, Israel",
                 "London, UK", "Austin, TX", "Seattle, WA", "Boston, MA"]

    job_categories = [
        "SSPM",
        "SaaS Security",
        "AI Agent Security",
        "SaaS Compliance",
        "AI Compliance"
    ]

    keywords_map = {
        "SSPM": ["sspm", "saas security posture", "saas posture management"],
        "SaaS Security": ["saas security", "cloud app security", "sanctioned it"],
        "AI Agent Security": ["ai security", "llm security", "ai agent security"],
        "SaaS Compliance": ["saas compliance", "cloud governance"],
        "AI Compliance": ["ai compliance", "ai governance"]
    }

    mock_jobs = []
    base_date = datetime.now()

    for i in range(50):  # Generate 50 mock jobs
        company = random.choice(companies)
        role = random.choice(roles)
        location = random.choice(locations)
        category = random.choice(job_categories)
        days_ago = random.randint(0, 30)
        posted_date = base_date - timedelta(days=days_ago)

        job = {
            "source_platform": "HackerNews",
            "source_url": f"https://news.ycombinator.com/item?id={40000000 + i}",
            "company_name": company,
            "job_title": role,
            "location": location,
            "job_category": category,
            "posted_date": posted_date,
            "raw_text": f"{company} is hiring a {role} in {location}. We're looking for someone with experience in {', '.join(keywords_map[category][:2])}.",
            "matched_keywords": keywords_map[category][:2],
        }
        mock_jobs.append(job)

    return mock_jobs


def get_mock_reddit_jobs() -> list:
    """Generate realistic mock Reddit job posts"""

    companies = [
        "Cisco", "Microsoft", "Google Cloud", "AWS", "Salesforce",
        "ServiceNow", "Workday", "Box", "Dropbox", "Atlassian",
        "Zoom", "Slack", "Notion", "Airtable", "Monday.com"
    ]

    subreddits = ["netsec", "cybersecurity", "InformationSecurity"]

    mock_jobs = []
    base_date = datetime.now()

    for i in range(30):  # Generate 30 mock Reddit jobs
        company = random.choice(companies)
        subreddit = random.choice(subreddits)
        days_ago = random.randint(0, 21)
        posted_date = base_date - timedelta(days=days_ago)

        category = random.choice(["SaaS Security", "SaaS Compliance", "SSPM"])

        job = {
            "source_platform": "Reddit",
            "source_url": f"https://reddit.com/r/{subreddit}/comments/abc{i}",
            "company_name": company,
            "job_title": f"Security Engineer - {category}",
            "location": random.choice(["Remote", "US", "Global"]),
            "job_category": category,
            "posted_date": posted_date,
            "raw_text": f"[Hiring] {company} is looking for a Security Engineer focused on {category.lower()}",
            "matched_keywords": [category.lower(), "security"],
        }
        mock_jobs.append(job)

    return mock_jobs


def get_mock_reddit_conversations() -> list:
    """Generate mock Reddit conversation signals"""

    topics = [
        ("Salesforce Breach", ["salesforce breach", "salesforce hack", "salesforce security"]),
        ("SaaS Security", ["saas security", "sspm", "cloud app security"]),
        ("AI Agent Security", ["ai security", "llm security", "ai agents"]),
    ]

    subreddits = ["netsec", "cybersecurity", "sysadmin"]
    usernames = ["security_pro_42", "cloud_defender", "saas_expert", "infosec_guru",
                 "compliance_lead", "security_analyst_99", "pentester_pro"]

    mock_conversations = []
    base_date = datetime.now()

    for i in range(100):  # Generate 100 mock conversations
        topic, keywords = random.choice(topics)
        subreddit = random.choice(subreddits)
        username = random.choice(usernames)
        days_ago = random.randint(0, 7)
        posted_date = base_date - timedelta(days=days_ago)
        engagement = random.randint(5, 500)

        conversation = {
            "platform": "Reddit",
            "author_username": username,
            "author_url": f"https://reddit.com/user/{username}",
            "post_title": f"Discussion about {topic}",
            "post_content": f"Has anyone been following the recent developments with {keywords[0]}? I think this is a major concern for enterprises...",
            "topic_category": topic,
            "mentioned_companies": random.sample(["Salesforce", "Okta", "Microsoft", "Google"], k=random.randint(1, 3)),
            "engagement_score": engagement,
            "post_url": f"https://reddit.com/r/{subreddit}/comments/xyz{i}",
            "posted_date": posted_date,
        }
        mock_conversations.append(conversation)

    return mock_conversations


if __name__ == "__main__":
    print("📦 Generating mock data...\n")

    hn_jobs = get_mock_hackernews_jobs()
    reddit_jobs = get_mock_reddit_jobs()
    conversations = get_mock_reddit_conversations()

    print(f"✅ Generated {len(hn_jobs)} HackerNews jobs")
    print(f"✅ Generated {len(reddit_jobs)} Reddit jobs")
    print(f"✅ Generated {len(conversations)} Reddit conversations")

    print("\n📊 Sample HackerNews Job:")
    print(hn_jobs[0])

    print("\n📊 Sample Reddit Conversation:")
    print(conversations[0])
