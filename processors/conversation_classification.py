"""
Conversation Classification Module with Google Gemini Support

Uses Google Gemini (FREE) or GPT-4 Mini to:
1. Score relevance of conversations/articles to SaaS security (0.0 to 1.0)
2. Identify key contributors/authors
3. Detect trending topics
4. Classify urgency (breaking news, general discussion, research)

This is specialized for conversation signals (Reddit, RSS, TLDR)
vs hiring signals.
"""

import os
import json
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.keywords import CONVERSATION_TOPICS

# Load environment variables
load_dotenv()


class ConversationClassifier:
    """Classify conversations and articles using Google Gemini or GPT-4 Mini"""

    def __init__(self, api_key: Optional[str] = None, use_mock: bool = False, provider: str = "auto"):
        """
        Initialize classifier

        Args:
            api_key: API key (or from .env)
            use_mock: If True, use mock responses (for testing without API key)
            provider: "gemini", "openai", or "auto" (tries Gemini first)
        """
        self.use_mock = use_mock
        self.provider = None
        self.categories = list(CONVERSATION_TOPICS.keys())

        if use_mock:
            print("🎭 Using mock classification (no API calls)")
            return

        # Try Gemini first (FREE)
        if provider in ["gemini", "auto"]:
            gemini_key = api_key or os.getenv("GOOGLE_API_KEY")
            if gemini_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_key)
                    self.client = genai.GenerativeModel('gemini-2.5-flash')
                    self.provider = "gemini"
                    print("✅ Google Gemini 2.5 Flash initialized (FREE tier)")
                    return
                except Exception as e:
                    print(f"⚠️  Gemini initialization failed: {e}")

        # Fallback to OpenAI
        if provider in ["openai", "auto"]:
            openai_key = api_key or os.getenv("OPENAI_API_KEY")
            if openai_key and not openai_key.startswith("sk-your"):
                try:
                    from openai import OpenAI
                    self.client = OpenAI(api_key=openai_key)
                    self.provider = "openai"
                    print("✅ OpenAI GPT-4 Mini initialized")
                    return
                except Exception as e:
                    print(f"⚠️  OpenAI initialization failed: {e}")

        # No valid API keys found
        print("⚠️  No valid API keys found. Using mock classification.")
        self.use_mock = True

    def classify_conversation(self, conversation_data: Dict) -> Dict:
        """
        Classify a conversation/article

        Args:
            conversation_data: Dict with title, content, platform, etc.

        Returns:
            Enhanced conversation_data with relevance_score and metadata
        """
        if self.use_mock:
            return self._mock_classify(conversation_data)

        # Build classification prompt
        prompt = self._build_classification_prompt(conversation_data)

        try:
            if self.provider == "gemini":
                result = self._classify_with_gemini(prompt)
            else:  # openai
                result = self._classify_with_openai(prompt)

            # Update conversation data
            conversation_data["relevance_score"] = float(result.get("relevance_score", 0.5))
            conversation_data["urgency"] = result.get("urgency", "normal")
            conversation_data["trending_potential"] = result.get("trending_potential", "low")
            conversation_data["key_insights"] = result.get("key_insights", [])

        except Exception as e:
            print(f"⚠️  Classification error: {e}")
            # Fall back to default scoring
            conversation_data["relevance_score"] = 0.6
            conversation_data["urgency"] = "normal"
            conversation_data["trending_potential"] = "low"

        return conversation_data

    def _classify_with_gemini(self, prompt: str) -> Dict:
        """Classify using Google Gemini"""
        response = self.client.generate_content(prompt)
        text = response.text

        # Extract JSON from response
        json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return json.loads(text)

    def _classify_with_openai(self, prompt: str) -> Dict:
        """Classify using OpenAI GPT-4 Mini"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in cybersecurity content analysis, specializing in SaaS security, SSPM, and breach detection.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=200,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    def _build_classification_prompt(self, conversation_data: Dict) -> str:
        """Build prompt for AI classification"""
        platform = conversation_data.get("platform", "unknown")
        title = conversation_data.get("title", "Unknown")
        content = conversation_data.get("content", conversation_data.get("summary", ""))[:500]
        keywords = ", ".join(conversation_data.get("matched_keywords", []))

        # Different prompts for different platforms
        if platform == "reddit":
            score = conversation_data.get("score", 0)
            comments = conversation_data.get("num_comments", 0)
            context = f"Reddit post with {score} upvotes and {comments} comments"
        elif platform in ["rss", "tldr_infosec"]:
            publisher = conversation_data.get("publisher", "Unknown")
            context = f"Article from {publisher}"
        else:
            context = "Content"

        prompt = f"""Analyze this cybersecurity content for relevance to SaaS Security:

