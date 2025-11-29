"""
HackerNews "Who's Hiring" Thread Scraper

Scrapes monthly "Who's Hiring" threads from HackerNews to find
companies hiring for SaaS security-related roles.

Data Source: HackerNews Algolia Search API (free, no auth required)
"""

import requests
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.keywords import HIRING_KEYWORDS


class HackerNewsHiringScraper:
    """Scraper for HackerNews 'Who's Hiring' threads"""

    def __init__(self):
        self.algolia_api_url = "http://hn.algolia.com/api/v1"
        self.session = requests.Session()
        self.keywords = self._flatten_keywords()

    def _flatten_keywords(self) -> List[str]:
        """Flatten all hiring keywords into a single list"""
        all_keywords = []
        for category, keywords in HIRING_KEYWORDS.items():
            all_keywords.extend([kw.lower() for kw in keywords])
        return all_keywords

    def search_hiring_threads(self, months_back: int = 2) -> List[Dict]:
        """
        Search for recent "Who's Hiring" threads

        Args:
            months_back: How many months back to search

        Returns:
            List of thread IDs and metadata
        """
        print(f"🔍 Searching for HackerNews 'Who's Hiring' threads...")

        # Search for Ask HN posts with "hiring" in title
        params = {
            "query": "hiring",
            "tags": "(story,ask_hn)",
            "hitsPerPage": 30,
        }

        try:
            response = self.session.get(
                f"{self.algolia_api_url}/search", params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            threads = []
            cutoff_date = datetime.now() - timedelta(days=months_back * 30)

            print(f"   Examining {len(data.get('hits', []))} search results...")

            for hit in data.get("hits", []):
                title = hit.get("title", "").lower()
                created_at = datetime.fromtimestamp(hit.get("created_at_i", 0))

                # Filter for "Ask HN: Who is hiring?" threads
                # More flexible matching - just look for "who" and "hiring"
                if (
                    "hiring" in title
                    and ("who" in title or "freelancer" in title or "seeking" in title)
                    and created_at > cutoff_date
                ):
                    threads.append(
                        {
                            "story_id": hit.get("objectID"),
                            "title": hit.get("title"),
                            "created_at": created_at,
                            "num_comments": hit.get("num_comments", 0),
                        }
                    )
                    print(f"   ✓ {hit.get('title')}")

            print(f"✅ Found {len(threads)} hiring threads")
            return sorted(threads, key=lambda x: x["created_at"], reverse=True)

        except Exception as e:
            print(f"❌ Error searching threads: {e}")
            return []

    def get_thread_comments(self, story_id: str) -> List[Dict]:
        """
        Get all comments from a specific thread

        Args:
            story_id: HackerNews story ID

        Returns:
            List of comment data
        """
        print(f"📥 Fetching comments from thread {story_id}...")

        try:
            # Get the story item which includes all comments
            response = self.session.get(
                f"{self.algolia_api_url}/items/{story_id}", timeout=10
            )
            response.raise_for_status()
            data = response.json()

            comments = []
            self._extract_comments_recursive(data, comments)

            print(f"✅ Retrieved {len(comments)} comments")
            return comments

        except Exception as e:
            print(f"❌ Error fetching comments: {e}")
            return []

    def _extract_comments_recursive(
        self, item: Dict, comments: List[Dict], depth: int = 0
    ):
        """Recursively extract comments from nested structure"""
        if not item:
            return

        # Add current comment if it has text
        if item.get("text") and depth > 0:  # depth > 0 to skip the story itself
            comments.append(
                {
                    "id": item.get("id"),
                    "author": item.get("author"),
                    "text": item.get("text"),
                    "created_at": datetime.fromtimestamp(
                        item.get("created_at_i", 0)
                    ),
                }
            )

        # Process child comments
        for child in item.get("children", []):
            self._extract_comments_recursive(child, comments, depth + 1)

    def filter_relevant_comments(self, comments: List[Dict]) -> List[Dict]:
        """
        Filter comments that contain SaaS security keywords

        Args:
            comments: List of all comments

        Returns:
            List of relevant comments
        """
        print(f"🔍 Filtering comments for SaaS security keywords...")

        relevant_comments = []
        for comment in comments:
            text = comment.get("text", "").lower()

            # Check if any keyword is in the comment
            for keyword in self.keywords:
                if keyword in text:
                    comment["matched_keywords"] = self._get_matched_keywords(text)
                    relevant_comments.append(comment)
                    break  # Don't check other keywords for this comment

        print(f"✅ Found {len(relevant_comments)} relevant job posts")
        return relevant_comments

    def _get_matched_keywords(self, text: str) -> List[str]:
        """Get all keywords that match in the text"""
        matched = []
        for keyword in self.keywords:
            if keyword in text.lower():
                matched.append(keyword)
        return matched

    def extract_job_info(self, comment: Dict) -> Dict:
        """
        Extract structured job information from comment text

        Args:
            comment: Comment data with text

        Returns:
            Structured job data
        """
        text = comment.get("text", "")

        # Try to extract company name (usually at the start or in bold)
        company = self._extract_company_name(text)

        # Try to extract location
        location = self._extract_location(text)

        # Determine category based on matched keywords
        category = self._determine_category(comment.get("matched_keywords", []))

        return {
            "source_platform": "HackerNews",
            "source_url": f"https://news.ycombinator.com/item?id={comment.get('id')}",
            "company_name": company,
            "job_title": "Multiple roles",  # HN posts usually have multiple roles
            "location": location,
            "job_category": category,
            "posted_date": comment.get("created_at"),
            "raw_text": text[:500],  # First 500 chars for debugging
            "matched_keywords": comment.get("matched_keywords", []),
        }

    def _extract_company_name(self, text: str) -> Optional[str]:
        """
        Extract company name from job post text

        HN format usually: "CompanyName (https://company.com) | Location | etc"
        """
        # Remove HTML tags first
        text_clean = re.sub(r"<[^>]+>", "", text)

        # Try to find company at the start (before | or ()
        match = re.match(r"^([A-Z][a-zA-Z0-9\s&\.]+?)(?:\s*\|||\s*\()", text_clean)
        if match:
            company = match.group(1).strip()
            # Remove common prefixes
            company = re.sub(r"^(at|join|hiring|seeking)\s+", "", company, flags=re.IGNORECASE)
            return company[:100]  # Max 100 chars

        # If no match, return None (will extract with spaCy later)
        return None

    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location from job post"""
        # Remove HTML tags
        text_clean = re.sub(r"<[^>]+>", "", text)

        # Common patterns: "Location: X", "| X |", "REMOTE", "ONSITE"
        remote_pattern = r"\b(REMOTE|Remote|remote|Work from home|WFH)\b"
        if re.search(remote_pattern, text_clean):
            return "Remote"

        # Try to find location patterns
        location_pattern = r"(?:Location:|based in|office in)\s*([A-Z][a-zA-Z\s,]+)"
        match = re.search(location_pattern, text_clean)
        if match:
            return match.group(1).strip()[:100]

        return None

    def _determine_category(self, keywords: List[str]) -> str:
        """Determine job category based on matched keywords"""
        # Map keywords back to categories
        for category, category_keywords in HIRING_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in [k.lower() for k in category_keywords]:
                    return category

        return "SaaS Security"  # Default

    def scrape(self, months_back: int = 2, max_threads: int = 3) -> List[Dict]:
        """
        Main scraping method

        Args:
            months_back: How many months back to search
            max_threads: Maximum number of threads to scrape

        Returns:
            List of job postings
        """
        print("\n" + "=" * 70)
        print("🚀 Starting HackerNews Hiring Scraper")
        print("=" * 70 + "\n")

        # Step 1: Find recent hiring threads
        threads = self.search_hiring_threads(months_back)

        if not threads:
            print("❌ No hiring threads found")
            return []

        # Step 2: Get comments from top threads
        all_jobs = []
        for thread in threads[:max_threads]:
            print(f"\n📍 Processing: {thread['title']}")
            print(f"   Date: {thread['created_at'].strftime('%Y-%m-%d')}")
            print(f"   Comments: {thread['num_comments']}")

            comments = self.get_thread_comments(thread["story_id"])

            # Step 3: Filter for relevant posts
            relevant_comments = self.filter_relevant_comments(comments)

            # Step 4: Extract structured data
            for comment in relevant_comments:
                job_info = self.extract_job_info(comment)
                all_jobs.append(job_info)

        print("\n" + "=" * 70)
        print(f"✅ Scraping complete! Found {len(all_jobs)} SaaS security job posts")
        print("=" * 70 + "\n")

        return all_jobs


def main():
    """Test the scraper"""
    scraper = HackerNewsHiringScraper()

    # Scrape recent threads
    jobs = scraper.scrape(months_back=2, max_threads=2)

    # Display results
    print("\n📊 RESULTS PREVIEW:")
    print("-" * 70)
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job.get('company_name', 'Unknown Company')}")
        print(f"   Category: {job['job_category']}")
        print(f"   Keywords: {', '.join(job['matched_keywords'][:3])}")
        print(f"   Location: {job.get('location', 'Not specified')}")
        print(f"   Posted: {job['posted_date'].strftime('%Y-%m-%d')}")
        print(f"   URL: {job['source_url']}")

    if len(jobs) > 5:
        print(f"\n... and {len(jobs) - 5} more jobs")

    return jobs


if __name__ == "__main__":
    jobs = main()
