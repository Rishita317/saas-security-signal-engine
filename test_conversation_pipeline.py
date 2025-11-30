"""
End-to-End Conversation Pipeline Test with Google Gemini

Tests the complete conversation signal pipeline:
1. Data collection from Reddit, RSS, and TLDR InfoSec
2. Classification with Google Gemini (FREE)
3. Trending detection
4. Filtering and export

This demonstrates the conversation tracking component of the
SaaS Security Signal Engine.
"""

import json
import csv
import os
from datetime import datetime
from scrapers.reddit_conversations import RedditConversationScraper
from scrapers.rss_publishers import RSSPublisherScraper
from scrapers.tldr_infosec import TLDRInfoSecScraper
from processors.conversation_classification import ConversationClassifier


def run_conversation_pipeline(
    reddit_limit: int = 50,
    rss_limit: int = 20,
    export_csv: bool = True,
):
    """
    Run the complete conversation signal pipeline

    Args:
        reddit_limit: Number of Reddit conversations to fetch
        rss_limit: Number of articles per RSS feed
        export_csv: Whether to export results to CSV
    """
    print("\n" + "=" * 70)
    print("🔐 SAAS SECURITY SIGNAL ENGINE - CONVERSATION PIPELINE")
    print("=" * 70 + "\n")

    # Step 1: Data Collection
    print("📥 STEP 1: Data Collection")
    print("-" * 70)

    # Reddit conversations
    reddit_scraper = RedditConversationScraper(use_mock=True)
    reddit_conversations = reddit_scraper.search_conversations(limit=reddit_limit)
    print(f"✅ Reddit: {len(reddit_conversations)} conversations")

    # RSS feeds
    rss_scraper = RSSPublisherScraper(use_mock=True)
    rss_articles = rss_scraper.fetch_all_feeds(max_articles_per_feed=rss_limit)
    print(f"✅ RSS: {len(rss_articles)} articles")

    # TLDR InfoSec
    tldr_scraper = TLDRInfoSecScraper(use_mock=True)
    tldr_newsletter = tldr_scraper.fetch_latest_newsletter()
    tldr_articles = tldr_newsletter.get("articles", [])
    print(f"✅ TLDR InfoSec: {len(tldr_articles)} articles")

    # Combine all sources
    all_conversations = reddit_conversations + rss_articles + tldr_articles
    print(f"\n📊 Total collected: {len(all_conversations)} items\n")

    # Step 2: Classification with Gemini
    print("🤖 STEP 2: Relevance Classification (Google Gemini - FREE)")
    print("-" * 70)
    classifier = ConversationClassifier()  # Will use Gemini automatically
    classified = classifier.batch_classify(all_conversations)

    classification_stats = classifier.get_classification_stats(classified)
    print(f"   Average relevance score: {classification_stats['avg_relevance']:.2f}")
    print(f"   High relevance (≥0.8): {classification_stats['high_relevance']}")
    print(f"   Breaking/High urgency: {classification_stats['by_urgency'].get('breaking', 0) + classification_stats['by_urgency'].get('high', 0)}\n")

    # Step 3: Filter by relevance
    print("🔎 STEP 3: Filtering by Relevance")
    print("-" * 70)
    relevant = classifier.filter_by_relevance(classified, min_score=0.7)
    print()

    # Step 4: Detect trending conversations
    print("🔥 STEP 4: Trending Detection")
    print("-" * 70)
    trending = classifier.get_trending_conversations(classified, limit=10)
    print(f"   Identified {len(trending)} top trending conversations\n")

    # Step 5: Display Results
    print("📊 STEP 5: Results Summary")
    print("-" * 70)
    print(f"\n✅ PIPELINE COMPLETE!")
    print(f"   Input: {len(all_conversations)} items")
    print(f"   Output: {len(relevant)} relevant items ({len(relevant)/len(all_conversations)*100:.1f}% pass rate)")

    print(f"\n   By Platform:")
    for platform, count in sorted(
        classification_stats["by_platform"].items(), key=lambda x: x[1], reverse=True
    ):
        print(f"      {platform}: {count}")

    print(f"\n   By Category:")
    for category, count in sorted(
        classification_stats["by_category"].items(), key=lambda x: x[1], reverse=True
    )[:5]:
        print(f"      {category}: {count}")

    print(f"\n   By Urgency:")
    for urgency, count in sorted(
        classification_stats["by_urgency"].items(), key=lambda x: x[1], reverse=True
    ):
        print(f"      {urgency}: {count}")

    print(f"\n   Trending Potential:")
    for trending_val, count in sorted(
        classification_stats["by_trending"].items(), key=lambda x: x[1], reverse=True
    ):
        print(f"      {trending_val}: {count}")

    # Show top contributors (from Reddit)
    reddit_only = [c for c in relevant if c.get("platform") == "reddit"]
    if reddit_only:
        authors = {}
        for conv in reddit_only:
            author = conv.get("author", "Unknown")
            authors[author] = authors.get(author, 0) + 1

        print(f"\n   Top Contributors (Reddit):")
        for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"      u/{author}: {count} posts")

    # Show top publishers
    rss_only = [c for c in relevant if c.get("platform") in ["rss", "tldr_infosec"]]
    if rss_only:
        publishers = {}
        for conv in rss_only:
            publisher = conv.get("publisher", "Unknown")
            publishers[publisher] = publishers.get(publisher, 0) + 1

        print(f"\n   Top Publishers:")
        for publisher, count in sorted(publishers.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"      {publisher}: {count} articles")

    # Step 6: Export (optional)
    if export_csv:
        export_to_csv(relevant, trending, suffix="_conversations")

    print("\n" + "=" * 70)

    return relevant, trending


