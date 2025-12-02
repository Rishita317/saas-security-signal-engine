"""
Job Classification Module with Google Gemini Support

Uses Google Gemini (FREE) or GPT-4 Mini to:
1. Score relevance to SaaS security (0.0 to 1.0)
2. Categorize jobs (SSPM, SaaS Security, AI Agent Security, etc.)
3. Validate extracted company names

This is the "intelligence layer" that filters signal from noise.
"""

import os
import json
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.keywords import HIRING_KEYWORDS, MIN_RELEVANCE_SCORE

# Load environment variables
load_dotenv()


class JobClassifier:
    """Classify job postings using Google Gemini or GPT-4 Mini"""

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
        self.categories = list(HIRING_KEYWORDS.keys())

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
        print("   Add GOOGLE_API_KEY or OPENAI_API_KEY to .env for real classification")
        self.use_mock = True

    def classify_job(self, job_data: Dict) -> Dict:
        """
        Classify a single job posting

        Args:
            job_data: Job dictionary with company_name, job_title, raw_text

        Returns:
            Enhanced job_data with relevance_score and validated category
        """
        if self.use_mock:
            return self._mock_classify(job_data)

        # Build classification prompt
        prompt = self._build_classification_prompt(job_data)

        try:
            if self.provider == "gemini":
                result = self._classify_with_gemini(prompt)
            else:  # openai
                result = self._classify_with_openai(prompt)

            # Update job data
            job_data["relevance_score"] = float(result.get("relevance_score", 0.5))
            job_data["job_category"] = result.get("category", job_data.get("job_category", "SaaS Security"))
            job_data["classification_confidence"] = result.get("confidence", "medium")

            # Validate company name if provided
            if "validated_company" in result and result["validated_company"]:
                job_data["company_name"] = result["validated_company"]

        except Exception as e:
            error_msg = str(e)
            # Check if it's a quota/rate limit error
            if "429" in error_msg or "quota" in error_msg.lower() or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"⚠️  API quota exhausted. Falling back to mock classification.")
                # Switch to mock mode for remaining jobs
                self.use_mock = True
                return self._mock_classify(job_data)
            else:
                print(f"⚠️  Classification error: {e}")
                # Fall back to default scoring
                job_data["relevance_score"] = 0.7
                job_data["classification_confidence"] = "low"

        return job_data

    def _classify_with_gemini(self, prompt: str) -> Dict:
        """Classify using Google Gemini"""
        response = self.client.generate_content(prompt)
        text = response.text

        # Extract JSON from response (Gemini sometimes adds markdown)
        json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        # Fallback: try parsing the whole response
        return json.loads(text)

    def _classify_with_openai(self, prompt: str) -> Dict:
        """Classify using OpenAI GPT-4 Mini"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in cybersecurity job classification, specializing in SaaS security, SSPM, and compliance roles.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=150,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    def _build_classification_prompt(self, job_data: Dict) -> str:
        """Build prompt for AI classification"""
        company = job_data.get("company_name", "Unknown")
        title = job_data.get("job_title", "Unknown")
        text = job_data.get("raw_text", "")[:500]
        keywords = ", ".join(job_data.get("matched_keywords", []))

        prompt = f"""Analyze this job posting for relevance to SaaS Security:

Company: {company}
Job Title: {title}
Matched Keywords: {keywords}
Description: {text}

Evaluate:
1. Relevance score (0.0 to 1.0) - How relevant is this to SaaS security, SSPM, SaaS compliance, or AI agent security?
2. Best category: {', '.join(self.categories)}
3. Confidence level: high, medium, or low

Return ONLY valid JSON with this exact structure (no markdown):
{{
    "relevance_score": 0.85,
    "category": "SSPM",
    "confidence": "high",
    "validated_company": "{company}"
}}

