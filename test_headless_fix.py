#!/usr/bin/env python3
"""
Quick test to verify headless mode fix for Indeed scraping
Tests the company name validation and extraction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.company_discovery_v3 import CompanyDiscoveryV3

def test_company_name_validation():
    """Test the _is_valid_company_name method"""
    engine = CompanyDiscoveryV3()

    print("=" * 70)
    print("🧪 Testing Company Name Validation")
    print("=" * 70)

    # Test cases: (name, should_be_valid)
    test_cases = [
        # INVALID - UI fragments from the bad GitHub Actions run
        ("e account", False),
        ("e an accountto save", False),
        ("ion EngineerYou need tosign inorcreate an accountto", False),
        ("orYou need tosign inorcreate an accountto save", False),
        ("ion Security OfficerYou need tosign inorcreate an a", False),
        ("e accountPOST A JOB--", False),
        ("is Cyber SecurityWhy choose a career in cyber secur", False),
        ("est News", False),
        ("Hiring Companies", False),
        ("es to apply for maximum exposure.Apply", False),
        ("es to apply for maximum exposure.", False),

        # VALID - Real companies
        ("North Point Technology, LLC", True),
        ("Advanced Technology Leaders, Inc.", True),
        ("Google", True),
        ("Amazon Web Services", True),
        ("Palo Alto Networks", True),
        ("CrowdStrike", True),
        ("Microsoft", True),
        ("Okta", True),
        ("Cisco Systems", True),
        ("IBM Security", True),
    ]

    passed = 0
    failed = 0

    for company_name, expected_valid in test_cases:
        result = engine._is_valid_company_name(company_name)
        status = "✅" if result == expected_valid else "❌"

        if result == expected_valid:
            passed += 1
        else:
            failed += 1
            print(f"{status} FAIL: '{company_name[:50]}' - Expected {expected_valid}, got {result}")

    print(f"\n📊 Test Results:")
    print(f"   ✅ Passed: {passed}/{len(test_cases)}")
    print(f"   ❌ Failed: {failed}/{len(test_cases)}")

    if failed == 0:
        print("\n🎉 All validation tests passed!")
        return True
    else:
        print(f"\n⚠️  {failed} tests failed")
        return False

def test_indeed_scraping_quick():
    """Quick test of Indeed scraping with 1 keyword"""
    print("\n" + "=" * 70)
    print("🧪 Testing Indeed Scraping (Quick - 1 keyword)")
    print("=" * 70)

    engine = CompanyDiscoveryV3()

    try:
        # Test with just 1 keyword to verify it works
        companies = engine._scrape_indeed(max_companies=10)

        print(f"\n✅ Successfully scraped Indeed")
        print(f"📊 Found {len(companies)} companies:")

        for i, company in enumerate(list(companies)[:10], 1):
            print(f"   {i}. {company}")

        # Check if we got any of the bad companies
        bad_companies = [c for c in companies if not engine._is_valid_company_name(c)]

        if bad_companies:
            print(f"\n⚠️  WARNING: Found {len(bad_companies)} invalid companies:")
            for bad in bad_companies[:5]:
                print(f"   ❌ {bad}")
            return False
        else:
            print(f"\n✅ All companies passed validation!")
            return True

    except Exception as e:
        print(f"\n❌ Error during scraping: {str(e)[:200]}")
        return False
    finally:
        engine._close_selenium_driver()

if __name__ == "__main__":
    print("🚀 Starting Headless Mode Fix Tests")
    print("=" * 70)

    # Test 1: Validation logic
    validation_passed = test_company_name_validation()

    # Test 2: Quick scraping test (optional - can be slow)
    print("\n⏱️  Quick scraping test starting (this may take 30-60 seconds)...")
    scraping_passed = test_indeed_scraping_quick()

    # Summary
    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    print(f"   Company Name Validation: {'✅ PASS' if validation_passed else '❌ FAIL'}")
    print(f"   Indeed Scraping Test: {'✅ PASS' if scraping_passed else '❌ FAIL'}")

    if validation_passed and scraping_passed:
        print("\n✅ All tests passed! Safe to push to GitHub.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Review issues before pushing.")
        sys.exit(1)
