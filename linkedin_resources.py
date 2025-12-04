"""
LinkedIn Resources - BONUS FEATURE (ISOLATED)

⚠️ IMPORTANT: This file is completely separate from the main scraping pipeline.
It does NOT scrape LinkedIn directly (TOS compliance).
It provides:
  1. Curated LinkedIn search URLs (dynamic, user-clicks to refresh)
  2. Optional CSV ingestion for manually exported LinkedIn data

This module NEVER touches:
  - scrapers/company_discovery_v3.py
  - orchestration/weekly_refresh_v2.py
  - Any existing data sources
"""

import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# CURATED LINKEDIN SEARCH URLS (User-Driven, No Scraping)
# ============================================================================

LINKEDIN_JOB_SEARCHES = {
    "SaaS Security Jobs (Last 7 Days)": "https://www.linkedin.com/jobs/search-results/?currentJobId=4311225585&keywords=Sass%20security%20jobs&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&referralSearchId=K2VSj42Y7CK3eEhKi4oclw%3D%3D&geoId=103644278&f_TPR=r604800",

    "SSPM Roles (Last Week)": "https://www.linkedin.com/jobs/search-results/?keywords=Sass+security+posture+management+jobs+&origin=JOB_SEARCH_PAGE_JOB_FILTER&referralSearchId=PY2OaqFnLCo66OuhvEnZpA%3D%3D&f_TPR=r604800",

    "Cloud / AppSec Security Roles": "https://www.linkedin.com/jobs/search-results/?currentJobId=4333092158&keywords=Cloud%20%2F%20AppSec%20security%20roles&origin=JOB_SEARCH_PAGE_JOB_FILTER&referralSearchId=%2BSeao7hqPibH2E8xu%2B2Ieg%3D%3D&f_TPR=r604800",

    "AI/LLM Security Roles": "https://www.linkedin.com/jobs/search-results/?keywords=AI%20security%20roles%20posted%20in%20the%20past%20week&origin=JOB_SEARCH_PAGE_JOB_FILTER&referralSearchId=5GtzIe9GUEcU5lodGQnK%2FQ%3D%3D&f_TPR=r604800",

    "Identity/IAM Security Roles": "https://www.linkedin.com/jobs/search-results/?keywords=Identity%2FIAM+security+roles+past+week&origin=JOB_SEARCH_PAGE_JOB_FILTER&referralSearchId=6gNrEkuXhu7LIEn22jEQXw%3D%3D&f_TPR=r604800",

    "DevSecOps Roles (Last Week)": "https://www.linkedin.com/jobs/search-results/?keywords=DevSecOps&f_TPR=r604800&origin=JOB_SEARCH_PAGE_JOB_FILTER",

    "Security Engineering Internships": "https://www.linkedin.com/jobs/search-results/?keywords=Security%20Engineering%20Intern&f_TPR=r604800&origin=JOB_SEARCH_PAGE_JOB_FILTER",

    "SOC Analyst Roles": "https://www.linkedin.com/jobs/search-results/?keywords=SOC%20Analyst&f_TPR=r604800&origin=JOB_SEARCH_PAGE_JOB_FILTER",
}

LINKEDIN_CONTENT_SEARCHES = {
    "SaaS Security Posts (Last Week)": "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Sass%20security&origin=FACETED_SEARCH&sid=5iC",

    "Cloud Security Discussions": "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Cloud%20Security&origin=FACETED_SEARCH",

    "SSPM Thought Leadership": "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=SSPM&origin=FACETED_SEARCH",

    "Zero Trust Architecture": "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Zero%20Trust&origin=FACETED_SEARCH",

    "AI Security Trends": "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=AI%20Security&origin=FACETED_SEARCH",
}

# ============================================================================
# OPTIONAL CSV INGESTION (Semi-Manual User Input)
# ============================================================================

