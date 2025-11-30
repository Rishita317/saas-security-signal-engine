"""
TLDR InfoSec Newsletter Scraper

Scrapes TLDR InfoSec newsletter (410,000+ subscribers) for:
- Latest cybersecurity news
- Security research
- Security tools and resources

Since TLDR doesn't provide a public RSS feed, this uses web scraping
or mock data for demonstration.
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.keywords import CONVERSATION_TOPICS


class TLDRInfoSecScraper:
    """Scrape TLDR InfoSec newsletter for security content"""

    def __init__(self, use_mock: bool = True):
        """
        Initialize TLDR scraper

        Args:
            use_mock: If True, use mock data (recommended - no official API)
        """
        self.use_mock = use_mock
        self.base_url = "https://tldr.tech/infosec"

    def fetch_latest_newsletter(self) -> Dict:
        """
        Fetch the latest TLDR InfoSec newsletter

        Returns:
            Newsletter dictionary with articles
        """
        if self.use_mock:
            return self._get_mock_newsletter()

        try:
            print("🔍 Fetching TLDR InfoSec newsletter...")

            # Note: TLDR doesn't provide official API/RSS
            # This would require web scraping or email parsing
            # For production, consider:
            # 1. Email forwarding to parse newsletters
            # 2. Official TLDR API (if they provide one)
            # 3. Partnership/subscription access

            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract newsletter content (structure may vary)
            articles = self._parse_newsletter_html(soup)

            return {
                "source": "TLDR InfoSec",
                "date": datetime.now(),
                "articles": articles,
            }

        except Exception as e:
            print(f"⚠️  Error fetching TLDR newsletter: {e}")
            print("   Using mock data instead")
            return self._get_mock_newsletter()

    def _parse_newsletter_html(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse TLDR newsletter HTML structure"""
        articles = []

        # Note: This is a placeholder structure
        # Actual TLDR HTML structure would need to be analyzed
        # and updated based on their current format

        # Look for article containers
        article_sections = soup.find_all("article") or soup.find_all("div", class_="article")

        for section in article_sections:
            try:
                title_elem = section.find("h2") or section.find("h3")
                summary_elem = section.find("p")
                link_elem = section.find("a")

                if title_elem:
                    article = {
                        "platform": "tldr_infosec",
                        "publisher": "TLDR InfoSec",
                        "title": title_elem.get_text(strip=True),
                        "summary": summary_elem.get_text(strip=True) if summary_elem else "",
                        "url": link_elem.get("href", "") if link_elem else "",
                        "published_at": datetime.now(),
                        "matched_keywords": [],
                        "category": "Unknown",
                    }

                    # Extract matched keywords
                    text = f"{article['title']} {article['summary']}".lower()
                    article["matched_keywords"] = self._extract_matched_keywords(text)
                    article["category"] = self._determine_category(text)

                    if article["matched_keywords"]:
                        articles.append(article)

            except Exception as e:
                print(f"   ⚠️  Error parsing article section: {e}")

        return articles

    def _extract_matched_keywords(self, text: str) -> List[str]:
        """Extract matched keywords from text"""
        matched = []

        for category, keywords in CONVERSATION_TOPICS.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    matched.append(keyword)

        return list(set(matched))  # Remove duplicates

    def _determine_category(self, text: str) -> str:
        """Determine category based on keywords"""
        category_scores = {}

        for category, keywords in CONVERSATION_TOPICS.items():
            score = sum(1 for kw in keywords if kw.lower() in text)
            if score > 0:
                category_scores[category] = score

        if category_scores:
            return max(category_scores, key=category_scores.get)

        return "General Security"

    def _get_mock_newsletter(self) -> Dict:
        """Generate mock TLDR InfoSec newsletter"""
        return {
            "source": "TLDR InfoSec",
            "date": datetime.now(),
            "subscriber_count": "410,000+",
            "articles": [
                {
                    "platform": "tldr_infosec",
                    "publisher": "TLDR InfoSec",
                    "section": "News 📰",
                    "title": "New SSPM Platform Raises $50M to Secure SaaS Applications",
                    "summary": "A startup focused on SaaS Security Posture Management announced a $50M Series B to help enterprises detect and fix misconfigurations across cloud apps like Salesforce, Microsoft 365, and Slack.",
                    "url": "https://techcrunch.com/sspm-funding",
                    "published_at": datetime.now(),
                    "matched_keywords": ["sspm", "saas security", "cloud app security"],
                    "category": "SSPM",
                },
                {
                    "platform": "tldr_infosec",
                    "publisher": "TLDR InfoSec",
                    "section": "Research 🧑‍🔬",
                    "title": "Researchers Discover Security Flaws in AI Agent Frameworks",
                    "summary": "Security researchers found critical vulnerabilities in popular AI agent frameworks that could allow attackers to manipulate autonomous agents and access sensitive corporate data across SaaS platforms.",
                    "url": "https://arxiv.org/ai-agent-security",
                    "published_at": datetime.now(),
                    "matched_keywords": ["ai agent security", "autonomous agent risk", "saas security"],
                    "category": "AI Agent Security",
                },
                {
                    "platform": "tldr_infosec",
                    "publisher": "TLDR InfoSec",
                    "section": "News 📰",
                    "title": "Salesforce Patches Critical Vulnerability in Customer Portal",
                    "summary": "Salesforce released an emergency security update after discovering a vulnerability that could expose customer data. The flaw affected millions of Salesforce instances worldwide.",
                    "url": "https://salesforce.com/security-advisory",
                    "published_at": datetime.now() - timedelta(days=1),
                    "matched_keywords": ["salesforce security", "saas security"],
                    "category": "Salesforce Breach",
                },
                {
                    "platform": "tldr_infosec",
                    "publisher": "TLDR InfoSec",
                    "section": "Tools 🔒",
                    "title": "Open-Source Tool for SaaS Compliance Auditing Released",
                    "summary": "A new open-source tool helps security teams audit SaaS applications for compliance with SOC 2, ISO 27001, and GDPR. The tool integrates with major cloud providers and SaaS platforms.",
                    "url": "https://github.com/saas-compliance-tool",
                    "published_at": datetime.now(),
                    "matched_keywords": ["saas compliance", "cloud governance", "saas audit"],
                    "category": "SaaS Compliance",
                },
                {
                    "platform": "tldr_infosec",
                    "publisher": "TLDR InfoSec",
                    "section": "News 📰",
                    "title": "Enterprise SaaS Security Spending Expected to Double by 2025",
                    "summary": "Market research shows enterprise spending on SaaS security tools like SSPM and CASB will double in the next two years as organizations struggle with shadow IT and compliance.",
                    "url": "https://gartner.com/saas-security-market",
                    "published_at": datetime.now(),
                    "matched_keywords": ["saas security", "sspm", "cloud security"],
                    "category": "SaaS Security",
                },
                {
                    "platform": "tldr_infosec",
                    "publisher": "TLDR InfoSec",
                    "section": "Research 🧑‍🔬",
                    "title": "Study Reveals 87% of Organizations Have Misconfigured SaaS Apps",
                    "summary": "A comprehensive study of 500 enterprises found that 87% have at least one critical misconfiguration in their SaaS applications, with Salesforce, Microsoft 365, and Slack being the most commonly misconfigured.",
                    "url": "https://research.com/saas-misconfigurations",
                    "published_at": datetime.now() - timedelta(days=2),
                    "matched_keywords": ["saas security", "cloud security", "saas posture"],
                    "category": "SaaS Security",
                },
                {
                    "platform": "tldr_infosec",
                    "publisher": "TLDR InfoSec",
                    "section": "News 📰",
                    "title": "Gainsight Announces Enhanced Security Features for Customer Success Platform",
                    "summary": "Following recent security concerns, Gainsight rolled out new security features including advanced access controls, audit logging, and integration with SSPM tools.",
                    "url": "https://gainsight.com/security-update",
                    "published_at": datetime.now() - timedelta(days=1),
                    "matched_keywords": ["gainsight", "saas security"],
                    "category": "SaaS Security",
                },
                {
                    "platform": "tldr_infosec",
                    "publisher": "TLDR InfoSec",
                    "section": "Tools 🔒",
                    "title": "New AI-Powered SSPM Tool Automates Security Remediation",
                    "summary": "A new AI-powered SSPM platform can automatically detect and fix security issues across SaaS applications, reducing remediation time from days to minutes.",
                    "url": "https://techcrunch.com/ai-sspm",
                    "published_at": datetime.now(),
                    "matched_keywords": ["sspm", "ai security", "saas security"],
                    "category": "SSPM",
                },
            ],
        }

    def get_stats(self, newsletter: Dict) -> Dict:
        """Get statistics about newsletter content"""
        articles = newsletter.get("articles", [])

        if not articles:
            return {}

        stats = {
            "total_articles": len(articles),
            "by_category": {},
            "by_section": {},
            "with_keywords": sum(1 for a in articles if a.get("matched_keywords")),
        }

        # Count by category
        for article in articles:
            category = article.get("category", "Unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        # Count by section (News, Research, Tools)
        for article in articles:
            section = article.get("section", "Unknown")
            stats["by_section"][section] = stats["by_section"].get(section, 0) + 1

        return stats


def main():
    """Test TLDR InfoSec scraper"""
    print("=" * 70)
    print("🧪 Testing TLDR InfoSec Newsletter Scraper")
    print("=" * 70 + "\n")

    # Initialize scraper (use mock for demo)
    scraper = TLDRInfoSecScraper(use_mock=True)

    # Fetch newsletter
    newsletter = scraper.fetch_latest_newsletter()

    # Show stats
    stats = scraper.get_stats(newsletter)
    print("📊 NEWSLETTER STATISTICS:")
    print("-" * 70)
    print(f"   Publisher: {newsletter['source']}")
    print(f"   Subscribers: {newsletter.get('subscriber_count', 'N/A')}")
    print(f"   Date: {newsletter['date'].strftime('%Y-%m-%d')}")
    print(f"   Total articles: {stats['total_articles']}")
    print(f"   With matched keywords: {stats['with_keywords']}")

    print(f"\n   By section:")
    for section, count in sorted(stats["by_section"].items(), key=lambda x: x[1], reverse=True):
        print(f"      {section}: {count}")

    print(f"\n   By category:")
    for category, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
        print(f"      {category}: {count}")

    # Show sample articles
    print("\n📋 NEWSLETTER ARTICLES:")
    print("=" * 70)

    for i, article in enumerate(newsletter["articles"], 1):
        print(f"\n{i}. [{article.get('section', 'N/A')}] {article.get('title')}")
        print(f"   Category: {article.get('category')}")
        print(f"   Summary: {article.get('summary')[:120]}...")
        print(f"   Keywords: {', '.join(article.get('matched_keywords', [])[:3])}")
        print(f"   URL: {article.get('url')}")

    print("\n" + "=" * 70)
    print("✅ TLDR InfoSec scraper test complete!")
    print(f"   Note: Using mock data (TLDR doesn't provide public RSS/API)")
    print("=" * 70 + "\n")

    return newsletter


if __name__ == "__main__":
    newsletter = main()
