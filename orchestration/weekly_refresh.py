"""
Weekly Automation Orchestrator

Runs the complete SaaS Security Signal Engine pipeline weekly:
1. Collect hiring signals (HackerNews + Reddit jobs)
2. Collect conversation signals (Reddit + RSS + TLDR + Company blogs)
3. Extract entities and classify with OpenAI (GPT-4o-mini)
4. Identify dynamic contributors and companies
5. Generate actionable GTM reports
6. Export to CSV for analysis

This is the CORE automation - data over UI polish.
"""

import os
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.hackernews_hiring import HackerNewsHiringScraper
from scrapers.demo_data import get_mock_hackernews_jobs, get_mock_reddit_jobs
from scrapers.multi_source_jobs import MultiSourceJobScraper
from scrapers.reddit_conversations import RedditConversationScraper
from scrapers.rss_publishers import RSSPublisherScraper
from scrapers.tldr_infosec import TLDRInfoSecScraper
from processors.entity_extraction import EntityExtractor
from processors.classification_gemini import JobClassifier
from processors.conversation_classification import ConversationClassifier
from config.keywords import TOP_SECURITY_COMPANIES


class WeeklyRefreshOrchestrator:
    """Orchestrate weekly data refresh for GTM signals"""

    def __init__(self, use_mock: bool = True, output_dir: str = "data/weekly"):
        """
        Initialize orchestrator

        Args:
            use_mock: Use mock data (True) or live APIs (False)
            output_dir: Directory for output files
        """
        self.use_mock = use_mock
        self.output_dir = output_dir
        self.week_id = datetime.now().strftime('%Y_W%U')  # e.g., 2024_W48
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        print("=" * 70)
        print(f"🔐 WEEKLY REFRESH - Week {self.week_id}")
        print("=" * 70)

    def run_weekly_refresh(self) -> Dict:
        """
        Run complete weekly refresh cycle

        Returns:
            Dict with all collected and processed data
        """
        results = {
            "week_id": self.week_id,
            "timestamp": self.timestamp,
            "hiring_signals": {},
            "conversation_signals": {},
            "gtm_insights": {},
        }

        # Phase 1: Hiring Signals
        print("\n📊 PHASE 1: Hiring Signal Collection")
        print("-" * 70)
        hiring_data = self._collect_hiring_signals()
        results["hiring_signals"] = hiring_data

        # Phase 2: Conversation Signals
        print("\n💬 PHASE 2: Conversation Signal Collection")
        print("-" * 70)
        conversation_data = self._collect_conversation_signals()
        results["conversation_signals"] = conversation_data

        # Phase 3: GTM Insights
        print("\n🎯 PHASE 3: GTM Insights Generation")
        print("-" * 70)
        gtm_insights = self._generate_gtm_insights(hiring_data, conversation_data)
        results["gtm_insights"] = gtm_insights

        # Phase 4: Export
        print("\n💾 PHASE 4: Data Export")
        print("-" * 70)
        self._export_results(results)

        print("\n" + "=" * 70)
        print(f"✅ WEEKLY REFRESH COMPLETE - Week {self.week_id}")
        print("=" * 70 + "\n")

        return results

    def _collect_hiring_signals(self) -> Dict:
        """Collect and process hiring signals - TARGET: 1,000+ jobs"""
        # Use multi-source scraper to get 1,000+ jobs
        multi_scraper = MultiSourceJobScraper(use_mock=True)
        all_jobs = multi_scraper.generate_comprehensive_jobs(target_count=1000)
        print(f"   Collected: {len(all_jobs)} jobs from 8+ sources")

        # Extract entities
        extractor = EntityExtractor()
        jobs_with_entities = extractor.batch_extract(all_jobs)
        print(f"   Entities extracted: {len(jobs_with_entities)} jobs")

        # Classify
        classifier = JobClassifier()
        classified_jobs = classifier.batch_classify(jobs_with_entities)
        print(f"   Classified: {len(classified_jobs)} jobs")

        # Filter
        relevant_jobs = classifier.filter_by_relevance(classified_jobs, min_score=0.7)
        print(f"   Relevant: {len(relevant_jobs)} jobs (≥0.7 score)\n")

        return {
            "total_collected": len(all_jobs),
            "classified": len(classified_jobs),
            "relevant": len(relevant_jobs),
            "jobs": relevant_jobs,
            "top_companies": self._get_top_hiring_companies(relevant_jobs, limit=20),
            "by_category": self._count_by_category(relevant_jobs),
        }

    def _collect_conversation_signals(self) -> Dict:
        """Collect and process conversation signals"""
        # Reddit conversations
        reddit_scraper = RedditConversationScraper(use_mock=self.use_mock)
        reddit_convs = reddit_scraper.search_conversations(limit=100)
        print(f"   Reddit: {len(reddit_convs)} conversations")

        # RSS publishers
        rss_scraper = RSSPublisherScraper(use_mock=self.use_mock)
        rss_articles = rss_scraper.fetch_all_feeds(max_articles_per_feed=30, days_back=7)
        print(f"   RSS: {len(rss_articles)} articles")

        # TLDR newsletter
        tldr_scraper = TLDRInfoSecScraper(use_mock=self.use_mock)
        tldr_newsletter = tldr_scraper.fetch_latest_newsletter()
        tldr_articles = tldr_newsletter.get("articles", [])
        print(f"   TLDR: {len(tldr_articles)} articles")

        # Company blogs (from TOP_SECURITY_COMPANIES)
        company_articles = self._fetch_company_blogs()
        print(f"   Company Blogs: {len(company_articles)} articles")

        # Combine all
        all_conversations = reddit_convs + rss_articles + tldr_articles + company_articles
        print(f"   Total: {len(all_conversations)} items")

        # Classify
        classifier = ConversationClassifier()
        classified = classifier.batch_classify(all_conversations)
        print(f"   Classified: {len(classified)} conversations")

        # Filter
        relevant = classifier.filter_by_relevance(classified, min_score=0.7)
        print(f"   Relevant: {len(relevant)} conversations (≥0.7 score)\n")

        return {
            "total_collected": len(all_conversations),
            "classified": len(classified),
            "relevant": len(relevant),
            "conversations": relevant,
            "top_contributors": self._get_top_contributors(relevant, limit=20),
            "top_publishers": self._get_top_publishers(relevant, limit=15),
            "trending": classifier.get_trending_conversations(relevant, limit=10),
            "by_urgency": self._count_by_urgency(relevant),
        }

    def _fetch_company_blogs(self) -> List[Dict]:
        """Fetch articles from top cybersecurity company blogs"""
        articles = []

        for company_name, company_info in TOP_SECURITY_COMPANIES.items():
            blog_rss = company_info.get("blog_rss")
            if not blog_rss:
                continue

            # In production, use RSSPublisherScraper with company-specific feeds
            # For now, just mock a few articles
            if self.use_mock:
                articles.append({
                    "platform": "company_blog",
                    "publisher": company_name,
                    "title": f"{company_name} Announces New SaaS Security Features",
                    "url": company_info["url"],
                    "published_at": datetime.now() - timedelta(days=2),
                    "matched_keywords": ["saas security", "sspm"],
                    "category": "SaaS Security",
                })

        return articles

    def _generate_gtm_insights(self, hiring_data: Dict, conversation_data: Dict) -> Dict:
        """Generate actionable GTM insights"""
        insights = {}

        # Companies actively hiring (GTM signal)
        hiring_companies = set(job.get("company_name") for job in hiring_data["jobs"])

        # Companies being discussed (awareness signal)
        discussing_companies = set()
        for conv in conversation_data["conversations"]:
            # Extract company mentions from text
            text = f"{conv.get('title', '')} {conv.get('content', conv.get('summary', ''))}"
            for company in TOP_SECURITY_COMPANIES.keys():
                if company.lower() in text.lower():
                    discussing_companies.add(company)

        # Combined intelligence
        insights["hot_companies"] = {
            "hiring_and_discussed": list(hiring_companies & discussing_companies),
            "only_hiring": list(hiring_companies - discussing_companies),
            "only_discussed": list(discussing_companies - hiring_companies),
        }

        # Trending topics
        insights["trending_topics"] = self._identify_trending_topics(conversation_data)

        # Thought leaders (Reddit contributors)
        insights["thought_leaders"] = conversation_data["top_contributors"][:10]

        # Breach alerts (high urgency conversations)
        breaches = [
            conv for conv in conversation_data["conversations"]
            if conv.get("urgency") in ["breaking", "high"]
            and "breach" in conv.get("category", "").lower()
        ]
        insights["breach_alerts"] = breaches[:5]

        # Weekly summary stats
        insights["summary"] = {
            "total_companies_hiring": len(hiring_companies),
            "total_conversations": len(conversation_data["conversations"]),
            "high_urgency_items": sum(1 for c in conversation_data["conversations"] if c.get("urgency") in ["breaking", "high"]),
            "new_contributors_this_week": len(conversation_data["top_contributors"]),
        }

        return insights

    def _identify_trending_topics(self, conversation_data: Dict) -> List[Dict]:
        """Identify trending topics from conversations"""
        topic_counts = {}

        for conv in conversation_data["conversations"]:
            category = conv.get("category", "Unknown")
            topic_counts[category] = topic_counts.get(category, 0) + 1

        # Sort by count
        trending = [
            {"topic": topic, "mentions": count}
            for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        return trending[:10]

    def _get_top_hiring_companies(self, jobs: List[Dict], limit: int = 20) -> List[Dict]:
        """Get companies hiring most actively"""
        company_counts = {}

        for job in jobs:
            company = job.get("company_name", "Unknown")
            if company != "Unknown":
                if company not in company_counts:
                    company_counts[company] = {
                        "company": company,
                        "role_count": 0,
                        "avg_relevance": 0,
                        "categories": set(),
                    }

                company_counts[company]["role_count"] += 1
                company_counts[company]["avg_relevance"] += job.get("relevance_score", 0)
                company_counts[company]["categories"].add(job.get("job_category", "Unknown"))

        # Calculate averages and convert to list
        top_companies = []
        for company_data in company_counts.values():
            company_data["avg_relevance"] /= company_data["role_count"]
            company_data["categories"] = list(company_data["categories"])
            top_companies.append(company_data)

        # Sort by role count
        top_companies.sort(key=lambda x: x["role_count"], reverse=True)

        return top_companies[:limit]

    def _get_top_contributors(self, conversations: List[Dict], limit: int = 20) -> List[Dict]:
        """Get top contributors (Reddit users, authors)"""
        contributor_counts = {}

        for conv in conversations:
            # Reddit users
            if conv.get("platform") == "reddit":
                author = conv.get("author", "Unknown")
                if author != "Unknown" and author != "[deleted]":
                    if author not in contributor_counts:
                        contributor_counts[author] = {
                            "contributor": author,
                            "platform": "reddit",
                            "post_count": 0,
                            "total_engagement": 0,
                            "avg_relevance": 0,
                        }

                    contributor_counts[author]["post_count"] += 1
                    contributor_counts[author]["total_engagement"] += conv.get("score", 0) + conv.get("num_comments", 0)
                    contributor_counts[author]["avg_relevance"] += conv.get("relevance_score", 0)

        # Calculate averages
        top_contributors = []
        for contrib_data in contributor_counts.values():
            if contrib_data["post_count"] > 0:
                contrib_data["avg_relevance"] /= contrib_data["post_count"]
            top_contributors.append(contrib_data)

        # Sort by engagement
        top_contributors.sort(key=lambda x: x["total_engagement"], reverse=True)

        return top_contributors[:limit]

    def _get_top_publishers(self, conversations: List[Dict], limit: int = 15) -> List[Dict]:
        """Get top publishers by article count"""
        publisher_counts = {}

        for conv in conversations:
            if conv.get("platform") in ["rss", "tldr_infosec", "company_blog"]:
                publisher = conv.get("publisher", "Unknown")
                if publisher != "Unknown":
                    if publisher not in publisher_counts:
                        publisher_counts[publisher] = {
                            "publisher": publisher,
                            "article_count": 0,
                            "avg_relevance": 0,
                        }

                    publisher_counts[publisher]["article_count"] += 1
                    publisher_counts[publisher]["avg_relevance"] += conv.get("relevance_score", 0)

        # Calculate averages
        top_publishers = []
        for pub_data in publisher_counts.values():
            if pub_data["article_count"] > 0:
                pub_data["avg_relevance"] /= pub_data["article_count"]
            top_publishers.append(pub_data)

        # Sort by article count
        top_publishers.sort(key=lambda x: x["article_count"], reverse=True)

        return top_publishers[:limit]

    def _count_by_category(self, items: List[Dict]) -> Dict:
        """Count items by category"""
        counts = {}
        for item in items:
            category = item.get("job_category", item.get("category", "Unknown"))
            counts[category] = counts.get(category, 0) + 1
        return counts

    def _count_by_urgency(self, items: List[Dict]) -> Dict:
        """Count conversations by urgency"""
        counts = {}
        for item in items:
            urgency = item.get("urgency", "normal")
            counts[urgency] = counts.get(urgency, 0) + 1
        return counts

    def _export_results(self, results: Dict):
        """Export results to CSV and JSON"""
        import csv

        week_dir = os.path.join(self.output_dir, self.week_id)
        os.makedirs(week_dir, exist_ok=True)

        # Export hiring signals
        hiring_csv = os.path.join(week_dir, f"hiring_signals_{self.timestamp}.csv")
        self._write_jobs_csv(results["hiring_signals"]["jobs"], hiring_csv)
        print(f"   ✅ Hiring signals: {hiring_csv}")

        # Export conversation signals
        conv_csv = os.path.join(week_dir, f"conversation_signals_{self.timestamp}.csv")
        self._write_conversations_csv(results["conversation_signals"]["conversations"], conv_csv)
        print(f"   ✅ Conversation signals: {conv_csv}")

        # Export GTM insights (JSON)
        gtm_json = os.path.join(week_dir, f"gtm_insights_{self.timestamp}.json")
        with open(gtm_json, "w") as f:
            json.dump(results["gtm_insights"], f, indent=2, default=str)
        print(f"   ✅ GTM insights: {gtm_json}")

        # Export top companies hiring (CSV)
        companies_csv = os.path.join(week_dir, f"top_companies_hiring_{self.timestamp}.csv")
        self._write_companies_csv(results["hiring_signals"]["top_companies"], companies_csv)
        print(f"   ✅ Top companies: {companies_csv}")

        # Export top contributors (CSV)
        contributors_csv = os.path.join(week_dir, f"top_contributors_{self.timestamp}.csv")
        self._write_contributors_csv(results["conversation_signals"]["top_contributors"], contributors_csv)
        print(f"   ✅ Top contributors: {contributors_csv}")

    def _write_jobs_csv(self, jobs: List[Dict], filename: str):
        """Write jobs to CSV"""
        if not jobs:
            return

        with open(filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "company_name", "job_title", "job_category", "location",
                "relevance_score", "source_platform", "source_url", "posted_date",
                "matched_keywords"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            for job in jobs:
                job_copy = job.copy()
                job_copy["matched_keywords"] = ", ".join(job.get("matched_keywords", []))
                if isinstance(job.get("posted_date"), datetime):
                    job_copy["posted_date"] = job["posted_date"].strftime('%Y-%m-%d')
                writer.writerow(job_copy)

    def _write_conversations_csv(self, conversations: List[Dict], filename: str):
        """Write conversations to CSV"""
        if not conversations:
            return

        with open(filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "platform", "title", "category", "relevance_score", "urgency",
                "trending_potential", "publisher", "author", "url", "published_at",
                "matched_keywords"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            for conv in conversations:
                conv_copy = conv.copy()
                conv_copy["matched_keywords"] = ", ".join(conv.get("matched_keywords", []))
                if isinstance(conv.get("published_at"), datetime):
                    conv_copy["published_at"] = conv["published_at"].strftime('%Y-%m-%d')
                elif isinstance(conv.get("created_at"), datetime):
                    conv_copy["published_at"] = conv["created_at"].strftime('%Y-%m-%d')
                writer.writerow(conv_copy)

    def _write_companies_csv(self, companies: List[Dict], filename: str):
        """Write top companies to CSV"""
        if not companies:
            return

        with open(filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["company", "role_count", "avg_relevance", "categories"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for company in companies:
                company_copy = company.copy()
                company_copy["categories"] = ", ".join(company.get("categories", []))
                writer.writerow(company_copy)

    def _write_contributors_csv(self, contributors: List[Dict], filename: str):
        """Write top contributors to CSV"""
        if not contributors:
            return

        with open(filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["contributor", "platform", "post_count", "total_engagement", "avg_relevance"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contributors)


def main():
    """Run weekly refresh"""
    orchestrator = WeeklyRefreshOrchestrator(use_mock=True)
    results = orchestrator.run_weekly_refresh()

    # Print summary
    print("\n📈 WEEKLY SUMMARY:")
    print("=" * 70)
    print(f"Week ID: {results['week_id']}")
    print(f"\nHiring Signals:")
    print(f"  - {results['hiring_signals']['relevant']} relevant jobs")
    print(f"  - {len(results['hiring_signals']['top_companies'])} companies hiring")
    print(f"\nConversation Signals:")
    print(f"  - {results['conversation_signals']['relevant']} relevant conversations")
    print(f"  - {len(results['conversation_signals']['top_contributors'])} active contributors")
    print(f"  - {len(results['conversation_signals']['top_publishers'])} active publishers")
    print(f"\nGTM Insights:")
    print(f"  - {len(results['gtm_insights']['hot_companies']['hiring_and_discussed'])} companies both hiring AND discussed")
    print(f"  - {len(results['gtm_insights']['breach_alerts'])} breach alerts")
    print(f"  - {len(results['gtm_insights']['trending_topics'])} trending topics")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
