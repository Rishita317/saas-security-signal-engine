#!/usr/bin/env python3
"""
Cleanup Script - Archive Outdated Files
Moves all outdated/unused files to _archive/ directory for safekeeping
"""

import os
import shutil
from datetime import datetime

# Create archive directory with timestamp
archive_dir = f"_archive/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(archive_dir, exist_ok=True)

print("=" * 70)
print("🗑️  CLEANUP: Archiving Outdated Files")
print("=" * 70)
print(f"Archive location: {archive_dir}\n")

# Files to archive
files_to_archive = {
    "Old Dashboard": [
        "streamlit_app.py",
    ],

    "Old Scraper Versions": [
        "scrapers/company_discovery.py",
        "scrapers/multi_source_jobs_OLD_BACKUP.py",
        "scrapers/demo_data.py",
    ],

    "Unused Scrapers": [
        "scrapers/hackernews_hiring.py",
        "scrapers/reddit_conversations.py",
        "scrapers/tldr_infosec.py",
        "scrapers/multi_ats_scraper.py",
    ],

    "Old Orchestration": [
        "orchestration/weekly_refresh_v2.py",
    ],

    "Test Runner Scripts": [
        "run_indeed_expanded.py",
        "run_internships_only.py",
        "run_v3_with_existing_data.py",
    ],

    "Test Files": [
        "test_all_fixes.py",
        "test_company_discovery.py",
        "test_conversation_pipeline.py",
        "test_fixes_simple.py",
        "test_indeed_selenium.py",
        "test_openai_setup.py",
        "test_pipeline.py",
        "test_pipeline_gemini.py",
        "test_real_scraping.py",
        "test_real_urls.py",
        "test_scale_100.py",
        "test_v3_discovery.py",
        "test_v3_quick.py",
        "test_workday_scraper.py",
    ],

    "Old Documentation": [
        "FINAL_FIXES_SUMMARY.md",
        "FIXES_SUMMARY.md",
        "GEMINI_INTEGRATION.md",
        "OPENAI_INTEGRATION.md",
        "OPENAI_SETUP_CHECKLIST.md",
        "PHASE1_COMPLETE.md",
        "PHASE2_COMPLETE.md",
        "PHASE3_COMPLETE.md",
        "PROJECT_STATUS.md",
        "QUICK_WINS_CHECKLIST.md",
        "REBUILD_PLAN.md",
        "TEST_RESULTS.md",
        "V3_IMPLEMENTATION_SUMMARY.md",
    ],

    "JSON Test Output": [
        "test_company_discovery.json",
        "test_real_jobs.json",
        "test_scale_100_conversations.json",
        "test_scale_100_hiring.json",
        "test_scale_100_tracker.json",
    ],

    "Log Files": [
        "run_indeed_1000.log",
        "run_indeed_expanded.log",
        "run_internships.log",
        "run_internships_fixed.log",
        "streamlit.log",
        "v3_discovery_output.log",
        "v3_discovery_run.log",
        "weekly_refresh_1000.log",
        "weekly_refresh_47keywords.log",
        "weekly_refresh_ALL_SOURCES.log",
        "weekly_refresh_FINAL.log",
        "weekly_refresh_FINAL_v3.log",
        "weekly_refresh_INDEED_ONLY_90keywords.log",
        "weekly_refresh_LIVE.log",
        "weekly_refresh_WITH_WORKDAY.log",
        "weekly_refresh_latest.log",
        "weekly_refresh_multi_source.log",
    ],
}

total_archived = 0
total_missing = 0

for category, files in files_to_archive.items():
    print(f"\n📁 {category}:")

    for file_path in files:
        if os.path.exists(file_path):
            # Create subdirectory structure in archive
            dest_dir = os.path.join(archive_dir, os.path.dirname(file_path))
            os.makedirs(dest_dir, exist_ok=True)

            # Move file
            dest_path = os.path.join(archive_dir, file_path)
            shutil.move(file_path, dest_path)
            print(f"   ✅ Archived: {file_path}")
            total_archived += 1
        else:
            print(f"   ⚠️  Not found: {file_path}")
            total_missing += 1

print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"✅ Files archived: {total_archived}")
print(f"⚠️  Files not found: {total_missing}")
print(f"\n📂 Archive location: {archive_dir}")
print("\n💡 To restore files, simply move them back from the archive directory.")
print("💡 To permanently delete, run: rm -rf _archive/")
print("\n✅ Cleanup complete!")
