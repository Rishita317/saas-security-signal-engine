"""
Quick test to generate conversation data with dynamic author extraction
"""

import sys
sys.path.append('.')

from scrapers.company_discovery_v3 import CompanyDiscoveryV3
import pandas as pd
from datetime import datetime
import os

print('🚀 Generating fresh conversation data with authors...')
print('=' * 70)

# Initialize engine
engine = CompanyDiscoveryV3()

# Scrape 20 posts to get good author coverage
print('📡 Scraping 20 posts from top security publishers...')
engine._discover_conversation_signals(target_posts=20)

# Collect conversation details with authors
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
    df = pd.DataFrame(conversation_details)

    # Save to data folder
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = 'data/weekly/2025_W49'
    os.makedirs(output_dir, exist_ok=True)

    output_file = f'{output_dir}/conversation_details_{timestamp}.csv'
    df.to_csv(output_file, index=False)

    print('\n✅ SUCCESS!')
    print(f'💾 Saved: {output_file}')
    print(f'📊 Total posts: {len(df)}')

    # Calculate stats
    with_authors = len(df[df['author'] != 'Unknown'])
    without_authors = len(df[df['author'] == 'Unknown'])

    print(f'👤 Posts with authors: {with_authors}')
    print(f'❓ Posts without authors: {without_authors}')

    print('\n📋 Sample data:')
    print(df[['publisher', 'author', 'title']].head(10).to_string(index=False))
else:
    print('❌ No conversation data collected')