def export_to_csv(conversations: list, trending: list, suffix: str = ""):
    """Export conversations to CSV files"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Export all relevant conversations
    all_filename = f"data/conversation_signals{suffix}_{timestamp}.csv"
    _write_csv(conversations, all_filename)
    print(f"\n💾 Exported all relevant conversations to: {all_filename}")

    # Export trending conversations
    trending_filename = f"data/trending_conversations{suffix}_{timestamp}.csv"
    _write_csv(trending, trending_filename)
    print(f"💾 Exported trending conversations to: {trending_filename}")


def _write_csv(conversations: list, filename: str):
    """Write conversations to CSV file"""
    if not conversations:
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        # Determine fields based on platform
        base_fields = [
            "platform",
            "title",
            "category",
            "relevance_score",
            "urgency",
            "trending_potential",
            "published_at",
            "matched_keywords",
            "url",
        ]

        # Add platform-specific fields
        sample = conversations[0]
        if sample.get("platform") == "reddit":
            extra_fields = ["subreddit", "author", "score", "num_comments"]
        elif sample.get("platform") in ["rss", "tldr_infosec"]:
            extra_fields = ["publisher", "author"]
        else:
            extra_fields = []

        fieldnames = base_fields + extra_fields

        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for conv in conversations:
            # Format matched_keywords as string
            conv_copy = conv.copy()
            conv_copy["matched_keywords"] = ", ".join(conv.get("matched_keywords", []))

            # Format published_at
            if isinstance(conv.get("published_at"), datetime):
                conv_copy["published_at"] = conv["published_at"].strftime('%Y-%m-%d %H:%M:%S')
            elif "created_at" in conv:
                conv_copy["published_at"] = conv["created_at"].strftime('%Y-%m-%d %H:%M:%S')

            writer.writerow(conv_copy)


def main():
    """Run the conversation pipeline test"""
    relevant, trending = run_conversation_pipeline(
        reddit_limit=50,
        rss_limit=20,
        export_csv=True,
    )

    # Show trending conversations
    print("\n🔥 TOP 10 TRENDING CONVERSATIONS:")
    print("=" * 70)

    for i, conv in enumerate(trending, 1):
        platform = conv.get("platform", "unknown").upper()
        title = conv.get("title", "No title")

        print(f"\n{i}. [{platform}] {title[:80]}")
        print(f"   Relevance: {conv.get('relevance_score', 0):.2f} ⭐")
        print(f"   Urgency: {conv.get('urgency')} | Trending: {conv.get('trending_potential')}")
        print(f"   Category: {conv.get('category')}")

        # Platform-specific details
        if platform == "REDDIT":
            print(f"   r/{conv.get('subreddit')} by u/{conv.get('author')}")
            print(f"   Engagement: {conv.get('score')} upvotes, {conv.get('num_comments')} comments")
        elif platform in ["RSS", "TLDR_INFOSEC"]:
            print(f"   Publisher: {conv.get('publisher')}")
            print(f"   Published: {conv.get('published_at').strftime('%Y-%m-%d')}")

        print(f"   URL: {conv.get('url')}")

        # Show key insights if available
        if conv.get("key_insights"):
            print(f"   💡 Insights: {'; '.join(conv.get('key_insights', []))}")

    print("\n" + "=" * 70)
    print("🎉 Conversation pipeline test complete!")
    print("=" * 70 + "\n")

    # Summary
    print("📋 WHAT WE TRACKED:")
    print("-" * 70)
    print("✅ Reddit discussions about SaaS security, breaches, SSPM")
    print("✅ RSS articles from 10+ top cybersecurity publishers")
    print("✅ TLDR InfoSec newsletter (410,000+ subscribers)")
    print("✅ AI-powered relevance scoring with Google Gemini")
    print("✅ Trending detection based on engagement + relevance")
    print("✅ Urgency classification (breaking/high/normal/low)")
    print("✅ Exported to CSV for GTM team analysis")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
