"""
RSS Feed Scraper for Cybersecurity Publishers

Scrapes top cybersecurity news sources for SaaS security content:
- Dark Reading
- BleepingComputer
- The Hacker News
- SecurityWeek
- Krebs on Security
- And 6 more top publishers
"""

import os
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.keywords import TOP_PUBLISHERS, CONVERSATION_TOPICS


class RSSPublisherScraper:
    """Scrape RSS feeds from top cybersecurity publishers"""

    def __init__(self, use_mock: bool = False):
        """
        Initialize RSS scraper

        Args:
            use_mock: If True, use mock data instead of fetching RSS
        """
        self.use_mock = use_mock
        self.publishers = TOP_PUBLISHERS

    def fetch_all_feeds(
        self,
        max_articles_per_feed: int = 20,
        days_back: int = 7,
    ) -> List[Dict]:
        """
        Fetch articles from all publisher RSS feeds

        Args:
            max_articles_per_feed: Maximum articles to fetch per publisher
            days_back: Only include articles from last N days

        Returns:
            List of article dictionaries
        """
        if self.use_mock:
            return self._get_mock_articles(max_articles_per_feed * len(self.publishers))

        all_articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        print(f"📰 Fetching RSS feeds from {len(self.publishers)} publishers...")
        print(f"   Time range: Last {days_back} days")
        print("-" * 70)

        for publisher_name, publisher_info in self.publishers.items():
            rss_url = publisher_info.get("rss")

            # Skip publishers without RSS
            if not rss_url:
                print(f"⏭️  {publisher_name}: No RSS feed available")
                continue

            try:
                print(f"🔍 Fetching {publisher_name}...")
                feed = feedparser.parse(rss_url)

                if feed.bozo:
                    print(f"⚠️  {publisher_name}: Feed parsing warning")

                articles = self._parse_feed(
                    feed,
                    publisher_name,
                    publisher_info,
                    max_articles_per_feed,
                    cutoff_date,
                )

                all_articles.extend(articles)
                print(f"   ✅ {len(articles)} articles fetched")

            except Exception as e:
                print(f"   ⚠️  Error fetching feed: {e}")

        print(f"\n✅ Total articles fetched: {len(all_articles)}")
        return all_articles

    def _parse_feed(
        self,
        feed,
        publisher_name: str,
        publisher_info: Dict,
        max_articles: int,
        cutoff_date: datetime,
    ) -> List[Dict]:
        """Parse RSS feed into article dictionaries"""
        articles = []

        for entry in feed.entries[:max_articles]:
            try:
                # Parse publication date
                published_date = self._parse_date(entry)

                # Skip old articles
                if published_date and published_date < cutoff_date:
                    continue

                # Extract article data
                article = {
                    "platform": "rss",
                    "publisher": publisher_name,
                    "publisher_url": publisher_info.get("url", ""),
                    "title": entry.get("title", "No title"),
                    "summary": entry.get("summary", entry.get("description", ""))[:500],
                    "url": entry.get("link", ""),
                    "published_at": published_date or datetime.now(),
                    "author": entry.get("author", "Unknown"),
                    "tags": [tag.term for tag in entry.get("tags", [])],
                    "matched_keywords": [],
                    "category": "Unknown",
                }

                # Extract matched keywords
                text = f"{article['title']} {article['summary']}".lower()
                article["matched_keywords"] = self._extract_matched_keywords(text)

                # Determine category
                article["category"] = self._determine_category(text)

                # Only include if relevant (has matched keywords)
                if article["matched_keywords"]:
                    articles.append(article)

            except Exception as e:
                print(f"      ⚠️  Error parsing entry: {e}")

        return articles

    def _parse_date(self, entry) -> Optional[datetime]:
        """Parse publication date from RSS entry"""
        # Try different date fields
        for date_field in ["published_parsed", "updated_parsed", "created_parsed"]:
            if hasattr(entry, date_field):
                date_tuple = getattr(entry, date_field)
                if date_tuple:
                    try:
                        return datetime(*date_tuple[:6])
                    except:
                        pass

        return None

    def _extract_matched_keywords(self, text: str) -> List[str]:
        """Extract matched keywords from article text"""
        matched = []

        for category, keywords in CONVERSATION_TOPICS.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    matched.append(keyword)

        return list(set(matched))  # Remove duplicates

    def _determine_category(self, text: str) -> str:
        """Determine article category based on keywords"""
        # Count matches per category
        category_scores = {}

        for category, keywords in CONVERSATION_TOPICS.items():
            score = sum(1 for kw in keywords if kw.lower() in text)
            if score > 0:
                category_scores[category] = score

        # Return category with most matches
        if category_scores:
            return max(category_scores, key=category_scores.get)

        return "General Security"

    def _get_mock_articles(self, limit: int = 100) -> List[Dict]:
        """Generate mock articles for testing"""
        mock_articles = [
            {
                "platform": "rss",
                "publisher": "The Hacker News",
                "publisher_url": "https://thehackernews.com",
                "title": "New SSPM Tool Detects Misconfigurations in Salesforce and Microsoft 365",
                "summary": "Researchers have developed a new SaaS Security Posture Management tool that automatically detects security misconfigurations across major cloud applications...",
                "url": "https://thehackernews.com/2024/01/sspm-tool.html",
                "published_at": datetime.now() - timedelta(days=2),
                "author": "Security Researcher",
                "tags": ["sspm", "cloud security"],
                "matched_keywords": ["sspm", "saas security", "cloud security"],
                "category": "SSPM",
            },
            {
                "platform": "rss",
                "publisher": "BleepingComputer",
                "publisher_url": "https://www.bleepingcomputer.com",
                "title": "Salesforce Data Breach Exposes Customer Information",
                "summary": "Salesforce announced a security incident affecting thousands of customers. The breach was caused by misconfigured access controls in their SaaS platform...",
                "url": "https://www.bleepingcomputer.com/news/salesforce-breach",
                "published_at": datetime.now() - timedelta(days=1),
                "author": "Lawrence Abrams",
                "tags": ["breach", "salesforce"],
                "matched_keywords": ["salesforce breach", "salesforce security", "saas security"],
                "category": "Salesforce Breach",
            },
            {
                "platform": "rss",
                "publisher": "Dark Reading",
                "publisher_url": "https://www.darkreading.com",
                "title": "AI Agents Pose New Security Risks to Enterprise SaaS Applications",
                "summary": "As organizations adopt AI agents to automate workflows, security teams face new challenges. These autonomous systems can access sensitive data across SaaS platforms...",
                "url": "https://www.darkreading.com/ai-agent-security",
                "published_at": datetime.now() - timedelta(days=3),
                "author": "Kelly Jackson Higgins",
                "tags": ["ai security", "saas"],
                "matched_keywords": ["ai agent security", "saas security", "autonomous agent risk"],
                "category": "AI Agent Security",
            },
            {
                "platform": "rss",
                "publisher": "SecurityWeek",
                "publisher_url": "https://www.securityweek.com",
                "title": "Gainsight Security Incident Affects Customer Success Platforms",
                "summary": "Customer success platform Gainsight disclosed a security incident involving unauthorized access to customer data. The breach highlights risks in SaaS platforms...",
                "url": "https://www.securityweek.com/gainsight-breach",
                "published_at": datetime.now() - timedelta(days=4),
                "author": "Eduard Kovacs",
                "tags": ["breach", "gainsight"],
                "matched_keywords": ["gainsight breach", "saas security"],
                "category": "Gainsight Breach",
            },
            {
                "platform": "rss",
                "publisher": "Krebs on Security",
                "publisher_url": "https://krebsonsecurity.com",
                "title": "SaaS Compliance: New Regulations for Cloud Service Providers",
                "summary": "Regulators are introducing new compliance requirements for SaaS providers, focusing on data protection, access controls, and security monitoring...",
                "url": "https://krebsonsecurity.com/saas-compliance",
                "published_at": datetime.now() - timedelta(days=5),
                "author": "Brian Krebs",
                "tags": ["compliance", "saas"],
                "matched_keywords": ["saas compliance", "cloud governance"],
                "category": "SaaS Compliance",
            },
        ]

        # Repeat mock articles to reach limit
        result = []
        while len(result) < limit:
            result.extend(mock_articles)

        return result[:limit]

    def filter_by_relevance(self, articles: List[Dict], min_keywords: int = 2) -> List[Dict]:
        """Filter articles by number of matched keywords"""
        filtered = [a for a in articles if len(a.get("matched_keywords", [])) >= min_keywords]

        print(f"🔍 Filtered: {len(filtered)}/{len(articles)} highly relevant articles")
        return filtered

    def get_stats(self, articles: List[Dict]) -> Dict:
        """Get statistics about scraped articles"""
        if not articles:
            return {}

        stats = {
            "total_articles": len(articles),
            "by_publisher": {},
            "by_category": {},
            "with_keywords": sum(1 for a in articles if a.get("matched_keywords")),
            "recent_24h": sum(
                1
                for a in articles
                if (datetime.now() - a.get("published_at", datetime.now())).days < 1
            ),
        }

        # Count by publisher
        for article in articles:
            publisher = article.get("publisher", "Unknown")
            stats["by_publisher"][publisher] = stats["by_publisher"].get(publisher, 0) + 1

        # Count by category
        for article in articles:
            category = article.get("category", "Unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        return stats


def main():
    """Test RSS publisher scraper"""
    print("=" * 70)
    print("🧪 Testing RSS Publisher Scraper")
    print("=" * 70 + "\n")

    # Initialize scraper (use mock for demo)
    scraper = RSSPublisherScraper(use_mock=True)

    # Fetch articles
    articles = scraper.fetch_all_feeds(max_articles_per_feed=20, days_back=7)

    # Filter by relevance
    relevant_articles = scraper.filter_by_relevance(articles, min_keywords=2)

    # Show stats
    stats = scraper.get_stats(relevant_articles)
    print("\n📊 ARTICLE STATISTICS:")
    print("-" * 70)
    print(f"   Total articles: {stats['total_articles']}")
    print(f"   With matched keywords: {stats['with_keywords']}")
    print(f"   Recent (24h): {stats['recent_24h']}")

    print(f"\n   By publisher:")
    for publisher, count in sorted(
        stats["by_publisher"].items(), key=lambda x: x[1], reverse=True
    )[:5]:
        print(f"      {publisher}: {count}")

    print(f"\n   By category:")
    for category, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
        print(f"      {category}: {count}")

    # Show sample articles
    print("\n📋 SAMPLE ARTICLES (Top 5):")
    print("=" * 70)

    for i, article in enumerate(relevant_articles[:5], 1):
        print(f"\n{i}. {article.get('publisher')}")
        print(f"   Title: {article.get('title')}")
        print(f"   Category: {article.get('category')}")
        print(f"   Published: {article.get('published_at').strftime('%Y-%m-%d %H:%M')}")
        print(f"   Keywords: {', '.join(article.get('matched_keywords', [])[:3])}")
        print(f"   URL: {article.get('url')}")

    print("\n" + "=" * 70)
    print("✅ RSS scraper test complete!")
    print("=" * 70 + "\n")

    return articles


if __name__ == "__main__":
    articles = main()
