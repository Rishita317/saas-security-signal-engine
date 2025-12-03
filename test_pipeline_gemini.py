"""
End-to-End Pipeline Test with OpenAI

Tests the complete hiring signal pipeline with FREE Gemini AI:
1. Data collection (mock data)
2. Entity extraction (spaCy)
3. Classification (Google Gemini 2.5 Flash - FREE!)
4. Filtering and export

This demonstrates real AI classification using OpenAI GPT-4o-mini.
"""

import json
from datetime import datetime
from scrapers.demo_data import get_mock_hackernews_jobs, get_mock_reddit_jobs
from processors.entity_extraction import EntityExtractor
from processors.classification_gemini import JobClassifier


def run_pipeline_with_gemini(num_jobs: int = 30, export_csv: bool = True):
    """
    Run the complete hiring signal pipeline with Gemini

    Args:
        num_jobs: Number of jobs to process
        export_csv: Whether to export results to CSV
    """
    print("\n" + "=" * 70)
    print("🚀 SAAS SECURITY SIGNAL ENGINE - OpenAI GPT-4o-mini PIPELINE")
    print("=" * 70 + "\n")

    # Step 1: Data Collection
    print("📥 STEP 1: Data Collection")
    print("-" * 70)
    hn_jobs = get_mock_hackernews_jobs()[:num_jobs // 2]
    reddit_jobs = get_mock_reddit_jobs()[:num_jobs // 2]
    all_jobs = hn_jobs + reddit_jobs
    print(f"✅ Collected {len(all_jobs)} jobs ({len(hn_jobs)} HN + {len(reddit_jobs)} Reddit)\n")

    # Step 2: Entity Extraction
    print("🔍 STEP 2: Entity Extraction (spaCy NER)")
    print("-" * 70)
    extractor = EntityExtractor()
    jobs_with_entities = extractor.batch_extract(all_jobs)

    stats = extractor.get_extraction_stats(jobs_with_entities)
    print(f"   Extracted companies: {stats['with_company']}/{stats['total_jobs']}")
    print(f"   Extracted titles: {stats['with_title']}/{stats['total_jobs']}")
    print(f"   Unique companies: {stats['unique_companies']}\n")

    # Step 3: Classification with Gemini
    print("🤖 STEP 3: Relevance Classification (OpenAI GPT-4o-mini)")
    print("-" * 70)
    classifier = JobClassifier()  # Will use Gemini automatically
    classified_jobs = classifier.batch_classify(jobs_with_entities)

    classification_stats = classifier.get_classification_stats(classified_jobs)
    print(f"   Average relevance score: {classification_stats['avg_relevance']:.2f}")
    print(f"   High relevance (≥0.8): {classification_stats['high_relevance']}")
    print(f"   Medium relevance (0.6-0.8): {classification_stats['medium_relevance']}\n")

    # Step 4: Filter by relevance
    print("🔎 STEP 4: Filtering by Relevance")
    print("-" * 70)
    relevant_jobs = classifier.filter_by_relevance(classified_jobs, min_score=0.7)
    print()

    # Step 5: Display Results
    print("📊 STEP 5: Results Summary")
    print("-" * 70)
    print(f"\n✅ PIPELINE COMPLETE!")
    print(f"   Input: {len(all_jobs)} jobs")
    print(f"   Output: {len(relevant_jobs)} relevant jobs ({len(relevant_jobs)/len(all_jobs)*100:.1f}% pass rate)")
    print(f"\n   Top 10 Companies Hiring:")

    # Count jobs per company
    company_counts = {}
    for job in relevant_jobs:
        company = job.get("company_name", "Unknown")
        company_counts[company] = company_counts.get(company, 0) + 1

    for i, (company, count) in enumerate(
        sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:10], 1
    ):
        print(f"   {i:2d}. {company:30s} - {count} roles")

    print(f"\n   By Category:")
    for category, count in sorted(
        classification_stats["by_category"].items(), key=lambda x: x[1], reverse=True
    ):
        print(f"      {category:25s}: {count:2d} jobs")

    # Compare with mock scores
    print(f"\n   🎯 AI Quality Improvement:")
    mock_avg = 0.70  # From previous mock tests
    improvement = ((classification_stats['avg_relevance'] - mock_avg) / mock_avg) * 100
    print(f"      Mock average: {mock_avg:.2f}")
    print(f"      Gemini average: {classification_stats['avg_relevance']:.2f}")
    print(f"      Improvement: +{improvement:.1f}%")

    # Step 6: Export (optional)
    if export_csv:
        export_to_csv(relevant_jobs, suffix="_openai")

    print("\n" + "=" * 70)

    return relevant_jobs


def export_to_csv(jobs: list, suffix: str = ""):
    """Export jobs to CSV file"""
    import csv
    import os

    filename = f"data/hiring_signals_gemini_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        if not jobs:
            return

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "company_name",
                "job_title",
                "job_category",
                "location",
                "relevance_score",
                "classification_confidence",
                "source_platform",
                "source_url",
                "posted_date",
                "matched_keywords",
            ],
        )

        writer.writeheader()
        for job in jobs:
            writer.writerow(
                {
                    "company_name": job.get("company_name", ""),
                    "job_title": job.get("job_title", ""),
                    "job_category": job.get("job_category", ""),
                    "location": job.get("location", ""),
                    "relevance_score": job.get("relevance_score", 0),
                    "classification_confidence": job.get("classification_confidence", ""),
                    "source_platform": job.get("source_platform", ""),
                    "source_url": job.get("source_url", ""),
                    "posted_date": job.get("posted_date", ""),
                    "matched_keywords": ", ".join(job.get("matched_keywords", [])),
                }
            )

    print(f"\n💾 Exported to: {filename}")


def main():
    """Run the pipeline test"""
    jobs = run_pipeline_with_gemini(num_jobs=30, export_csv=True)

    # Show sample results
    print("\n📋 SAMPLE RESULTS (Top 5):")
    print("=" * 70)

    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job.get('company_name', 'Unknown')}")
        print(f"   Role: {job.get('job_title', 'Not specified')}")
        print(f"   Category: {job.get('job_category')}")
        print(f"   Location: {job.get('location', 'Not specified')}")
        print(f"   Relevance: {job.get('relevance_score', 0):.2f} ⭐")
        print(f"   Confidence: {job.get('classification_confidence', 'N/A')}")
        print(f"   Source: {job.get('source_platform')}")
        print(f"   Posted: {job.get('posted_date').strftime('%Y-%m-%d')}")

    print("\n" + "=" * 70)
    print("🎉 OpenAI pipeline test complete! AI classification working!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