def ingest_linkedin_csv(csv_path: str = "inputs/linkedin_jobs.csv") -> Optional[pd.DataFrame]:
    """
    OPTIONAL: Ingest manually exported LinkedIn jobs CSV

    This function:
      - Only runs if linkedin_jobs.csv exists
      - Parses user-provided LinkedIn export data
      - Classifies relevance for SaaS/Security roles
      - Returns DataFrame ready to append to existing dataset

    ⚠️ IMPORTANT: This does NOT touch existing scrapers or data sources.
    It's a completely separate, optional bonus feature.

    CSV Format Expected:
      - company_name (required)
      - title (required)
      - url (optional)
      - location (optional)
      - posted_date (optional)

    Args:
        csv_path: Path to manually exported LinkedIn CSV

    Returns:
        DataFrame with parsed LinkedIn jobs, or None if file doesn't exist
    """

    if not os.path.exists(csv_path):
        print(f"ℹ️  No LinkedIn CSV found at {csv_path} (this is optional)")
        return None

    print(f"📂 Loading LinkedIn CSV from {csv_path}...")

    try:
        # Load CSV
        df = pd.read_csv(csv_path)

        # Validate required columns
        required_cols = ['company_name', 'title']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            print(f"⚠️  Missing required columns: {missing_cols}")
            print(f"   Expected columns: {required_cols}")
            return None

        # Add source column
        df['source'] = 'LinkedIn (Manual)'

        # Add ingestion timestamp
        df['ingested_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Filter for relevant security roles
        security_keywords = [
            'security', 'cybersecurity', 'infosec', 'sspm', 'appsec',
            'devsecops', 'soc', 'iam', 'cloud security', 'threat',
            'compliance', 'risk', 'privacy'
        ]

        df['is_relevant'] = df['title'].str.lower().apply(
            lambda title: any(keyword in title for keyword in security_keywords)
        )

        relevant_df = df[df['is_relevant']].copy()
        relevant_df = relevant_df.drop(columns=['is_relevant'])

        print(f"✅ Loaded {len(df)} LinkedIn jobs")
        print(f"   Relevant security roles: {len(relevant_df)}")
        print(f"   Unique companies: {relevant_df['company_name'].nunique()}")

        return relevant_df

    except Exception as e:
        print(f"⚠️  Error loading LinkedIn CSV: {str(e)}")
        return None


def merge_linkedin_with_existing(linkedin_df: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    """
    OPTIONAL: Merge LinkedIn data with existing hiring details

    This function:
      - Appends LinkedIn jobs to existing dataset
      - Deduplicates based on company_name + title
      - Preserves all existing data without modification

    Args:
        linkedin_df: DataFrame from ingest_linkedin_csv()
        existing_df: Existing hiring_details.csv

    Returns:
        Combined DataFrame (existing data + LinkedIn data)
    """

    if linkedin_df is None or linkedin_df.empty:
        return existing_df

    print("🔄 Merging LinkedIn data with existing dataset...")

    # Ensure consistent column structure
    common_cols = ['company_name', 'title', 'url', 'location', 'source', 'posted_date']

    # Add missing columns with defaults
    for col in common_cols:
        if col not in linkedin_df.columns:
            linkedin_df[col] = 'N/A'
        if col not in existing_df.columns:
            existing_df[col] = 'N/A'

    # Combine datasets
    combined_df = pd.concat([existing_df, linkedin_df], ignore_index=True)

    # Deduplicate (keep first occurrence)
    combined_df = combined_df.drop_duplicates(subset=['company_name', 'title'], keep='first')

    print(f"✅ Combined dataset: {len(combined_df)} total jobs")
    print(f"   Original: {len(existing_df)}")
    print(f"   Added from LinkedIn: {len(combined_df) - len(existing_df)}")

    return combined_df


def get_linkedin_stats(linkedin_df: Optional[pd.DataFrame]) -> Dict:
    """
    Get statistics about LinkedIn data (for dashboard display)

    Returns:
        Dictionary with LinkedIn metrics
    """

    if linkedin_df is None or linkedin_df.empty:
        return {
            'total_jobs': 0,
            'unique_companies': 0,
            'status': 'No LinkedIn data loaded'
        }

    return {
        'total_jobs': len(linkedin_df),
        'unique_companies': linkedin_df['company_name'].nunique(),
        'status': 'LinkedIn data loaded successfully',
        'top_companies': linkedin_df['company_name'].value_counts().head(5).to_dict()
    }


# ============================================================================
# USAGE INSTRUCTIONS (For Users)
# ============================================================================

USAGE_INSTRUCTIONS = """
## How to Use LinkedIn Resources (Optional Bonus Feature)

### Option 1: Use Dynamic Search Links
1. Click any LinkedIn search link in the dashboard
2. LinkedIn will show you fresh results (auto-refreshes each time)
3. Manually review and apply to relevant positions

### Option 2: Export LinkedIn Data (Semi-Manual)
1. Go to LinkedIn and run your searches (use provided links)
2. Export results to CSV using LinkedIn's export feature or copy-paste to Google Sheets
3. Save as: `inputs/linkedin_jobs.csv`
4. Format CSV with columns: `company_name`, `title`, `url`, `location`, `posted_date`
5. Re-run the dashboard - LinkedIn data will auto-merge with existing data

### CSV Template Example:
```csv
company_name,title,url,location,posted_date
CrowdStrike,Senior Security Engineer,https://linkedin.com/jobs/...,Austin TX,2025-12-04
Palo Alto Networks,Cloud Security Architect,https://linkedin.com/jobs/...,Remote,2025-12-03
```

⚠️ **Note**: This feature is completely optional and does NOT affect your existing
job board scraping pipeline. All LinkedIn data is treated as a separate bonus source.
"""

if __name__ == "__main__":
    print("=" * 70)
    print("LinkedIn Resources - Isolated Bonus Feature")
    print("=" * 70)
    print("\n📋 Available LinkedIn Job Searches:")
    for name, url in LINKEDIN_JOB_SEARCHES.items():
        print(f"   • {name}")

    print("\n💬 Available LinkedIn Content Searches:")
    for name, url in LINKEDIN_CONTENT_SEARCHES.items():
        print(f"   • {name}")

    print(f"\n{USAGE_INSTRUCTIONS}")

    # Test CSV ingestion (optional)
    linkedin_data = ingest_linkedin_csv()
    if linkedin_data is not None:
        stats = get_linkedin_stats(linkedin_data)
        print(f"\n📊 LinkedIn Data Stats:")
        print(f"   Total Jobs: {stats['total_jobs']}")
        print(f"   Unique Companies: {stats['unique_companies']}")
