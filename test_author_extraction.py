"""
Quick test to verify author extraction from conversation signals
"""

import sys
sys.path.append('.')

from scrapers.company_discovery_v3 import CompanyDiscoveryV3

# Test the author extraction method
engine = CompanyDiscoveryV3()

# Test URLs
test_urls = [
    "https://www.paloaltonetworks.com/blog/2025/12/unit-42-incident-response-retainer-for-aws/",
    "https://www.crowdstrike.com/blog/",
    "https://www.checkpoint.com/blog/"
]

print("=" * 70)
print("Testing Author Extraction")
print("=" * 70)

for url in test_urls:
    print(f"\n🔍 Testing: {url}")
    author = engine._extract_author_from_url(url)
    print(f"👤 Author: {author}")

print("\n" + "=" * 70)
print("Now testing full conversation signal discovery (5 posts)...")
print("=" * 70)

# Test the full pipeline with a small number
engine._discover_conversation_signals(target_posts=5)

# Print results
print("\n" + "=" * 70)
print("RESULTS:")
print("=" * 70)

for company, data in engine.companies.items():
    if data['conversations']:
        print(f"\n{company}:")
        for post in data['conversations']:
            print(f"  📄 {post['title'][:60]}")
            print(f"  👤 Author: {post['author']}")
            print(f"  🔗 URL: {post['url'][:60]}...")
            print()