{context}
Title: {title}
Matched Keywords: {keywords}
Content: {content}

Evaluate:
1. Relevance score (0.0 to 1.0) - How relevant is this to SaaS security, SSPM, SaaS breaches, or AI agent security?
2. Urgency: "breaking" (active breach/critical news), "high" (important update), "normal" (general discussion), or "low" (not timely)
3. Trending potential: "high" (likely to go viral), "medium" (moderate interest), or "low" (niche topic)
4. Key insights: List 1-2 key takeaways (brief)

Return ONLY valid JSON with this exact structure (no markdown):
{{
    "relevance_score": 0.85,
    "urgency": "high",
    "trending_potential": "medium",
    "key_insights": ["Brief insight 1", "Brief insight 2"]
}}

Scoring guide:
- 0.9-1.0: Active SaaS breach, critical SSPM vulnerability, major AI agent security issue
- 0.7-0.9: Important SaaS security news, SSPM product launches, compliance updates
- 0.5-0.7: General SaaS security discussion, tool recommendations
- 0.3-0.5: Tangentially related cloud/security topics
- 0.0-0.3: Not relevant to SaaS security"""

        return prompt

    def _mock_classify(self, conversation_data: Dict) -> Dict:
        """Mock classification (for testing without API key)"""
        matched_keywords = conversation_data.get("matched_keywords", [])
        category = conversation_data.get("category", "General")
        platform = conversation_data.get("platform", "unknown")

        # Base score on number of keyword matches
        if len(matched_keywords) >= 3:
            score = 0.9
            urgency = "high"
        elif len(matched_keywords) >= 2:
            score = 0.8
            urgency = "normal"
        elif len(matched_keywords) >= 1:
            score = 0.7
            urgency = "normal"
        else:
            score = 0.5
            urgency = "low"

        # Boost for breach-related categories
        if "breach" in category.lower():
            score = min(1.0, score + 0.15)
            urgency = "breaking"

        # Boost for SSPM and AI Agent Security
        if category in ["SSPM", "AI Agent Security"]:
            score = min(1.0, score + 0.1)

        # Engagement-based trending potential (for Reddit)
        if platform == "reddit":
            score_val = conversation_data.get("score", 0)
            comments = conversation_data.get("num_comments", 0)

            if score_val > 100 or comments > 50:
                trending = "high"
            elif score_val > 50 or comments > 20:
                trending = "medium"
            else:
                trending = "low"
        else:
            trending = "medium"

        conversation_data["relevance_score"] = score
        conversation_data["urgency"] = urgency
        conversation_data["trending_potential"] = trending
        conversation_data["key_insights"] = [f"Related to {category}", "Mock classification"]

        return conversation_data

    def batch_classify(self, conversations: List[Dict], batch_size: int = 10) -> List[Dict]:
        """Classify multiple conversations"""
        provider_name = "Mock" if self.use_mock else (
            "Google Gemini" if self.provider == "gemini" else "GPT-4 Mini"
        )
        print(f"\n🤖 Classifying {len(conversations)} conversations with {provider_name}...")

        classified_conversations = []
        for i, conversation in enumerate(conversations):
            try:
                classified_conversation = self.classify_conversation(conversation)
                classified_conversations.append(classified_conversation)

                if (i + 1) % batch_size == 0:
                    print(f"   Processed {i + 1}/{len(conversations)} conversations...")

            except Exception as e:
                print(f"⚠️  Error classifying conversation {i}: {e}")
                conversation["relevance_score"] = 0.5
                classified_conversations.append(conversation)

        print(f"✅ Classification complete!\n")
        return classified_conversations

    def filter_by_relevance(
        self, conversations: List[Dict], min_score: float = 0.7
    ) -> List[Dict]:
        """Filter conversations by relevance score"""
        filtered = [c for c in conversations if c.get("relevance_score", 0) >= min_score]

        print(f"🔍 Filtered: {len(filtered)}/{len(conversations)} conversations above {min_score} relevance score")
        return filtered

    def get_trending_conversations(
        self, conversations: List[Dict], limit: int = 10
    ) -> List[Dict]:
        """Get top trending conversations"""
        # Sort by relevance + trending potential
        scored = []
        for conv in conversations:
            relevance = conv.get("relevance_score", 0)
            trending_map = {"high": 0.3, "medium": 0.15, "low": 0}
            trending_boost = trending_map.get(conv.get("trending_potential", "low"), 0)

            # Engagement boost for Reddit
            if conv.get("platform") == "reddit":
                engagement_score = (
                    conv.get("score", 0) / 100 + conv.get("num_comments", 0) / 50
                ) * 0.1
                trending_boost += min(0.2, engagement_score)

            total_score = relevance + trending_boost
            scored.append((total_score, conv))

        # Sort and return top N
        scored.sort(reverse=True, key=lambda x: x[0])
        return [conv for _, conv in scored[:limit]]

    def get_classification_stats(self, conversations: List[Dict]) -> Dict:
        """Get statistics about classified conversations"""
        if not conversations:
            return {}

        relevance_scores = [c.get("relevance_score", 0) for c in conversations]

        stats = {
            "total_conversations": len(conversations),
            "avg_relevance": sum(relevance_scores) / len(relevance_scores),
            "high_relevance": sum(1 for score in relevance_scores if score >= 0.8),
            "medium_relevance": sum(1 for score in relevance_scores if 0.6 <= score < 0.8),
            "low_relevance": sum(1 for score in relevance_scores if score < 0.6),
            "by_urgency": {},
            "by_trending": {},
            "by_platform": {},
            "by_category": {},
        }

        # Count by urgency
        for conv in conversations:
            urgency = conv.get("urgency", "normal")
            stats["by_urgency"][urgency] = stats["by_urgency"].get(urgency, 0) + 1

        # Count by trending potential
        for conv in conversations:
            trending = conv.get("trending_potential", "low")
            stats["by_trending"][trending] = stats["by_trending"].get(trending, 0) + 1

        # Count by platform
        for conv in conversations:
            platform = conv.get("platform", "unknown")
            stats["by_platform"][platform] = stats["by_platform"].get(platform, 0) + 1

        # Count by category
        for conv in conversations:
            category = conv.get("category", "Unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        return stats


def main():
    """Test conversation classification"""
    print("=" * 70)
    print("🧪 Testing Conversation Classification with Google Gemini")
    print("=" * 70 + "\n")

    # Get mock conversations from different sources
    from scrapers.reddit_conversations import RedditConversationScraper
    from scrapers.rss_publishers import RSSPublisherScraper

    reddit_scraper = RedditConversationScraper(use_mock=True)
    rss_scraper = RSSPublisherScraper(use_mock=True)

    reddit_conversations = reddit_scraper.search_conversations(limit=20)
    rss_articles = rss_scraper.fetch_all_feeds(max_articles_per_feed=5)

    all_conversations = reddit_conversations + rss_articles
    print(f"📥 Collected {len(all_conversations)} conversations/articles")
    print(f"   Reddit: {len(reddit_conversations)}")
    print(f"   RSS: {len(rss_articles)}\n")

    # Initialize classifier (will try Gemini first)
    classifier = ConversationClassifier()

    # Classify conversations
    classified = classifier.batch_classify(all_conversations[:15])  # Test with 15

    # Filter by relevance
    relevant = classifier.filter_by_relevance(classified, min_score=0.7)

    # Get trending
    trending = classifier.get_trending_conversations(classified, limit=5)

    # Show results
    print("\n📊 CLASSIFICATION RESULTS:")
    print("-" * 70)

    stats = classifier.get_classification_stats(classified)
    print(f"   Total conversations: {stats['total_conversations']}")
    print(f"   Average relevance: {stats['avg_relevance']:.2f}")
    print(f"   High relevance (≥0.8): {stats['high_relevance']}")

    print(f"\n   By urgency:")
    for urgency, count in sorted(stats["by_urgency"].items(), key=lambda x: x[1], reverse=True):
        print(f"      {urgency}: {count}")

    print(f"\n   By trending potential:")
    for trending_val, count in sorted(stats["by_trending"].items(), key=lambda x: x[1], reverse=True):
        print(f"      {trending_val}: {count}")

    print(f"\n   By platform:")
    for platform, count in sorted(stats["by_platform"].items(), key=lambda x: x[1], reverse=True):
        print(f"      {platform}: {count}")

    # Show top trending
    print("\n🔥 TOP TRENDING CONVERSATIONS:")
    print("=" * 70)

    for i, conv in enumerate(trending, 1):
        print(f"\n{i}. [{conv.get('platform').upper()}] {conv.get('title', 'No title')[:80]}")
        print(f"   Relevance: {conv.get('relevance_score', 0):.2f} | Urgency: {conv.get('urgency')} | Trending: {conv.get('trending_potential')}")
        print(f"   Category: {conv.get('category')}")
        if conv.get('key_insights'):
            print(f"   Insights: {'; '.join(conv.get('key_insights', []))}")

    print("\n" + "=" * 70)
    print("✅ Conversation classifier test complete!")
    print("=" * 70 + "\n")

    return classified


if __name__ == "__main__":
    conversations = main()
