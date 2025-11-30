"""
Reddit Conversation Scraper

Monitors Reddit for discussions about:
1. SaaS security breaches (Salesforce, Gainsight, Salesloft)
2. SSPM and SaaS security topics
3. AI Agent Security discussions
4. SaaS compliance and governance

Uses PRAW (Python Reddit API Wrapper) to fetch posts and comments.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.keywords import CONVERSATION_TOPICS, TARGET_SUBREDDITS

# Load environment variables
load_dotenv()


class RedditConversationScraper:
    """Scrape Reddit for SaaS security conversations"""

    def __init__(self, use_mock: bool = True):
        """
        Initialize Reddit scraper

        Args:
            use_mock: If True, use mock data (no Reddit API needed)
        """
        self.use_mock = use_mock
        self.subreddits = TARGET_SUBREDDITS

        if not use_mock:
            try:
                import praw

                # Initialize Reddit API
                self.reddit = praw.Reddit(
                    client_id=os.getenv("REDDIT_CLIENT_ID"),
                    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                    user_agent=os.getenv("REDDIT_USER_AGENT", "SaaS-Security-Signal-Engine/1.0"),
                )
                print("✅ Reddit API initialized")
            except Exception as e:
                print(f"⚠️  Reddit API initialization failed: {e}")
                print("   Using mock data instead")
                self.use_mock = True

    def search_conversations(
        self,
        time_filter: str = "week",
        limit: int = 100,
    ) -> List[Dict]:
        """
        Search Reddit for relevant conversations

        Args:
            time_filter: Time range (hour, day, week, month, year)
            limit: Maximum number of posts to fetch per subreddit

        Returns:
            List of conversation dictionaries
        """
        if self.use_mock:
            return self._get_mock_conversations(limit)

        conversations = []

        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                print(f"🔍 Searching r/{subreddit_name}...")

                # Search for each conversation topic
                for category, keywords in CONVERSATION_TOPICS.items():
                    for keyword in keywords[:3]:  # Limit keywords to avoid rate limits
                        try:
                            # Search submissions
                            for submission in subreddit.search(
                                keyword,
                                time_filter=time_filter,
                                limit=limit // len(keywords),
                            ):
                                conversation = self._parse_submission(submission, category)
                                conversations.append(conversation)

                        except Exception as e:
                            print(f"⚠️  Error searching '{keyword}': {e}")

            except Exception as e:
                print(f"⚠️  Error accessing r/{subreddit_name}: {e}")

        print(f"✅ Found {len(conversations)} conversations")
        return conversations

    def get_trending_topics(
        self,
        time_filter: str = "week",
        limit: int = 50,
    ) -> List[Dict]:
        """
        Get trending/hot discussions from target subreddits

        Args:
            time_filter: Time range
            limit: Maximum posts per subreddit

        Returns:
            List of trending conversation dictionaries
        """
        if self.use_mock:
            return self._get_mock_conversations(limit)

        conversations = []

        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)

                # Get hot posts
                for submission in subreddit.hot(limit=limit):
                    # Check if relevant to our topics
                    if self._is_relevant(submission):
                        conversation = self._parse_submission(submission, category="General")
                        conversations.append(conversation)

            except Exception as e:
                print(f"⚠️  Error accessing r/{subreddit_name}: {e}")

        return conversations

    def _parse_submission(self, submission, category: str) -> Dict:
        """Parse Reddit submission into conversation dictionary"""
        return {
            "platform": "reddit",
            "subreddit": submission.subreddit.display_name,
            "title": submission.title,
            "author": str(submission.author),
            "content": submission.selftext[:1000] if submission.selftext else "",
            "url": f"https://reddit.com{submission.permalink}",
            "score": submission.score,
            "num_comments": submission.num_comments,
            "created_at": datetime.fromtimestamp(submission.created_utc),
            "category": category,
            "matched_keywords": self._extract_matched_keywords(
                submission.title + " " + submission.selftext
            ),
        }

    def _is_relevant(self, submission) -> bool:
        """Check if submission is relevant to SaaS security topics"""
        text = (submission.title + " " + submission.selftext).lower()

        for category, keywords in CONVERSATION_TOPICS.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    return True

        return False

    def _extract_matched_keywords(self, text: str) -> List[str]:
        """Extract matched keywords from text"""
        text_lower = text.lower()
        matched = []

        for category, keywords in CONVERSATION_TOPICS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matched.append(keyword)

        return list(set(matched))  # Remove duplicates

    def _get_mock_conversations(self, limit: int = 100) -> List[Dict]:
        """Generate mock Reddit conversations for testing"""
        from scrapers.demo_data import get_mock_reddit_conversations

        conversations = get_mock_reddit_conversations()
        return conversations[:limit]

    def filter_by_engagement(
        self, conversations: List[Dict], min_score: int = 10, min_comments: int = 5
    ) -> List[Dict]:
        """Filter conversations by engagement metrics"""
        filtered = [
            c
            for c in conversations
            if c.get("score", 0) >= min_score and c.get("num_comments", 0) >= min_comments
        ]

        print(f"🔍 Filtered: {len(filtered)}/{len(conversations)} high-engagement conversations")
        return filtered

    def get_stats(self, conversations: List[Dict]) -> Dict:
        """Get statistics about conversations"""
        if not conversations:
            return {}

        stats = {
            "total_conversations": len(conversations),
            "by_subreddit": {},
            "by_category": {},
            "avg_score": sum(c.get("score", 0) for c in conversations) / len(conversations),
            "avg_comments": sum(c.get("num_comments", 0) for c in conversations)
            / len(conversations),
            "high_engagement": sum(
                1 for c in conversations if c.get("score", 0) >= 50 or c.get("num_comments", 0) >= 20
            ),
        }

        # Count by subreddit
        for conv in conversations:
            subreddit = conv.get("subreddit", "Unknown")
            stats["by_subreddit"][subreddit] = stats["by_subreddit"].get(subreddit, 0) + 1

        # Count by category
        for conv in conversations:
            category = conv.get("category", "Unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        return stats


def main():
    """Test Reddit conversation scraper"""
    print("=" * 70)
    print("🧪 Testing Reddit Conversation Scraper")
    print("=" * 70 + "\n")

    # Initialize scraper (use mock data for demo)
    scraper = RedditConversationScraper(use_mock=True)

    # Search for conversations
    conversations = scraper.search_conversations(limit=50)

    # Filter by engagement
    high_engagement = scraper.filter_by_engagement(
        conversations,
        min_score=20,
        min_comments=10,
    )

    # Show stats
    stats = scraper.get_stats(conversations)
    print("\n📊 CONVERSATION STATISTICS:")
    print("-" * 70)
    print(f"   Total conversations: {stats['total_conversations']}")
    print(f"   Average score: {stats['avg_score']:.1f}")
    print(f"   Average comments: {stats['avg_comments']:.1f}")
    print(f"   High engagement: {stats['high_engagement']}")

    print(f"\n   By subreddit:")
    for subreddit, count in sorted(
        stats["by_subreddit"].items(), key=lambda x: x[1], reverse=True
    ):
        print(f"      r/{subreddit}: {count}")

    print(f"\n   By category:")
    for category, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
        print(f"      {category}: {count}")

    # Show sample conversations
    print("\n📋 SAMPLE CONVERSATIONS (Top 5):")
    print("=" * 70)

    for i, conv in enumerate(high_engagement[:5], 1):
        print(f"\n{i}. r/{conv.get('subreddit')} - {conv.get('score')} upvotes, {conv.get('num_comments')} comments")
        print(f"   Title: {conv.get('title')}")
        print(f"   Category: {conv.get('category')}")
        print(f"   Author: u/{conv.get('author')}")
        print(f"   Posted: {conv.get('created_at').strftime('%Y-%m-%d')}")
        print(f"   Keywords: {', '.join(conv.get('matched_keywords', [])[:3])}")
        print(f"   URL: {conv.get('url')}")

    print("\n" + "=" * 70)
    print("✅ Reddit scraper test complete!")
    print("=" * 70 + "\n")

    return conversations


if __name__ == "__main__":
    conversations = main()
