"""
SaaS Security Signal Engine V2 - Company-Centric GTM Dashboard

NEW APPROACH:
- Focus on COMPANIES (not individual jobs)
- 3 Tabs: Company Tracker, Hiring Signals, Conversation Signals
- Priority scoring: Both (3) > Hiring Only (2) > Talking Only (1)

Last Updated: December 5, 2025 - Fresh data from automated weekly refresh
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import glob

# Page configuration
st.set_page_config(
    page_title="SaaS Security GTM Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #000000;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    .stMetric [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }
    /* Dataframe text color - table cells only */
    .stDataFrame tbody tr td {
        color: #000000 !important;
    }
    .stDataFrame thead tr th {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)


def load_latest_data():
    """Load the most recent data files"""
    try:
        # Find the latest week directory
        week_dirs = glob.glob("data/weekly/2025_W*")
        if not week_dirs:
            return None, None, None, None

        latest_week = max(week_dirs)

        # Find latest files in that week
        company_tracker_files = glob.glob(f"{latest_week}/company_tracker_*.csv")
        hiring_details_files = glob.glob(f"{latest_week}/hiring_details_*.csv")
        conversation_files = glob.glob(f"{latest_week}/conversation_details_*.csv")

        if not company_tracker_files:
            return None, None, None, latest_week

        # Load the file with the MOST companies (best data quality)
        # This avoids loading failed runs that may have fewer companies
        def get_best_file(files):
            best_file = None
            max_rows = 0
            for f in files:
                try:
                    row_count = pd.read_csv(f).shape[0]
                    if row_count > max_rows:
                        max_rows = row_count
                        best_file = f
                except:
                    continue
            return best_file

        latest_tracker = get_best_file(company_tracker_files)
        latest_hiring = get_best_file(hiring_details_files) if hiring_details_files else None
        latest_conversation = get_best_file(conversation_files) if conversation_files else None

        company_tracker = pd.read_csv(latest_tracker)
        hiring_details = pd.read_csv(latest_hiring) if latest_hiring else pd.DataFrame()
        conversation_details = pd.read_csv(latest_conversation) if latest_conversation else pd.DataFrame()

        return company_tracker, hiring_details, conversation_details, latest_week

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None, None


def main():
    """Main dashboard function"""

    # Header
    st.markdown('<p class="main-header">🎯 SaaS Security GTM Intelligence</p>', unsafe_allow_html=True)
    st.markdown("**Company-Centric Market Intelligence for Obsidian Security**")

    # Load data
    company_tracker, hiring_details, conversation_details, week_id = load_latest_data()

    if company_tracker is None:
        st.warning("⚠️ No data found. Run the weekly refresh first:")
        st.code("python orchestration/weekly_refresh_v2.py --companies 100 --posts 20")
        return

    # Sidebar - Summary Stats
    st.sidebar.header("📊 Quick Stats")
    st.sidebar.metric("Week", week_id.split('/')[-1] if week_id else "N/A")
    st.sidebar.metric("Total Companies", len(company_tracker))
    st.sidebar.metric("Total Jobs", len(hiring_details) if not hiring_details.empty else 0)
    st.sidebar.metric("Total Posts", len(conversation_details) if not conversation_details.empty else 0)

    # Breakdown by priority
    st.sidebar.markdown("---")
    st.sidebar.markdown("**By Activity Type:**")

    high_priority = len(company_tracker[company_tracker['activity_type'] == 'both'])
    hiring_only = len(company_tracker[company_tracker['activity_type'] == 'hiring_only'])
    talking_only = len(company_tracker[company_tracker['activity_type'] == 'talking_only'])

    st.sidebar.metric("🎯 High Priority (Both)", high_priority)
    st.sidebar.metric("📢 Hiring Only", hiring_only)
    st.sidebar.metric("💬 Talking Only", talking_only)

    # Main Content - 4 Tabs (LinkedIn Resources is BONUS - isolated)
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 Company Tracker",
        "📋 Hiring Signals",
        "💬 Conversation Signals",
        "🔗 LinkedIn Resources (Bonus)"
    ])

    # TAB 1: Company Tracker
    with tab1:
        st.header("🏢 Company Tracker")
        st.markdown("**1,000 companies active in the SaaS Security space**")

        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            activity_filter = st.selectbox(
                "Activity Type",
                ["All", "High Priority (Both)", "Hiring Only", "Talking Only"],
                index=0
            )

        with col2:
            min_priority = st.slider("Min Priority Score", 1, 3, 1)

        with col3:
            sort_by = st.selectbox(
                "Sort By",
                ["Priority Score", "Role Count", "Post Count", "Company Name"],
                index=0
            )

        # Apply filters
        filtered_df = company_tracker.copy()

        if activity_filter != "All":
            activity_map = {
                "High Priority (Both)": "both",
                "Hiring Only": "hiring_only",
                "Talking Only": "talking_only"
            }
            filtered_df = filtered_df[filtered_df['activity_type'] == activity_map[activity_filter]]

        filtered_df = filtered_df[filtered_df['priority_score'] >= min_priority]

        # Sort
        sort_map = {
            "Priority Score": "priority_score",
            "Role Count": "role_count",
            "Post Count": "post_count",
            "Company Name": "company_name"
        }
        filtered_df = filtered_df.sort_values(
            by=sort_map[sort_by],
            ascending=(sort_by == "Company Name")
        )

        # Display table
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=600,
            column_config={
                "company_name": st.column_config.TextColumn("Company", width="medium"),
                "activity_type": st.column_config.TextColumn("Activity", width="small"),
                "role_count": st.column_config.NumberColumn("# Roles", width="small"),
                "post_count": st.column_config.NumberColumn("# Posts", width="small"),
                "priority_score": st.column_config.NumberColumn("Priority", width="small"),
                "last_updated": st.column_config.DateColumn("Updated", width="small"),
            }
        )

        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"company_tracker_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    # TAB 2: Hiring Signals
    with tab2:
        st.header("📋 Hiring Signals")
        st.markdown("**Drill-down view of security job postings by company**")

        if hiring_details.empty:
            st.info("No hiring data available yet.")
        else:
            # Company filter
            companies = ["All"] + sorted(hiring_details['company_name'].unique().tolist())
            selected_company = st.selectbox("Filter by Company", companies, index=0)

            # Apply filter
            filtered_jobs = hiring_details.copy()
            if selected_company != "All":
                filtered_jobs = filtered_jobs[filtered_jobs['company_name'] == selected_company]

            # Display table with clickable URLs
            st.dataframe(
                filtered_jobs,
                use_container_width=True,
                height=600,
                column_config={
                    "company_name": st.column_config.TextColumn("Company", width="medium"),
                    "title": st.column_config.TextColumn("Job Title", width="large"),
                    "location": st.column_config.TextColumn("Location", width="small"),
                    "source": st.column_config.TextColumn("Source", width="small"),
                    "url": st.column_config.LinkColumn("Apply", width="small"),
                    "posted_date": st.column_config.DateColumn("Posted", width="small"),
                }
            )

            # Download button
            csv = filtered_jobs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"hiring_signals_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

    # TAB 3: Conversation Signals
    with tab3:
        st.header("💬 Conversation Signals")
        st.markdown("**Blog posts and discussions from Top 10 security publishers**")

        if conversation_details.empty:
            st.info("No conversation data available yet.")
        else:
            # Publisher filter
            publishers = ["All"] + sorted(conversation_details['publisher'].unique().tolist())
            selected_publisher = st.selectbox("Filter by Publisher", publishers, index=0)

            # Apply filter
            filtered_convs = conversation_details.copy()
            if selected_publisher != "All":
                filtered_convs = filtered_convs[filtered_convs['publisher'] == selected_publisher]

            # Display table with clickable URLs
            st.dataframe(
                filtered_convs,
                use_container_width=True,
                height=600,
                column_config={
                    "publisher": st.column_config.TextColumn("Publisher", width="medium"),
                    "title": st.column_config.TextColumn("Title", width="large"),
                    "url": st.column_config.LinkColumn("Read", width="small"),
                    "published_at": st.column_config.TextColumn("Published", width="small"),
                    "source": st.column_config.TextColumn("Source", width="small"),
                }
            )

            # Download button
            csv = filtered_convs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"conversation_signals_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

    # TAB 4: LinkedIn Resources (BONUS - ISOLATED from main pipeline)
    with tab4:
        st.header("🔗 LinkedIn Resources (Optional Bonus Feature)")
        st.markdown("⚠️ **This tab is completely separate from the main scraping pipeline. No LinkedIn scraping is performed.**")

        # Import LinkedIn resources (isolated module)
        try:
            import linkedin_resources as lr

            # Section 1: LinkedIn Job Search URLs
            st.subheader("📋 Curated LinkedIn Job Searches")
            st.markdown("Click any link below to search LinkedIn for fresh security roles (auto-refreshes):")

            # Display job search links in 2 columns
            col1, col2 = st.columns(2)

            job_searches = list(lr.LINKEDIN_JOB_SEARCHES.items())
            mid_point = len(job_searches) // 2

            with col1:
                for name, url in job_searches[:mid_point]:
                    st.markdown(f"🔗 [{name}]({url})")

            with col2:
                for name, url in job_searches[mid_point:]:
                    st.markdown(f"🔗 [{name}]({url})")

            st.markdown("---")

            # Section 2: LinkedIn Content Search URLs
            st.subheader("💬 Curated LinkedIn Content Searches")
            st.markdown("Click any link to find security thought leadership posts:")

            col1, col2 = st.columns(2)

            content_searches = list(lr.LINKEDIN_CONTENT_SEARCHES.items())
            mid_point = len(content_searches) // 2

            with col1:
                for name, url in content_searches[:mid_point]:
                    st.markdown(f"🔗 [{name}]({url})")

            with col2:
                for name, url in content_searches[mid_point:]:
                    st.markdown(f"🔗 [{name}]({url})")

            st.markdown("---")

            # Section 3: Optional CSV Upload
            st.subheader("📤 Optional: Upload LinkedIn Export CSV")
            st.markdown("""
            **Semi-Manual Bonus Feature:**
            1. Use the LinkedIn search links above
            2. Manually export your results to CSV
            3. Upload here to merge with existing data (optional)
            """)

            uploaded_file = st.file_uploader("Upload linkedin_jobs.csv (optional)", type=['csv'])

            if uploaded_file is not None:
                # Save uploaded file
                os.makedirs("inputs", exist_ok=True)
                csv_path = "inputs/linkedin_jobs.csv"

                with open(csv_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                st.success(f"✅ LinkedIn CSV uploaded successfully!")

                # Ingest and display stats
                linkedin_df = lr.ingest_linkedin_csv(csv_path)

                if linkedin_df is not None:
                    stats = lr.get_linkedin_stats(linkedin_df)

                    st.metric("LinkedIn Jobs Loaded", stats['total_jobs'])
                    st.metric("Unique Companies", stats['unique_companies'])

                    st.dataframe(linkedin_df.head(10), use_container_width=True)

            # Section 4: Usage Instructions
            st.markdown("---")
            st.subheader("ℹ️ How to Use LinkedIn Resources")
            st.markdown(lr.USAGE_INSTRUCTIONS)

            # Note about isolation
            st.info("""
            **🔒 Important Notes:**
            - This feature does NOT scrape LinkedIn (TOS compliant)
            - All links are user-driven and dynamic (auto-refresh)
            - LinkedIn data is optional and does NOT affect your existing pipeline
            - All logic is isolated in `linkedin_resources.py`
            """)

        except ImportError:
            st.error("⚠️ LinkedIn resources module not found. Please ensure `linkedin_resources.py` exists.")

    # Footer
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    st.markdown("*Data refreshes weekly on Mondays at 8 AM UTC*")


if __name__ == "__main__":
    main()
