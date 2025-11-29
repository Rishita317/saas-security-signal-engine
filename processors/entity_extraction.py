"""
Entity Extraction Module

Uses spaCy NLP to extract:
- Company names (ORG entities)
- Job titles (using patterns)
- Locations (GPE entities)

This enriches scraped job posts with structured data.
"""

import spacy
import re
from typing import Dict, List, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.keywords import JOB_TITLE_PATTERNS


class EntityExtractor:
    """Extract structured entities from job post text using spaCy NLP"""

    def __init__(self):
        print("🧠 Loading spaCy model...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model loaded successfully")
        except OSError:
            print("❌ spaCy model not found. Run: python -m spacy download en_core_web_sm")
            raise

        # Company name cleaning patterns
        self.company_suffixes = [
            r"\s+(Inc\.?|LLC|Ltd\.?|Corp\.?|Corporation|Co\.?|Company)$",
            r"\s+\([^)]+\)$",  # Remove parenthetical info
        ]

    def extract_entities(self, job_data: Dict) -> Dict:
        """
        Extract all entities from a job posting

        Args:
            job_data: Dictionary with job information including 'raw_text'

        Returns:
            Enhanced job_data with extracted entities
        """
        text = job_data.get("raw_text", "")

        if not text:
            return job_data

        # Process text with spaCy
        doc = self.nlp(text[:1000])  # Limit to first 1000 chars for performance

        # Extract company if not already present
        if not job_data.get("company_name"):
            company = self.extract_company(doc, text)
            if company:
                job_data["company_name"] = company

        # Extract job title if not specific
        if not job_data.get("job_title") or job_data["job_title"] == "Multiple roles":
            title = self.extract_job_title(text)
            if title:
                job_data["job_title"] = title

        # Extract location if not present
        if not job_data.get("location"):
            location = self.extract_location(doc)
            if location:
                job_data["location"] = location

        # Normalize company name for deduplication
        if job_data.get("company_name"):
            job_data["company_name_normalized"] = self.normalize_company_name(
                job_data["company_name"]
            )

        return job_data

    def extract_company(self, doc, text: str) -> Optional[str]:
        """
        Extract company name from text using spaCy NER

        Args:
            doc: spaCy Doc object
            text: Original text

        Returns:
            Company name or None
        """
        # Look for ORG entities
        org_entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

        if org_entities:
            # Take the first ORG entity (usually the company posting)
            company = org_entities[0]

            # Clean up company name
            company = self.clean_company_name(company)

            # Validate length
            if 2 <= len(company) <= 50:
                return company

        # Fallback: Try to find company at start of text
        match = re.match(r"^([A-Z][A-Za-z0-9\s&\.]{2,40})", text)
        if match:
            company = match.group(1).strip()
            company = self.clean_company_name(company)
            if 2 <= len(company) <= 50:
                return company

        return None

    def clean_company_name(self, company: str) -> str:
        """Clean and normalize company name"""
        # Remove common suffixes
        for pattern in self.company_suffixes:
            company = re.sub(pattern, "", company, flags=re.IGNORECASE)

        # Remove extra whitespace
        company = " ".join(company.split())

        # Remove leading articles
        company = re.sub(r"^(The|A|An)\s+", "", company, flags=re.IGNORECASE)

        return company.strip()

    def normalize_company_name(self, company: str) -> str:
        """
        Normalize company name for deduplication

        Returns lowercase, trimmed version for matching
        """
        normalized = company.lower().strip()

        # Remove common suffixes for better matching
        for pattern in self.company_suffixes:
            normalized = re.sub(pattern, "", normalized, flags=re.IGNORECASE)

        # Remove extra whitespace
        normalized = " ".join(normalized.split())

        return normalized

    def extract_job_title(self, text: str) -> Optional[str]:
        """
        Extract job title using regex patterns

        Args:
            text: Job post text

        Returns:
            Job title or None
        """
        for pattern in JOB_TITLE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(0)
                # Clean up the title
                title = " ".join(title.split())  # Remove extra whitespace
                if len(title) <= 100:
                    return title

        # Additional patterns for common titles
        common_titles = [
            r"(Senior|Staff|Principal|Lead)?\s*(Security|Software|DevOps|Cloud|Application)\s+Engineer",
            r"(Senior|Staff|Principal)?\s*Security\s+Architect",
            r"(Senior|Staff)?\s*(Security|Compliance|GRC)\s+Analyst",
            r"(Senior|Staff|Principal)?\s*Security\s+Researcher",
        ]

        for pattern in common_titles:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)

        return None

    def extract_location(self, doc) -> Optional[str]:
        """
        Extract location using spaCy NER

        Args:
            doc: spaCy Doc object

        Returns:
            Location string or None
        """
        # Look for GPE (Geo-Political Entity) entities
        locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

        if locations:
            # Return first location found
            return locations[0][:100]  # Max 100 chars

        return None

    def batch_extract(self, jobs: List[Dict]) -> List[Dict]:
        """
        Extract entities from multiple jobs efficiently

        Args:
            jobs: List of job dictionaries

        Returns:
            List of enhanced job dictionaries
        """
        print(f"\n🔍 Extracting entities from {len(jobs)} jobs...")

        enhanced_jobs = []
        for i, job in enumerate(jobs):
            try:
                enhanced_job = self.extract_entities(job)
                enhanced_jobs.append(enhanced_job)

                if (i + 1) % 10 == 0:
                    print(f"   Processed {i + 1}/{len(jobs)} jobs...")

            except Exception as e:
                print(f"⚠️  Error processing job {i}: {e}")
                enhanced_jobs.append(job)  # Include original on error

        print(f"✅ Entity extraction complete!\n")
        return enhanced_jobs

    def get_extraction_stats(self, jobs: List[Dict]) -> Dict:
        """Get statistics about extracted entities"""
        stats = {
            "total_jobs": len(jobs),
            "with_company": sum(1 for j in jobs if j.get("company_name")),
            "with_title": sum(1 for j in jobs if j.get("job_title")),
            "with_location": sum(1 for j in jobs if j.get("location")),
            "unique_companies": len(set(j.get("company_name") for j in jobs if j.get("company_name"))),
        }
        return stats


