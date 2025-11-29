# Streamlit Dashboard Guide

## Quick Start

### Launch the Dashboard

```bash
cd /Users/rishitameharishi/Documents/Sass_Security_Engine\(SSE\)
source venv/bin/activate
streamlit run streamlit_app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

---

## Dashboard Features

### 📊 Key Metrics (Top Row)

- **Total Jobs**: Number of jobs matching current filters
- **Companies**: Unique companies hiring
- **Avg Relevance**: Average relevance score (0-1.0)
- **High Relevance**: Count and percentage of jobs with score ≥0.8

### 📈 Interactive Charts

1. **Jobs by Category**
   - Bar chart showing distribution across SSPM, SaaS Security, AI Agent Security, etc.
   - Color-coded by count
   - Sortable

2. **Top 10 Companies Hiring**
   - Horizontal bar chart
   - Shows companies with most open roles
   - Dynamically updates with filters

3. **Job Postings Timeline**
   - Line chart showing posting trends over time
   - Helps identify hiring spikes
   - Interactive hover for details

4. **Relevance Score Distribution**
   - Histogram of relevance scores
   - Helps understand data quality
   - Shows distribution across 0-1.0 range

### 🔍 Filters & Search (Sidebar)

**Filters:**
- **Category**: Filter by SSPM, SaaS Security, AI Agent Security, etc.
- **Source**: Filter by HackerNews, Reddit, or other sources
- **Minimum Relevance Score**: Slider from 0.0 to 1.0

**Search:**
- Full-text search across company names, job titles, and keywords
- Real-time filtering as you type
- Case-insensitive

### 📋 Data Table

- **Sortable**: Click column headers to sort
- **Searchable**: Use search box above table
- **Formatted**: Clean display with proper date formatting
- **Downloadable**: Export filtered results to CSV

### 💾 Export

Click "📥 Download Filtered Data (CSV)" to export:
- Only filtered/searched results
- All columns included
- Timestamped filename
- Ready for Excel or further analysis

---

## Usage Examples

### Example 1: Find SSPM Jobs

1. In sidebar, select **Category**: "SSPM"
2. Set **Minimum Relevance**: 0.7
3. Review filtered jobs in table
4. Click download to save results

### Example 2: Track CrowdStrike Hiring

1. In search box, type "CrowdStrike"
2. View all CrowdStrike roles
3. Check relevance scores
4. Export for sharing with team

### Example 3: High-Value Targets

1. Set **Minimum Relevance**: 0.8
2. Select **Category**: "SSPM" or "AI Agent Security"
3. View only highly relevant, high-priority roles
4. Sort by company to see which are hiring most

### Example 4: Recent Activity

1. Look at "Job Postings Timeline" chart
2. Identify spikes in hiring
3. Filter by those dates
4. Investigate which companies/categories drove the spike

---

## Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│  🔐 SaaS Security Signal Engine                         │
│  Automated GTM Intelligence for SaaS Security          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [ Total Jobs ] [ Companies ] [ Avg Relevance ] [ High ]│
│                                                         │
├───────────────────────┬─────────────────────────────────┤
│  Jobs by Category    │  Top 10 Companies Hiring       │
│  [Bar Chart]         │  [Horizontal Bar Chart]        │
├───────────────────────┴─────────────────────────────────┤
│  Job Postings Timeline                                 │
│  [Line Chart]                                          │
├────────────────────────────────────────────────────────┤
│  Relevance Score Distribution                          │
│  [Histogram]                                           │
├────────────────────────────────────────────────────────┤
│  📋 Job Listings                                       │
│  [Searchable, Sortable Table]                          │
│  [Download Button]                                     │
└────────────────────────────────────────────────────────┘
```

**Sidebar:**
```
┌──────────────────┐
│ 📊 Filters       │
├──────────────────┤
│ Last Updated     │
│ Total Jobs: 30   │
├──────────────────┤
│ Category: [All]  │
│ Source: [All]    │
│ Min Relevance: ▓ │
├──────────────────┤
│ Filtered: 30     │
├──────────────────┤
│ 🔗 Quick Links   │
└──────────────────┘
```

---

## Data Requirements

The dashboard automatically loads the most recent CSV file from the `data/` directory.

**Required format:**
- Filename: `hiring_signals_YYYYMMDD_HHMMSS.csv`
- Columns: company_name, job_title, job_category, location, relevance_score, source_platform, source_url, posted_date, matched_keywords

**Generate data:**
```bash
python test_pipeline.py
```

---

## Customization

### Change Number of Top Companies

Edit `streamlit_app.py`, line ~133:
```python
create_company_chart(filtered_df, top_n=10)  # Change to 15, 20, etc.
```

### Adjust Chart Colors

Charts use Plotly color schemes:
- `Blues`: Jobs by category
- `Viridis`: Top companies
- `#1f77b4`: Default blue

Change in respective chart functions.

### Add New Filters

Add to sidebar section (around line 80):
```python
# Example: Add location filter
locations = ['All'] + sorted(df['location'].unique().tolist())
selected_location = st.selectbox("Location", locations)
```

---

## Troubleshooting

### "No data found" Error

**Problem**: No CSV files in `data/` directory

**Solution**:
```bash
python test_pipeline.py
```

### Charts Not Displaying

**Problem**: Missing Plotly

**Solution**:
```bash
pip install plotly
```

### Dashboard Won't Start

**Problem**: Streamlit not installed or wrong directory

**Solution**:
```bash
source venv/bin/activate
pip install -r requirements.txt
cd /path/to/project
streamlit run streamlit_app.py
```

### Browser Doesn't Open

**Solution**: Manually navigate to `http://localhost:8501`

### Port Already in Use

**Solution**: Kill existing Streamlit process or use different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## Performance

- **Load Time**: <2 seconds for 100 jobs
- **Filtering**: Instant (in-memory)
- **Charts**: Real-time updates
- **Export**: <1 second

**Optimization Tips:**
- Dashboard caches data automatically
- Reload data: Click "☰" menu → "Rerun"
- For 1000+ jobs: Consider pagination

---

## Deployment Options

### Option 1: Local (Current)
```bash
streamlit run streamlit_app.py
```

### Option 2: Streamlit Cloud (Free)
1. Push to GitHub (already done ✅)
2. Go to `share.streamlit.io`
3. Connect GitHub repo
4. Deploy `streamlit_app.py`
5. Share public URL

### Option 3: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## Next Enhancements

### Potential Features:
1. **Real-time updates**: Auto-refresh every N minutes
2. **Email alerts**: Notify when high-relevance jobs appear
3. **Advanced analytics**: Company hiring velocity, category trends
4. **Comparison view**: Week-over-week changes
5. **Company profiles**: Deep-dive pages for each company
6. **Saved filters**: Bookmark common filter combinations
7. **API endpoint**: Programmatic access to data

---

## Support

**Documentation**: See `README.md`, `PHASE2_COMPLETE.md`
**Issues**: Create GitHub issue
**Questions**: Check `TEST_RESULTS.md` for common issues

---

## Credits

Built with:
- **Streamlit**: Dashboard framework
- **Plotly**: Interactive charts
- **Pandas**: Data manipulation
- **Python**: Core language

Part of the **SaaS Security Signal Engine** project for Obsidian Security.
