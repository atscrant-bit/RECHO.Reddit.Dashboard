"""
RECHO Reddit Performance Console
Professional Marketing Analytics Dashboard
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="RECHO | Reddit Performance Console",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - WHITE & RED THEME
# ============================================================================
st.markdown("""
<style>
    .main {
        background: #FFFFFF;
    }
    
    h1 {
        color: #D43E2B;
        font-weight: 700;
    }
    
    .stMetric {
        background: #FFFFFF;
        border: 2px solid #F0F0F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .stMetric:hover {
        border-color: #D43E2B;
        box-shadow: 0 4px 16px rgba(212,62,43,0.15);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetricLabel"] {
        color: #666666;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    [data-testid="stMetricValue"] {
        color: #1A1A1A;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stButton>button {
        background-color: #D43E2B;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background-color: #B53325;
        box-shadow: 0 4px 12px rgba(212,62,43,0.3);
    }
    
    .alert-success {
        background: #D4EDDA;
        border-left: 4px solid #28A745;
        padding: 16px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-warning {
        background: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 16px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-danger {
        background: #F8D7DA;
        border-left: 4px solid #D43E2B;
        padding: 16px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    try:
        with open('dashboard_metrics.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("⚠️ Error: dashboard_metrics.json not found")
        st.info("Please ensure the data file is in your repository")
        st.stop()
    except json.JSONDecodeError:
        st.error("⚠️ Error: Invalid JSON format in dashboard_metrics.json")
        st.stop()

data = load_data()

# ============================================================================
# HEADER
# ============================================================================
col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    st.markdown("<h1 style='text-align: center;'>🎯 RECHO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Reddit Performance Console</p>", unsafe_allow_html=True)

with col3:
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%b %d, %Y')}")
    st.caption("📊 Mock Data Active")

st.markdown("---")

# ============================================================================
# GLOBAL CONTROLS
# ============================================================================
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    date_range = st.selectbox(
        "📅 Date Range",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
        index=1
    )

with col2:
    all_accounts = ["All Accounts"] + [acc['account_name'] for acc in data['accounts']['comparison']]
    account_filter = st.multiselect(
        "👤 Accounts",
        all_accounts,
        default=["All Accounts"]
    )

with col3:
    export_btn = st.button("📥 Export Report")
    if export_btn:
        st.success("Export feature coming soon!")

st.markdown("---")

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.title("📍 Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "📊 Overview",
        "🌱 Organic Performance", 
        "💰 Paid Ads",
        "📢 Brand Monitoring",
        "👥 Accounts",
        "🧠 Strategic Insights"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Quick Stats")

total_sessions = sum(t['sessions'] for t in data['traffic']['organic_vs_paid'])
total_conversions = sum(t['conversions'] for t in data['traffic']['organic_vs_paid'])
total_revenue = sum(c['revenue'] for c in data['paid']['campaign_summary'])

st.sidebar.metric("Sessions", f"{total_sessions:,}")
st.sidebar.metric("Conversions", f"{total_conversions:,}")
st.sidebar.metric("Revenue", f"${total_revenue:,.0f}")

# ============================================================================
# OVERVIEW TAB
# ============================================================================
if page == "📊 Overview":
    st.header("Executive Overview")
    
    # Calculate KPIs
    total_spend = sum(c['spend'] for c in data['paid']['campaign_summary'])
    blended_roas = total_revenue / total_spend if total_spend > 0 else 0
    total_karma = sum(acc['total_karma'] for acc in data['accounts']['comparison'])
    avg_cvr = (total_conversions / total_sessions * 100) if total_sessions > 0 else 0
    
    # KPI Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Revenue", f"${total_revenue:,.0f}", delta="+22.3%")
    
    with col2:
        st.metric("📈 ROAS", f"{blended_roas:.2f}", delta="+8.7%")
    
    with col3:
        st.metric("🎯 Conversions", f"{total_conversions:,}", delta="+18.5%")
    
    with col4:
        st.metric("⭐ Total Karma", f"{total_karma:,}", delta="+15.8%")
    
    # KPI Row 2
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌐 Traffic", f"{total_sessions:,}", delta="+14.2%")
    
    with col2:
        st.metric("📊 CVR", f"{avg_cvr:.2f}%", delta="+3.2%")
    
    with col3:
        total_posts = sum(s['post_count'] for s in data['organic']['subreddit_performance'])
        st.metric("📝 Posts", f"{total_posts}", delta="+12")
    
    with col4:
        sentiment = data['brand']['sentiment_ratio']
        st.metric("😊 Sentiment", f"{sentiment}%", delta="+2.1%")
    
    st.markdown("---")
    
    # Insights
    st.subheader("💡 Key Insights")
    
    st.markdown("""
    <div class='alert-success'>
    <strong>✅ Strong Performance:</strong> Reddit-driven conversions up 18.5% with ROAS at 3.59. 
    Organic engagement maintaining 83%+ upvote rate.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='alert-warning'>
    <strong>⚠️ Attention Needed:</strong> Q1 campaign CPA slightly above target. 
    Consider reallocating budget to higher-performing placements.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Activity Chart
    st.subheader("📈 Activity & Traffic Trend")
    
    daily_data = pd.DataFrame(data['organic']['daily_metrics'][:30])
    daily_data['date'] = pd.to_datetime(daily_data['date'])
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=daily_data['date'],
            y=daily_data['posts'],
            name="Posts",
            line=dict(color='#D43E2B', width=2),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=daily_data['date'],
            y=daily_data['clicks'],
            name="Traffic",
            line=dict(color='#666666', width=2)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        template='simple_white'
    )
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Posts", secondary_y=False)
    fig.update_yaxes(title_text="Clicks", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Tables
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Subreddits")
        df_subs = pd.DataFrame(data['traffic']['by_subreddit'][:5])
        df_subs = df_subs[['subreddit', 'sessions', 'conversions']]
        st.dataframe(df_subs, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("💰 Campaigns")
        df_camps = pd.DataFrame(data['paid']['campaign_summary'])
        df_camps['campaign_name'] = df_camps['campaign_name'].str.replace('_', ' ')
        df_camps = df_camps[['campaign_name', 'roas', 'conversions']]
        st.dataframe(df_camps, use_container_width=True, hide_index=True)

# ============================================================================
# ORGANIC TAB
# ============================================================================
elif page == "🌱 Organic Performance":
    st.header("Organic Performance")
    
    # KPIs
    total_posts = sum(s['post_count'] for s in data['organic']['subreddit_performance'])
    total_engagement = sum(s['total_upvotes'] + s['total_comments'] for s in data['organic']['subreddit_performance'])
    avg_engagement = sum(s['avg_engagement_rate'] for s in data['organic']['subreddit_performance']) / len(data['organic']['subreddit_performance'])
    total_karma = sum(s['total_karma'] for s in data['organic']['subreddit_performance'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Posts", f"{total_posts}")
    
    with col2:
        st.metric("🔥 Engagement", f"{total_engagement:,}", delta="+18.2%")
    
    with col3:
        st.metric("📊 Avg Rate", f"{avg_engagement:.2f}%")
    
    with col4:
        st.metric("🏆 Karma", f"{total_karma:,}", delta="+22.5%")
    
    st.markdown("---")
    
    # Karma Growth Chart
    st.subheader("📈 Karma Growth by Account")
    
    df_karma = pd.DataFrame(data['organic']['karma_velocity'])
    df_karma['date'] = pd.to_datetime(df_karma['date'])
    
    fig = px.line(
        df_karma,
        x='date',
        y='karma_velocity',
        color='account_name',
        labels={'karma_velocity': 'Karma/Day', 'account_name': 'Account'},
        color_discrete_sequence=['#D43E2B', '#FF6B5A', '#666666']
    )
    
    fig.update_layout(height=400, hovermode='x unified', template='simple_white')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Top Posts
    st.subheader("🌟 Top Posts")
    df_posts = pd.DataFrame(data['organic']['top_posts'][:10])
    df_posts = df_posts[['title', 'subreddit', 'upvotes', 'comments', 'engagement_rate']]
    st.dataframe(df_posts, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Subreddit Performance
    st.subheader("📍 Performance by Subreddit")
    df_subs = pd.DataFrame(data['organic']['subreddit_performance'])
    df_subs = df_subs[['subreddit', 'post_count', 'total_upvotes', 'ctr', 'avg_upvote_rate']]
    st.dataframe(df_subs, use_container_width=True, hide_index=True)

# ============================================================================
# PAID ADS TAB
# ============================================================================
elif page == "💰 Paid Ads":
    st.header("Paid Advertising")
    
    total_spend = sum(c['spend'] for c in data['paid']['campaign_summary'])
    total_revenue = sum(c['revenue'] for c in data['paid']['campaign_summary'])
    total_conversions = sum(c['conversions'] for c in data['paid']['campaign_summary'])
    avg_roas = total_revenue / total_spend if total_spend > 0 else 0
    avg_cpa = total_spend / total_conversions if total_conversions > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💵 Spend", f"${total_spend:,.0f}")
    
    with col2:
        st.metric("📈 ROAS", f"{avg_roas:.2f}", delta="+8.5%")
    
    with col3:
        st.metric("💰 CPA", f"${avg_cpa:.2f}", delta="-$2.50")
    
    with col4:
        st.metric("🎯 Conversions", f"{total_conversions:,}", delta="+12.8%")
    
    st.markdown("---")
    
    # Spend vs Conversions
    st.subheader("📊 Daily Spend vs Conversions")
    
    df_daily = pd.DataFrame(data['paid']['daily_metrics'][:30])
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    df_daily_agg = df_daily.groupby('date').agg({'spend': 'sum', 'conversions': 'sum'}).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=df_daily_agg['date'], y=df_daily_agg['spend'], name="Spend", marker_color='#D43E2B'),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=df_daily_agg['date'], y=df_daily_agg['conversions'], name="Conversions", line=dict(color='#28A745', width=3)),
        secondary_y=True
    )
    
    fig.update_layout(height=400, hovermode='x unified', template='simple_white')
    fig.update_yaxes(title_text="Spend ($)", secondary_y=False)
    fig.update_yaxes(title_text="Conversions", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Campaign Performance
    st.subheader("📋 Campaign Performance")
    
    df_campaigns = pd.DataFrame(data['paid']['campaign_summary'])
    df_campaigns['campaign_name'] = df_campaigns['campaign_name'].str.replace('_', ' ')
    df_display = df_campaigns[['campaign_name', 'spend', 'roas', 'cpa', 'conversions', 'revenue']]
    df_display['spend'] = df_display['spend'].apply(lambda x: f"${x:,.0f}")
    df_display['cpa'] = df_display['cpa'].apply(lambda x: f"${x:.2f}")
    df_display['revenue'] = df_display['revenue'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Subreddit ROAS
    st.subheader("🎯 ROAS by Subreddit")
    
    df_subs = pd.DataFrame(data['paid']['subreddit_performance'][:10])
    
    fig = go.Figure(data=[
        go.Bar(
            x=df_subs['subreddit'],
            y=df_subs['roas'],
            marker_color=['#28A745' if r >= 5 else '#D43E2B' if r >= 3 else '#FFA500' for r in df_subs['roas']],
            text=df_subs['roas'].round(2),
            textposition='outside'
        )
    ])
    
    fig.add_hline(y=3.0, line_dash="dash", line_color="gray", annotation_text="Target: 3.0")
    fig.update_layout(height=400, template='simple_white')
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# BRAND MONITORING TAB
# ============================================================================
elif page == "📢 Brand Monitoring":
    st.header("Brand Monitoring")
    
    total_mentions = sum(s['mention_count'] for s in data['brand']['by_subreddit'])
    sentiment_ratio = data['brand']['sentiment_ratio']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📢 Mentions", f"{total_mentions:,}", delta="+18.5%")
    
    with col2:
        st.metric("😊 Positive", f"{sentiment_ratio}%", delta="+2.1%")
    
    with col3:
        st.metric("📊 Daily Avg", f"{total_mentions/163:.1f}")
    
    with col4:
        st.metric("🏆 Share of Voice", "34.2%", delta="+5.1%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment Chart
        st.subheader("😊 Sentiment Distribution")
        
        df_sentiment = pd.DataFrame(data['brand']['sentiment_distribution'])
        df_sentiment['sentiment'] = df_sentiment['sentiment'].str.capitalize()
        
        colors = {'Positive': '#28A745', 'Neutral': '#FFA500', 'Negative': '#D43E2B'}
        
        fig = go.Figure(data=[go.Pie(
            labels=df_sentiment['sentiment'],
            values=df_sentiment['mention_count'],
            hole=.6,
            marker_colors=[colors[s] for s in df_sentiment['sentiment']]
        )])
        
        fig.update_layout(
            height=400,
            annotations=[dict(text=f'{sentiment_ratio}%<br>Positive', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Share of Voice
        st.subheader("🏆 Share of Voice")
        
        competitors = [
            {'brand': 'Your Brand', 'sov': 34.2},
            {'brand': 'Competitor A', 'sov': 28.5},
            {'brand': 'Competitor B', 'sov': 22.1},
            {'brand': 'Competitor C', 'sov': 15.2}
        ]
        df_comp = pd.DataFrame(competitors)
        
        fig = go.Figure(data=[
            go.Bar(
                x=df_comp['brand'],
                y=df_comp['sov'],
                marker_color=['#D43E2B' if b == 'Your Brand' else '#CCCCCC' for b in df_comp['brand']]
            )
        ])
        
        fig.update_layout(height=400, template='simple_white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Mentions Over Time
    st.subheader("📈 Mention Volume")
    
    df_trend = pd.DataFrame(data['brand']['mention_trend'][:30])
    df_trend['date'] = pd.to_datetime(df_trend['date'])
    
    fig = px.area(df_trend, x='date', y='mention_count', color_discrete_sequence=['#D43E2B'])
    fig.update_layout(height=400, template='simple_white')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Alerts
    st.subheader("🚨 Alerts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='alert-warning'>
        <h4>⚠️ Mentions Spike</h4>
        <p><strong>Date:</strong> Feb 8, 2026</p>
        <p><strong>Increase:</strong> +145% vs avg</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='alert-success'>
        <h4>✅ Sentiment Up</h4>
        <p><strong>Period:</strong> Last 7 days</p>
        <p><strong>Change:</strong> +2.1% positive</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ACCOUNTS TAB
# ============================================================================
elif page == "👥 Accounts":
    st.header("Account Analysis")
    
    df_accounts = pd.DataFrame(data['accounts']['comparison'])
    df_accounts['posts_per_week'] = (df_accounts['total_posts'] / (df_accounts['account_age_days'] / 7)).round(1)
    df_accounts['karma_velocity'] = (df_accounts['total_karma'] / (df_accounts['account_age_days'] / 7)).round(0)
    
    st.subheader("📊 Performance Comparison")
    
    df_display = df_accounts[[
        'account_name', 'account_type', 'total_karma', 
        'posts_per_week', 'karma_velocity', 'total_clicks'
    ]]
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Individual accounts
    for idx, account in df_accounts.iterrows():
        with st.expander(f"📊 {account['account_name']}", expanded=(idx==0)):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Karma", f"{account['total_karma']:,}")
            
            with col2:
                st.metric("Posts/Week", f"{account['posts_per_week']}")
            
            with col3:
                st.metric("Karma/Week", f"+{account['karma_velocity']}")
            
            with col4:
                st.metric("Clicks", f"{account['total_clicks']:,}")

# ============================================================================
# STRATEGIC INSIGHTS TAB
# ============================================================================
elif page == "🧠 Strategic Insights":
    st.header("Strategic Insights & Content Lab")
    
    st.subheader("📝 Weekly AI Summary")
    
    summary = st.text_area(
        "AI-Generated Insights",
        value="""**Week of February 3-9, 2026**

🎯 **Highlights:**
• Holiday campaign exceeded targets: 3.79 ROAS (+12% vs target)
• r/Sneakers engagement up 23%
• Brand sentiment at 93% positive (+2.1%)

⚠️ **Action Items:**
• Q1 campaign CPA at $27.08 (target: $25) - reallocate budget
• r/Fitness underperforming - refresh creative
• Response time 4.2hrs - aim for <3hrs

💡 **Recommendations:**
1. Increase budget to top-performing subreddits
2. Test video content in underperforming areas
3. Launch community appreciation series
        """,
        height=300
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🤖 Generate"):
            st.info("Coming soon!")
    
    st.markdown("---")
    
    # Content Reliability
    st.subheader("🎯 Content Reliability")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 40px; background: #F8F8F8; border-radius: 12px;'>
            <div style='font-size: 4rem; font-weight: 800; color: #D43E2B;'>87%</div>
            <div style='font-size: 1.2rem; color: #666;'>RELIABILITY SCORE</div>
            <p style='color: #28A745; font-weight: 600; margin-top: 15px;'>✅ ABOVE TARGET (85%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 40px; background: #F8F8F8; border-radius: 12px;'>
            <div style='font-size: 4rem; font-weight: 800; color: #28A745;'>12%</div>
            <div style='font-size: 1.2rem; color: #666;'>AI DETECTION</div>
            <p style='color: #28A745; font-weight: 600; margin-top: 15px;'>✅ LOW RISK</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action Items
    st.subheader("✅ Recommended Actions")
    
    actions = [
        {'Priority': '🔴 High', 'Action': 'Respond to negative sentiment spike', 'Deadline': '2026-02-13'},
        {'Priority': '🟡 Medium', 'Action': 'A/B test new creative', 'Deadline': '2026-02-17'},
        {'Priority': '🟢 Low', 'Action': 'Update content calendar', 'Deadline': '2026-02-20'}
    ]
    
    df_actions = pd.DataFrame(actions)
    st.dataframe(df_actions, use_container_width=True, hide_index=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>🎯 RECHO</strong> | Reddit Performance Console v1.0</p>
    <p style='font-size: 0.9rem;'>Last Updated: {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
</div>
""", unsafe_allow_html=True)