def main():
    """Test entity extraction with demo data"""
    from scrapers.demo_data import get_mock_hackernews_jobs

    print("=" * 70)
    print("🧪 Testing Entity Extraction")
    print("=" * 70 + "\n")

    # Get mock data
    jobs = get_mock_hackernews_jobs()[:10]  # Test with 10 jobs

    # Initialize extractor
    extractor = EntityExtractor()

    # Process jobs
    enhanced_jobs = extractor.batch_extract(jobs)

    # Show results
    print("\n📊 EXTRACTION RESULTS:")
    print("-" * 70)

    for i, job in enumerate(enhanced_jobs[:5], 1):
        print(f"\n{i}. Company: {job.get('company_name', 'Unknown')}")
        print(f"   Title: {job.get('job_title', 'Not specified')}")
        print(f"   Location: {job.get('location', 'Not specified')}")
        print(f"   Category: {job.get('job_category')}")
        print(f"   Normalized: {job.get('company_name_normalized', 'N/A')}")

    # Show stats
    print("\n" + "=" * 70)
    stats = extractor.get_extraction_stats(enhanced_jobs)
    print("📈 EXTRACTION STATISTICS:")
    print(f"   Total jobs: {stats['total_jobs']}")
    print(f"   With company name: {stats['with_company']} ({stats['with_company']/stats['total_jobs']*100:.1f}%)")
    print(f"   With job title: {stats['with_title']} ({stats['with_title']/stats['total_jobs']*100:.1f}%)")
    print(f"   With location: {stats['with_location']} ({stats['with_location']/stats['total_jobs']*100:.1f}%)")
    print(f"   Unique companies: {stats['unique_companies']}")
    print("=" * 70)

    return enhanced_jobs


if __name__ == "__main__":
    jobs = main()
