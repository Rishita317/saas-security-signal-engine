"""
Weekly Automation Orchestrator - Company-Centric GTM Intelligence

Uses CompanyDiscoveryV3 for real, comprehensive data collection
Runs every Monday at 8 AM UTC via GitHub Actions
"""

import os
import sys
from datetime import datetime
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.company_discovery_v3 import CompanyDiscoveryV3


def main():
    """Run weekly data refresh"""

    print("=" * 70)
    print(f"🚀 WEEKLY REFRESH - Week {datetime.now().strftime('%Y_W%U')}")
    print("=" * 70)
    print("Company-Centric GTM Intelligence for SaaS Security")
    print("=" * 70)

    # Initialize V3 discovery engine
    engine = CompanyDiscoveryV3()

    # Run all data sources (with error handling to ensure pipeline completes)
    print("\n1️⃣ Running Indeed scraping...")
    try:
        engine._scrape_indeed(max_companies=400)
    except Exception as e:
        print(f"   ⚠️  Indeed scraping failed: {str(e)[:100]}")
        print("   ℹ️  Continuing with other sources...")

    print("\n2️⃣ Running VC Portfolio scraping (25+ VCs)...")
    try:
        engine._scrape_vc_portfolios(max_companies=600)
    except Exception as e:
        print(f"   ⚠️  VC scraping failed: {str(e)[:100]}")
        print("   ℹ️  Continuing with other sources...")

    print("\n3️⃣ Running Security Job Boards...")
    try:
        engine._scrape_security_job_boards(max_companies=50)
    except Exception as e:
        print(f"   ⚠️  Job boards failed: {str(e)[:100]}")
        print("   ℹ️  Continuing with other sources...")

    print("\n4️⃣ Running Direct ATS Discovery...")
    try:
        engine._scrape_greenhouse_direct(max_companies=20)
        engine._scrape_lever_direct(max_companies=20)
        engine._scrape_workday_direct(max_companies=20)
    except Exception as e:
        print(f"   ⚠️  ATS scraping failed: {str(e)[:100]}")
        print("   ℹ️  Continuing with other sources...")

    print("\n5️⃣ Running Conversation Signal Discovery...")
    try:
        engine._discover_conversation_signals(target_posts=30)
    except Exception as e:
        print(f"   ⚠️  Conversation signals failed: {str(e)[:100]}")
        print("   ℹ️  Pipeline will still save data collected so far...")

    # Generate and save data
    print("\n📊 Generating output files...")
    tracker = engine._generate_company_tracker()

    # Create output directory
    week_id = datetime.now().strftime('%Y_W%U')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    week_dir = f"data/weekly/{week_id}"
    os.makedirs(week_dir, exist_ok=True)

    # Save company tracker
    tracker_df = pd.DataFrame(tracker)
    tracker_file = f"{week_dir}/company_tracker_{timestamp}.csv"
    tracker_df.to_csv(tracker_file, index=False)
    print(f"   💾 Saved: {tracker_file}")

    # Save hiring details
    hiring_details = []
    for company_name, data in engine.companies.items():
        for job in data['hiring']:
            hiring_details.append({
                'company_name': company_name,
                'title': job.get('title', ''),
                'url': job.get('url', ''),
                'location': job.get('location', ''),
                'source': job.get('source', ''),
                'posted_date': job.get('posted_date', '')
            })

    if hiring_details:
        hiring_df = pd.DataFrame(hiring_details)
        hiring_file = f"{week_dir}/hiring_details_{timestamp}.csv"
        hiring_df.to_csv(hiring_file, index=False)
        print(f"   💾 Saved: {hiring_file}")

    # Save conversation details
    conversation_details = []
    for company_name, data in engine.companies.items():
        for post in data['conversations']:
            conversation_details.append({
                'publisher': company_name,
                'title': post.get('title', ''),
                'author': post.get('author', 'Unknown'),
                'url': post.get('url', ''),
                'published_at': post.get('published_at', ''),
                'source': post.get('source', '')
            })

    if conversation_details:
        conv_df = pd.DataFrame(conversation_details)
        conv_file = f"{week_dir}/conversation_details_{timestamp}.csv"
        conv_df.to_csv(conv_file, index=False)
        print(f"   💾 Saved: {conv_file}")

    print(f"\n✅ Weekly refresh complete!")
    print(f"   Total companies: {len(tracker)}")
    print(f"   High priority (both signals): {len([c for c in tracker if c['activity_type'] == 'both'])}")
    print(f"   Hiring only: {len([c for c in tracker if c['activity_type'] == 'hiring_only'])}")
    print(f"   Talking only: {len([c for c in tracker if c['activity_type'] == 'talking_only'])}")


if __name__ == "__main__":
    main()
