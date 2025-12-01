"""
SaaS Security Signal Engine - Streamlit Dashboard

A simple, clean dashboard for visualizing hiring signals and conversation trends
in the SaaS security space.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import glob

# Page configuration
st.set_page_config(
    page_title="SaaS Security Signal Engine",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_latest_data():
    """Load the most recent hiring signals CSV"""
    data_dir = "data"
    csv_files = glob.glob(f"{data_dir}/hiring_signals_*.csv")

    if not csv_files:
        return None, None

    # Get the most recent file
    latest_file = max(csv_files, key=os.path.getctime)
    df = pd.read_csv(latest_file)

    # Parse dates
    df['posted_date'] = pd.to_datetime(df['posted_date'])

    # Extract timestamp from filename
    timestamp = latest_file.split('_')[-2] + '_' + latest_file.split('_')[-1].replace('.csv', '')

    return df, timestamp


@st.cache_data
def load_conversation_data():
    """Load the most recent conversation signals CSV"""
    data_dir = "data"
    csv_files = glob.glob(f"{data_dir}/conversation_signals_*.csv")

    if not csv_files:
        return None, None

    # Get the most recent file
    latest_file = max(csv_files, key=os.path.getctime)
    df = pd.read_csv(latest_file)

    # Parse dates
    if 'published_at' in df.columns:
        df['published_at'] = pd.to_datetime(df['published_at'])

    # Extract timestamp from filename
    timestamp = latest_file.split('_')[-2] + '_' + latest_file.split('_')[-1].replace('.csv', '')

    return df, timestamp


def create_category_chart(df):
    """Create a bar chart of jobs by category"""
    category_counts = df['job_category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']

    fig = px.bar(
        category_counts,
        x='Category',
        y='Count',
        title='Jobs by Category',
        color='Count',
        color_continuous_scale='Blues',
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Category",
        yaxis_title="Number of Jobs",
        height=400,
    )
    return fig


def create_company_chart(df, top_n=10):
    """Create a horizontal bar chart of top companies"""
    company_counts = df['company_name'].value_counts().head(top_n).reset_index()
    company_counts.columns = ['Company', 'Count']

    fig = px.bar(
        company_counts,
        x='Count',
        y='Company',
        orientation='h',
        title=f'Top {top_n} Companies Hiring',
        color='Count',
        color_continuous_scale='Viridis',
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Number of Roles",
        yaxis_title="",
        height=400,
    )
    return fig


def create_relevance_distribution(df):
    """Create histogram of relevance scores"""
    fig = px.histogram(
        df,
        x='relevance_score',
        nbins=20,
        title='Relevance Score Distribution',
        color_discrete_sequence=['#1f77b4'],
    )
    fig.update_layout(
        xaxis_title="Relevance Score",
        yaxis_title="Number of Jobs",
        height=300,
    )
    return fig


def create_timeline_chart(df):
    """Create timeline of job postings"""
    df_timeline = df.groupby(df['posted_date'].dt.date).size().reset_index()
    df_timeline.columns = ['Date', 'Count']

    fig = px.line(
        df_timeline,
        x='Date',
        y='Count',
        title='Job Postings Over Time',
        markers=True,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Jobs Posted",
        height=300,
    )
    return fig


def main():
    # Header
    st.markdown('<p class="main-header">🔐 SaaS Security Signal Engine</p>', unsafe_allow_html=True)
    st.markdown("**Automated GTM Intelligence - Weekly Refreshed Data**")
    st.markdown("---")

    # Create tabs
    tab1, tab2 = st.tabs(["📊 Hiring Signals", "💬 Conversation Signals"])

    with tab1:
        show_hiring_signals()

    with tab2:
        show_conversation_signals()


def show_hiring_signals():
    """Display hiring signals dashboard"""
    # Load data
    df, timestamp = load_latest_data()

    if df is None:
        st.error("No hiring data found. Please run `python test_pipeline_gemini.py` to generate data first.")
        return

    # Sidebar
    with st.sidebar:
        st.header("📊 Dashboard Filters")

        # Data info
        st.info(f"**Last Updated:** {timestamp}")
        st.metric("Total Jobs", len(df))

        # Filters
        st.subheader("Filters")

        # Category filter
        categories = ['All'] + sorted(df['job_category'].unique().tolist())
        selected_category = st.selectbox("Category", categories)

        # Source filter
        sources = ['All'] + sorted(df['source_platform'].unique().tolist())
        selected_source = st.selectbox("Source", sources)

        # Relevance filter
        min_relevance = st.slider(
            "Minimum Relevance Score",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.1,
        )

        # Apply filters
        filtered_df = df.copy()
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['job_category'] == selected_category]
        if selected_source != 'All':
            filtered_df = filtered_df[filtered_df['source_platform'] == selected_source]
        filtered_df = filtered_df[filtered_df['relevance_score'] >= min_relevance]

        st.metric("Filtered Jobs", len(filtered_df))

        st.markdown("---")
        st.markdown("### 🔗 Quick Links")
        st.markdown("- [GitHub Repo](https://github.com/Rishita317/saas-security-signal-engine)")
        st.markdown("- [Run Pipeline](javascript:void(0))")
        st.markdown("- [Documentation](README.md)")

    # Main content
    if len(filtered_df) == 0:
        st.warning("No jobs match the current filters. Try adjusting the filters.")
        return

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Jobs",
            len(filtered_df),
            delta=None,
        )

    with col2:
        unique_companies = filtered_df['company_name'].nunique()
        st.metric(
            "Companies",
            unique_companies,
        )

    with col3:
        avg_relevance = filtered_df['relevance_score'].mean()
        st.metric(
            "Avg Relevance",
            f"{avg_relevance:.2f}",
        )

    with col4:
        high_relevance = (filtered_df['relevance_score'] >= 0.8).sum()
        st.metric(
            "High Relevance",
            high_relevance,
            delta=f"{high_relevance/len(filtered_df)*100:.0f}%",
        )

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_category_chart(filtered_df), use_container_width=True)

    with col2:
        st.plotly_chart(create_company_chart(filtered_df), use_container_width=True)

    # Timeline
    st.plotly_chart(create_timeline_chart(filtered_df), use_container_width=True)

    # Relevance distribution
    st.plotly_chart(create_relevance_distribution(filtered_df), use_container_width=True)

    st.markdown("---")

    # Data table
    st.subheader("📋 Job Listings")

    # Add search
    search_query = st.text_input("🔍 Search jobs (company, title, keywords)", "")

    display_df = filtered_df.copy()
    if search_query:
        mask = (
            display_df['company_name'].str.contains(search_query, case=False, na=False) |
            display_df['job_title'].str.contains(search_query, case=False, na=False) |
            display_df['matched_keywords'].str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]

    # Format for display
    display_cols = [
        'company_name', 'job_title', 'job_category',
        'location', 'relevance_score', 'source_platform', 'posted_date'
    ]

    # Rename columns for better display
    display_df = display_df[display_cols].copy()
    display_df.columns = [
        'Company', 'Job Title', 'Category',
        'Location', 'Relevance', 'Source', 'Posted Date'
    ]

    # Format dates
    display_df['Posted Date'] = display_df['Posted Date'].dt.strftime('%Y-%m-%d')

    # Sort by relevance
    display_df = display_df.sort_values('Relevance', ascending=False)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
    )

    # Download button
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name=f"filtered_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

    st.markdown("---")

    # Insights
    st.subheader("💡 Key Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏆 Top Categories")
        top_categories = filtered_df['job_category'].value_counts().head(3)
        for i, (cat, count) in enumerate(top_categories.items(), 1):
            st.markdown(f"{i}. **{cat}**: {count} jobs")

    with col2:
        st.markdown("#### 🌟 Top Companies")
        top_companies = filtered_df['company_name'].value_counts().head(3)
        for i, (company, count) in enumerate(top_companies.items(), 1):
            st.markdown(f"{i}. **{company}**: {count} roles")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>🔐 SaaS Security Signal Engine | Built for Obsidian Security AI GTM Engineer Role</p>
            <p>Powered by Google Gemini, spaCy NLP, and Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_conversation_signals():
    """Display conversation signals dashboard"""
    # Load conversation data
    df, timestamp = load_conversation_data()

    if df is None:
        st.error("No conversation data found. Please run `python test_conversation_pipeline.py` to generate data first.")
        return

    st.subheader("💬 Conversation Signals - What People Are Saying")
    st.info(f"**Last Updated:** {timestamp} | **Total Conversations:** {len(df)}")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Items", len(df))

    with col2:
        if 'publisher' in df.columns:
            unique_publishers = df[df['platform'].isin(['rss', 'tldr_infosec'])]['publisher'].nunique()
        else:
            unique_publishers = 0
        st.metric("Publishers", unique_publishers)

    with col3:
        avg_relevance = df['relevance_score'].mean()
        st.metric("Avg Relevance", f"{avg_relevance:.2f}")

    with col4:
        if 'urgency' in df.columns:
            high_urgency = df[df['urgency'].isin(['breaking', 'high'])].shape[0]
        else:
            high_urgency = 0
        st.metric("High Urgency", high_urgency)

    st.markdown("---")

    # Top contributors table (Reddit)
    reddit_df = df[df['platform'] == 'reddit'].copy()
    if len(reddit_df) > 0 and 'author' in reddit_df.columns:
        st.subheader("🏆 Top Contributors (Reddit)")
        contributor_counts = reddit_df['author'].value_counts().head(10)
        contributor_df = pd.DataFrame({
            'Contributor': contributor_counts.index,
            'Posts': contributor_counts.values
        })
        st.dataframe(contributor_df, use_container_width=True)

    st.markdown("---")

    # Top publishers table
    publisher_df = df[df['platform'].isin(['rss', 'tldr_infosec'])].copy()
    if len(publisher_df) > 0 and 'publisher' in publisher_df.columns:
        st.subheader("📰 Top Publishers")
        publisher_counts = publisher_df['publisher'].value_counts().head(10)
        publisher_table = pd.DataFrame({
            'Publisher': publisher_counts.index,
            'Articles': publisher_counts.values
        })
        st.dataframe(publisher_table, use_container_width=True)

    st.markdown("---")

    # Trending/High urgency conversations
    if 'urgency' in df.columns:
        high_urgency_df = df[df['urgency'].isin(['breaking', 'high'])].copy()
        if len(high_urgency_df) > 0:
            st.subheader("🔥 High Urgency / Breaking News")
            for idx, row in high_urgency_df.head(5).iterrows():
                with st.expander(f"[{row['urgency'].upper()}] {row['title'][:80]}..."):
                    st.write(f"**Platform:** {row['platform']}")
                    st.write(f"**Category:** {row.get('category', 'N/A')}")
                    st.write(f"**Relevance:** {row['relevance_score']:.2f}")
                    if 'url' in row and pd.notna(row['url']):
                        st.write(f"**URL:** {row['url']}")

    st.markdown("---")

    # Full data table
    st.subheader("📋 All Conversations")

    # Search
    search_query = st.text_input("🔍 Search conversations", "")

    display_df = df.copy()
    if search_query:
        mask = (
            display_df['title'].str.contains(search_query, case=False, na=False) |
            display_df.get('publisher', pd.Series([''] * len(display_df))).str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]

    # Format for display
    display_cols = ['platform', 'title', 'category', 'relevance_score']
    if 'urgency' in display_df.columns:
        display_cols.append('urgency')
    if 'publisher' in display_df.columns:
        display_cols.append('publisher')

    display_df = display_df[display_cols].copy()
    display_df = display_df.sort_values('relevance_score', ascending=False)

    st.dataframe(display_df, use_container_width=True, height=400)

    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Conversation Data (CSV)",
        data=csv,
        file_name=f"conversation_signals_{timestamp}.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
