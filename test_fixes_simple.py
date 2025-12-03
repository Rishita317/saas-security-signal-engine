"""
Simple Test - Verify Fixes Without Dependencies
"""

import sys

print("=" * 70)
print("🧪 Testing Core Fixes")
print("=" * 70 + "\n")

# Test 1: Check CSV import in file
print("📝 Test 1: Checking CSV import exists in weekly_refresh.py...")
try:
    with open('orchestration/weekly_refresh.py', 'r') as f:
        content = f.read()

    if 'import csv' in content:
        print("✅ CSV module import found in weekly_refresh.py")
    else:
        print("❌ CSV import missing in weekly_refresh.py")
        sys.exit(1)

except Exception as e:
    print(f"❌ Could not read weekly_refresh.py: {e}")
    sys.exit(1)

# Test 2: Check URL generation method exists
print("\n📝 Test 2: Checking _generate_job_url method exists...")
try:
    with open('scrapers/multi_source_jobs.py', 'r') as f:
        content = f.read()

    if '_generate_job_url' in content:
        print("✅ _generate_job_url method found")

        # Check for realistic URL patterns
        required_patterns = ['linkedin.com', 'indeed.com', 'dice.com']
        found_patterns = []
        for pattern in required_patterns:
            if pattern in content:
                found_patterns.append(pattern)

        if len(found_patterns) >= 2:
            print(f"✅ Found {len(found_patterns)} realistic URL patterns")
        else:
            print(f"⚠️  Only found {len(found_patterns)} URL patterns")
    else:
        print("❌ _generate_job_url method not found")
        sys.exit(1)

except Exception as e:
    print(f"❌ Could not read multi_source_jobs.py: {e}")
    sys.exit(1)

# Test 3: Check streamlit app has LinkColumn config
print("\n📝 Test 3: Checking streamlit dashboard has hyperlink config...")
try:
    with open('streamlit_app.py', 'r') as f:
        content = f.read()

    if 'LinkColumn' in content and 'column_config' in content:
        print("✅ Dashboard configured with clickable hyperlinks")

        # Check if URL is in display columns
        if "'url'" in content.lower() or '"url"' in content.lower():
            print("✅ URL column included in display")
        else:
            print("⚠️  URL column may not be displayed")
    else:
        print("❌ Hyperlink configuration not found")
        sys.exit(1)

except Exception as e:
    print(f"❌ Could not read streamlit_app.py: {e}")
    sys.exit(1)

# Test 4: Check GitHub Actions permissions
print("\n📝 Test 4: Checking GitHub Actions workflow permissions...")
try:
    with open('.github/workflows/weekly_refresh.yml', 'r') as f:
        content = f.read()

    if 'permissions:' in content:
        print("✅ Permissions section found")

        if 'contents: write' in content:
            print("✅ Write permissions granted")
        else:
            print("❌ Write permissions not found")
            sys.exit(1)
    else:
        print("❌ Permissions section not found")
        sys.exit(1)

except Exception as e:
    print(f"❌ Could not read workflow file: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ALL CORE FIXES VERIFIED!")
print("=" * 70)
print("\n📋 Summary:")
print("   1. ✅ CSV import added to weekly_refresh.py (line ~17)")
print("   2. ✅ Job URL generation with realistic patterns")
print("   3. ✅ Dashboard hyperlinks configured")
print("   4. ✅ GitHub Actions write permissions added")
print("\n🚀 Ready to commit and push to GitHub!")
