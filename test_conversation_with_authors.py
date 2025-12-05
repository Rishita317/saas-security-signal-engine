"""
Test conversation signals with author extraction on localhost
This will scrape a few articles and show the author extraction in action
"""

import sys
import os
sys.path.append('.')

from scrapers.company_discovery_v3 import CompanyDiscoveryV3
import pandas as pd
from datetime import datetime

print("=" * 80)
print("TESTING CONVERSATION SIGNALS WITH AUTHOR EXTRACTION")
print("=" * 80)
print("\nThis will:")
print("1. Scrape 10 security articles from top publishers")
print("2. Extract author from each article URL")
print("3. Display results in a table")
print("4. Save to a test CSV file")
print("\n" + "=" * 80)

# Initialize the engine
engine = CompanyDiscoveryV3()

# Run conversation signal discovery (10 posts for quick testing)
print("\n🚀 Starting scraping...")
engine._discover_conversation_signals(target_posts=10)

# Collect conversation details
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

# Create DataFrame
if conversation_details:
    df = pd.DataFrame(conversation_details)

    print("\n" + "=" * 80)
    print("RESULTS - CONVERSATION SIGNALS WITH AUTHORS")
    print("=" * 80)

    # Display each row nicely
    for idx, row in df.iterrows():
        print(f"\n📄 Article #{idx + 1}")
        print(f"   Publisher: {row['publisher']}")
        print(f"   Title: {row['title'][:70]}...")
        print(f"   👤 Author: {row['author']}")
        print(f"   URL: {row['url'][:60]}...")
        print(f"   Published: {row['published_at']}")

    # Save to test CSV
    test_file = "test_conversation_with_authors.csv"
    df.to_csv(test_file, index=False)

    print("\n" + "=" * 80)
    print(f"✅ SUCCESS!")
    print("=" * 80)
    print(f"Total articles scraped: {len(df)}")
    print(f"Authors found: {len(df[df['author'] != 'Unknown'])}")
    print(f"Unknown authors: {len(df[df['author'] == 'Unknown'])}")
    print(f"\n💾 Saved to: {test_file}")

    # Show CSV preview
    print("\n" + "=" * 80)
    print("CSV PREVIEW (First 3 rows):")
    print("=" * 80)
    print(df.head(3).to_string(index=False))

    print("\n" + "=" * 80)
    print(f"🔍 To view the full CSV, run:")
    print(f"   cat {test_file}")
    print("=" * 80)

else:
    print("\n❌ No conversation signals found. Check your internet connection.")
