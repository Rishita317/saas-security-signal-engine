import sys
sys.path.append('.')
import streamlit_app_v2 as app

company_tracker, hiring_details, conversation_details, week_id = app.load_latest_data()

print('=' * 70)
print('✅ DASHBOARD DATA LOADING TEST')
print('=' * 70)
print(f'Week: {week_id}')
print(f'Companies: {len(company_tracker) if company_tracker is not None else 0}')
print(f'Jobs: {len(hiring_details) if not hiring_details.empty else 0}')
print(f'Posts: {len(conversation_details) if not conversation_details.empty else 0}')
print()

if conversation_details is not None and not conversation_details.empty:
    if 'author' in conversation_details.columns:
        print('✅ Author column exists in conversation data!')
        print()
        print('Sample posts with authors:')
        for idx, row in conversation_details[['publisher', 'author', 'title']].head(5).iterrows():
            publisher = row['publisher'][:18]
            author = row['author'][:28]
            title = row['title'][:35]
            print(f'  {publisher:18} | {author:28} | {title}...')

        # Stats
        has_author = conversation_details['author'].notna() & (conversation_details['author'] != 'Unknown')
        print()
        print(f'📊 Posts with real authors: {has_author.sum()}/{len(conversation_details)}')
    else:
        print('❌ Author column missing!')
        print(f'Columns: {list(conversation_details.columns)}')
else:
    print('❌ No conversation data loaded')