Scoring guide:
- 0.9-1.0: Directly related to SaaS security/SSPM/compliance
- 0.7-0.9: Cloud/app security with SaaS components
- 0.5-0.7: General security role at a SaaS company
- 0.3-0.5: Tangentially related
- 0.0-0.3: Not relevant"""

        return prompt

    def _mock_classify(self, job_data: Dict) -> Dict:
        """Mock classification (for testing without API key)"""
        matched_keywords = job_data.get("matched_keywords", [])
        category = job_data.get("job_category", "SaaS Security")

        # Base score on number of keyword matches
        if len(matched_keywords) >= 3:
            score = 0.9
        elif len(matched_keywords) >= 2:
            score = 0.8
        elif len(matched_keywords) >= 1:
            score = 0.7
        else:
            score = 0.6

        # Boost for high-value categories
        if category in ["SSPM", "AI Agent Security"]:
            score = min(1.0, score + 0.1)

        job_data["relevance_score"] = score
        job_data["classification_confidence"] = "mock"

        return job_data

    def batch_classify(self, jobs: List[Dict], batch_size: int = 10) -> List[Dict]:
        """Classify multiple jobs"""
        provider_name = "Mock" if self.use_mock else ("Google Gemini" if self.provider == "gemini" else "GPT-4 Mini")
        print(f"\n🤖 Classifying {len(jobs)} jobs with {provider_name}...")

        classified_jobs = []
        for i, job in enumerate(jobs):
            try:
                classified_job = self.classify_job(job)
                classified_jobs.append(classified_job)

                if (i + 1) % batch_size == 0:
                    print(f"   Processed {i + 1}/{len(jobs)} jobs...")

            except Exception as e:
                print(f"⚠️  Error classifying job {i}: {e}")
                job["relevance_score"] = 0.5
                classified_jobs.append(job)

        print(f"✅ Classification complete!\n")
        return classified_jobs

    def filter_by_relevance(self, jobs: List[Dict], min_score: Optional[float] = None) -> List[Dict]:
        """Filter jobs by relevance score"""
        min_score = min_score or MIN_RELEVANCE_SCORE
        filtered = [j for j in jobs if j.get("relevance_score", 0) >= min_score]

        print(f"🔍 Filtered: {len(filtered)}/{len(jobs)} jobs above {min_score} relevance score")
        return filtered

    def get_classification_stats(self, jobs: List[Dict]) -> Dict:
        """Get statistics about classified jobs"""
        if not jobs:
            return {}

        relevance_scores = [j.get("relevance_score", 0) for j in jobs]

        stats = {
            "total_jobs": len(jobs),
            "avg_relevance": sum(relevance_scores) / len(relevance_scores),
            "high_relevance": sum(1 for score in relevance_scores if score >= 0.8),
            "medium_relevance": sum(1 for score in relevance_scores if 0.6 <= score < 0.8),
            "low_relevance": sum(1 for score in relevance_scores if score < 0.6),
            "by_category": {},
        }

        for job in jobs:
            category = job.get("job_category", "Unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        return stats


def main():
    """Test classification with demo data"""
    from scrapers.demo_data import get_mock_hackernews_jobs
    from processors.entity_extraction import EntityExtractor

    print("=" * 70)
    print("🧪 Testing Job Classification with Google Gemini")
    print("=" * 70 + "\n")

    # Get mock data and extract entities
    jobs = get_mock_hackernews_jobs()[:15]
    extractor = EntityExtractor()
    jobs = extractor.batch_extract(jobs)

    # Initialize classifier (will try Gemini first)
    classifier = JobClassifier()

    # Classify jobs
    classified_jobs = classifier.batch_classify(jobs)

    # Filter by relevance
    relevant_jobs = classifier.filter_by_relevance(classified_jobs)

    # Show results
    print("\n📊 CLASSIFICATION RESULTS:")
    print("-" * 70)

    for i, job in enumerate(relevant_jobs[:5], 1):
        print(f"\n{i}. {job.get('company_name', 'Unknown')}")
        print(f"   Title: {job.get('job_title', 'Not specified')}")
        print(f"   Category: {job.get('job_category')}")
        print(f"   Relevance Score: {job.get('relevance_score', 0):.2f}")
        print(f"   Confidence: {job.get('classification_confidence', 'N/A')}")
        print(f"   Keywords: {', '.join(job.get('matched_keywords', [])[:3])}")

    # Show stats
    print("\n" + "=" * 70)
    stats = classifier.get_classification_stats(classified_jobs)
    print("📈 CLASSIFICATION STATISTICS:")
    print(f"   Total jobs: {stats['total_jobs']}")
    print(f"   Average relevance: {stats['avg_relevance']:.2f}")
    print(f"   High relevance (≥0.8): {stats['high_relevance']}")
    print(f"   Medium relevance (0.6-0.8): {stats['medium_relevance']}")
    print(f"   Low relevance (<0.6): {stats['low_relevance']}")
    print(f"\n   By category:")
    for category, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
        print(f"      {category}: {count}")
    print("=" * 70)

    return relevant_jobs


if __name__ == "__main__":
    jobs = main()
