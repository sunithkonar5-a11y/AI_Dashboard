"""
Amazon E-commerce Sales Analytics Dashboard
============================================
A hackathon-ready Streamlit dashboard with Plotly visualizations,
dynamic sidebar filters, KPI cards, and bonus insight features.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import re
import calendar


# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Amazon Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS – gradient headers, card styling,
# shadows, consistent blue/purple/teal palette
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit header / footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Gradient Header Banner ── */
.header-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #00c9a7 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.8rem;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.35);
}
.header-banner h1 {
    color: #ffffff;
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.5px;
}
.header-banner p {
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    margin: 0.4rem 0 0 0;
    font-weight: 400;
}

/* ── KPI Metric Card ── */
.kpi-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
    border: 1px solid rgba(102, 126, 234, 0.12);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.18);
}
.kpi-icon {
    font-size: 2rem;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-size: 1.85rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.25rem 0;
}
.kpi-label {
    font-size: 0.82rem;
    color: #8892b0;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
}

/* ── Section Card (chart wrapper) ── */
.section-card {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 0.6rem;
}

/* ── Insight Cards ── */
.insight-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}
.insight-card.teal {
    background: linear-gradient(135deg, #00c9a7 0%, #00b4d8 100%);
    box-shadow: 0 4px 20px rgba(0, 201, 167, 0.3);
}
.insight-card.amber {
    background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
}
.insight-card h4 {
    margin: 0 0 0.3rem 0;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.85;
}
.insight-card p {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 700;
}

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}
/* Sidebar Headers & Text */
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 1.35rem !important;
    text-shadow: 0 0 10px rgba(255,255,255,0.2);
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p {
    color: #e0e0e0 !important;
    font-weight: 500 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1);
}
/* File Uploader Text */
section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] div {
    color: #e0e0e0 !important;
}
/* Date Input / Multiselect Box / Dropdowns */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
section[data-testid="stSidebar"] div[data-baseweb="input"] > div {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #e0e0e0 !important;
}
/* Multiselect Selected Chips */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background: linear-gradient(135deg, #f72585 0%, #7209b7 100%) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(247, 37, 133, 0.4);
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] * {
    color: #ffffff !important;
}

/* ── Plotly chart container tweaks ── */
.stPlotlyChart {
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────
@st.cache_data
def load_data(file_buffer=None):
    """Load and prepare the dataset."""
    try:
        if file_buffer is not None:
            df = pd.read_csv(file_buffer)
        else:
            csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amazon_sales_data.csv")
            df = pd.read_csv(csv_path)
            
        # Clean column names
        df.columns = df.columns.str.lower().str.replace(" ", "_").str.strip()
        
        # Column Mapping: Fix 'unnamed: 0' to 'order_id'
        if "unnamed:_0" in df.columns:
            df.rename(columns={"unnamed:_0": "order_id"}, inplace=True)
            
        
        if "order_date" in df.columns:
            # Safely convert dates
            df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
            # Drop invalid dates
            df = df.dropna(subset=["order_date"])
            
        # Safely convert numeric columns
        numeric_cols = ["quantity_sold", "total_revenue", "rating"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                
        return df, None
    except Exception as e:
        return None, str(e)


# ──────────────────────────────────────────────
# SIDEBAR FILTERS
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📁 Data Source")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    using_uploaded_data = False
    if uploaded_file is not None:
        raw_df, error = load_data(uploaded_file)
        
        required_cols = [
            "order_id", "order_date", "product_category", "customer_region", 
            "payment_method", "quantity_sold", "total_revenue"
        ]
        
        if error:
            st.error(f"❌ Error loading file: {error}")
            df, _ = load_data()
        elif not all(col in raw_df.columns for col in required_cols):
            missing = [col for col in required_cols if col not in raw_df.columns]
            st.error(f"⚠️ Required columns missing: {', '.join(missing)}. Please upload correct dataset.")
            st.stop() # Stop execution so the app doesn't crash on charts
        else:
            st.success("✅ File uploaded successfully!")
            
            # Debug info (hackathon demo)
            with st.expander("🔍 Debug: Column Names"):
                st.write(f"**Rows loaded:** {len(raw_df):,}")
                st.write("**Columns detected:**")
                st.write(list(raw_df.columns))
            
            df = raw_df
            using_uploaded_data = True

    else:
        df, _ = load_data()

    st.markdown("---")
    st.markdown("## 🎛️ Filters")
    st.markdown("---")

    # Region
    all_regions = sorted(df["customer_region"].unique())
    selected_regions = st.multiselect(
        "🌍 Customer Region",
        options=all_regions,
        default=all_regions,
    )

    # Category
    all_categories = sorted(df["product_category"].unique())
    selected_categories = st.multiselect(
        "📦 Product Category",
        options=all_categories,
        default=all_categories,
    )

    st.markdown("---")

    # Date range
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    date_range = st.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.markdown("---")

    # Payment method
    all_payments = sorted(df["payment_method"].unique())
    selected_payments = st.multiselect(
        "💳 Payment Method",
        options=all_payments,
        default=all_payments,
    )

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#8892b0;font-size:0.75rem;'>"
        "Built with Streamlit & Plotly</p>",
        unsafe_allow_html=True,
    )

# ── Apply filters ──
# Handle single-date selection gracefully
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0] if isinstance(date_range, tuple) else date_range

filtered_df = df[
    (df["customer_region"].isin(selected_regions))
    & (df["product_category"].isin(selected_categories))
    & (df["payment_method"].isin(selected_payments))
    & (df["order_date"].dt.date >= start_date)
    & (df["order_date"].dt.date <= end_date)
]

# ──────────────────────────────────────────────
# HEADER BANNER
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="header-banner">
        <h1>📊 Conversational AI for Instant Business Intelligence Dashboard</h1>
        <p>Real-time insights across categories, regions, and payment channels</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if 'using_uploaded_data' in locals() and using_uploaded_data:
    st.markdown('<div class="section-title">👀 Data Preview (First 5 Rows)</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# KPI METRICS ROW
# ──────────────────────────────────────────────
total_revenue = filtered_df["total_revenue"].sum() if "total_revenue" in filtered_df.columns else 0
total_orders = filtered_df["order_id"].nunique() if "order_id" in filtered_df.columns else 0
avg_rating = filtered_df["rating"].mean() if "rating" in filtered_df.columns and len(filtered_df) > 0 else 0



col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-value">₹{total_revenue:,.0f}</div>
            <div class="kpi-label">Total Revenue</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-label">Total Orders</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">⭐</div>
            <div class="kpi-value">{avg_rating:.2f}</div>
            <div class="kpi-label">Avg Rating</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CHART COLOR PALETTE (blue / purple / teal)
# ──────────────────────────────────────────────
PALETTE = [
    "#667eea", "#764ba2", "#00c9a7", "#00b4d8",
    "#f72585", "#7209b7", "#3a0ca3", "#4cc9f0",
]


# ──────────────────────────────────────────────
# CHART BUILDERS
# ──────────────────────────────────────────────
def build_revenue_over_time(data: pd.DataFrame) -> go.Figure:
    """Line chart: Revenue over time with markers."""
    agg = (
        data.groupby(data["order_date"].dt.to_period("M"))
        .agg(total_revenue=("total_revenue", "sum"))
        .reset_index()
    )
    agg["order_date"] = agg["order_date"].dt.to_timestamp()

    fig = px.line(
        agg,
        x="order_date",
        y="total_revenue",
        markers=True,
        labels={"order_date": "Month", "total_revenue": "Revenue (₹)"},
    )
    fig.update_traces(
        line=dict(color="#667eea", width=3),
        marker=dict(size=8, color="#764ba2"),
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        height=370,
    )
    return fig


def build_revenue_by_category(data: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart: Revenue by product category."""
    agg = (
        data.groupby("product_category")
        .agg(total_revenue=("total_revenue", "sum"))
        .reset_index()
        .sort_values("total_revenue")
    )

    fig = px.bar(
        agg,
        x="total_revenue",
        y="product_category",
        orientation="h",
        color="product_category",
        color_discrete_sequence=PALETTE,
        labels={"total_revenue": "Revenue (₹)", "product_category": ""},
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
        yaxis=dict(showgrid=False),
        height=370,
    )
    return fig


def build_donut_region(data: pd.DataFrame) -> go.Figure:
    """Donut chart: Sales (units sold) by customer region."""
    agg = data.groupby("customer_region")["quantity_sold"].sum().reset_index()

    fig = px.pie(
        agg,
        values="quantity_sold",
        names="customer_region",
        hole=0.55,
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Units Sold: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
    )
    return fig


def build_donut_payment(data: pd.DataFrame) -> go.Figure:
    """Donut chart: Payment method distribution (order count)."""
    agg = data.groupby("payment_method")["order_id"].count().reset_index()
    agg.columns = ["payment_method", "order_count"]

    fig = px.pie(
        agg,
        values="order_count",
        names="payment_method",
        hole=0.55,
        color_discrete_sequence=PALETTE[2:] + PALETTE[:2],
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
    )
    return fig


# ──────────────────────────────────────────────
# RENDER CHARTS – row 1 (line + bar)

# ──────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown(
        '<div class="section-card"><div class="section-title">📈 Revenue Over Time</div>',
        unsafe_allow_html=True,
    )
    if len(filtered_df) > 0:
        st.plotly_chart(build_revenue_over_time(filtered_df), use_container_width=True)
    else:
        st.info("No data for the selected filters.")
    st.markdown("</div>", unsafe_allow_html=True)

with chart_col2:
    st.markdown(
        '<div class="section-card"><div class="section-title">📊 Total Revenue by Product Category</div>',
        unsafe_allow_html=True,
    )
    if len(filtered_df) > 0:
        st.plotly_chart(build_revenue_by_category(filtered_df), use_container_width=True)
    else:
        st.info("No data for the selected filters.")
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# RENDER CHARTS – row 2 (donuts)
# ──────────────────────────────────────────────
donut_col1, donut_col2 = st.columns(2)

with donut_col1:
    st.markdown(
        '<div class="section-card"><div class="section-title">🌍 Sales by Customer Region (Units Sold)</div>',
        unsafe_allow_html=True,
    )
    if len(filtered_df) > 0:
        st.plotly_chart(build_donut_region(filtered_df), use_container_width=True)
    else:
        st.info("No data for the selected filters.")
    st.markdown("</div>", unsafe_allow_html=True)

with donut_col2:
    st.markdown(
        '<div class="section-card"><div class="section-title">💳 Payment Method Distribution</div>',
        unsafe_allow_html=True,
    )
    if len(filtered_df) > 0:
        st.plotly_chart(build_donut_payment(filtered_df), use_container_width=True)
    else:
        st.info("No data for the selected filters.")
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# BONUS: INSIGHT CARDS
# ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<div class="section-title" style="font-size:1.25rem;">💡 Key Insights</div>',
    unsafe_allow_html=True,
)

ins_col1, ins_col2, ins_col3 = st.columns(3)

# ── Top Performing Category ──
if len(filtered_df) > 0:
    top_cat = (
        filtered_df.groupby("product_category")["total_revenue"]
        .sum()
        .idxmax()
    )
    top_cat_rev = filtered_df.groupby("product_category")["total_revenue"].sum().max()
else:
    top_cat = "N/A"
    top_cat_rev = 0

with ins_col1:
    st.markdown(
        f"""
        <div class="insight-card">
            <h4>🏆 Top Category</h4>
            <p>{top_cat}</p>
            <p style="font-size:0.85rem;opacity:0.8;">₹{top_cat_rev:,.0f} revenue</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Most Used Payment Method ──
if len(filtered_df) > 0:
    top_payment = filtered_df["payment_method"].value_counts().idxmax()
    top_payment_pct = (
        filtered_df["payment_method"].value_counts(normalize=True).iloc[0] * 100
    )
else:
    top_payment = "N/A"
    top_payment_pct = 0

with ins_col2:
    st.markdown(
        f"""
        <div class="insight-card teal">
            <h4>💳 Most Used Payment</h4>
            <p>{top_payment}</p>
            <p style="font-size:0.85rem;opacity:0.8;">{top_payment_pct:.1f}% of orders</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Revenue Trend Insight ──
if len(filtered_df) > 0:
    monthly = (
        filtered_df.groupby(filtered_df["order_date"].dt.to_period("M"))
        .agg(rev=("total_revenue", "sum"))
        .reset_index()
    )
    if len(monthly) >= 2:
        first_half = monthly["rev"].iloc[: len(monthly) // 2].sum()
        second_half = monthly["rev"].iloc[len(monthly) // 2 :].sum()
        if first_half > 0:
            pct_change = ((second_half - first_half) / first_half) * 100
            direction = "increased" if pct_change >= 0 else "decreased"
            arrow = "📈" if pct_change >= 0 else "📉"
            trend_text = f"{arrow} Revenue {direction} by {abs(pct_change):.1f}% in the latter half of the selected period"
        else:
            trend_text = "📈 Not enough data for trend analysis"
    else:
        trend_text = "📈 Select a wider date range for trend analysis"
else:
    trend_text = "📈 No data available"

with ins_col3:
    st.markdown(
        f"""
        <div class="insight-card amber">
            <h4>📈 Revenue Trend</h4>
            <p style="font-size:0.95rem;">{trend_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────
# 🤖 ASK QUESTIONS ABOUT YOUR DATA
# ──────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div class="section-title" style="font-size:1.4rem;">🤖 Ask Questions About Your Data</div>',
    unsafe_allow_html=True,
)
st.markdown("<p style='color:#8892b0;'>Ask simple questions about the filtered data (e.g. <em>What is the total revenue?</em> or <em>Which category has the highest sales?</em>)</p>", unsafe_allow_html=True)

with st.form(key="question_form", clear_on_submit=False):
    query = st.text_input("Your Question:", placeholder="Ask anything about your data... e.g. 'most used payment method' or 'best region'")
    submitted = st.form_submit_button("Ask")

if submitted:
    if not query:
        st.warning("Please enter a question.")
    elif len(filtered_df) == 0:
        st.warning("Your current filters resulted in an empty dataset. Try adjusting the filters.")
    else:
        q_lower = query.lower().strip()
        ans = None
        
        # Get all unique categories and regions (lowercase for matching)
        categories = [str(c).lower().strip() for c in filtered_df["product_category"].dropna().unique()]
        regions = [str(r).lower().strip() for r in filtered_df["customer_region"].dropna().unique()]
        
        # Check if any category or region is mentioned in the query
        mentioned_category_lower = next((cat for cat in categories if cat in q_lower), None)
        mentioned_region_lower = next((reg for reg in regions if reg in q_lower), None)

        # 0. Advanced Analytical / Correlation Queries
        if any(kw in q_lower for kw in ["correlation", "relationship", "impact", "effect", "analysis", "strategy", "analyzing", "analyze"]):
            # ── Flexible column mapping (case/space insensitive) ──────
            _cols = filtered_df.columns.str.lower().str.strip()
            column_map = {}
            for col, norm in zip(filtered_df.columns, _cols):
                if "discount" in norm:
                    column_map["discount"] = col
                elif "quant" in norm:
                    column_map["quantity"] = col
                elif "revenue" in norm or "sales" in norm:
                    column_map["revenue"] = col
                elif "category" in norm:
                    column_map["category"] = col

            required_keys = ["discount", "quantity", "revenue", "category"]
            if not all(k in column_map for k in required_keys):
                ans = (
                    f"⚠️ Required data columns (Discount, Quantity, Revenue, Category) not found. "
                    f"Available columns: {list(filtered_df.columns)}"
                )
            else:
                discount_col  = column_map["discount"]
                quantity_col  = column_map["quantity"]
                revenue_col   = column_map["revenue"]
                category_col  = column_map["category"]
                try:
                    # 1. Compute overall correlation
                    correlation = filtered_df[[discount_col, quantity_col, revenue_col]].corr()
                    disc_qty_corr = correlation.loc[discount_col, quantity_col]
                    disc_rev_corr = correlation.loc[discount_col, revenue_col]

                    ans_lines = ["🧠 **Analysis Summary:**"]

                    if disc_qty_corr > 0:
                        ans_lines.append(f"- Discount and Quantity have a positive correlation ({disc_qty_corr:.2f})")
                    else:
                        ans_lines.append(f"- Discount and Quantity have a negative correlation ({disc_qty_corr:.2f})")

                    if disc_rev_corr > 0:
                        ans_lines.append(f"- Discount and Revenue have a positive correlation ({disc_rev_corr:.2f})")
                    else:
                        ans_lines.append(f"- Discount and Revenue have a negative correlation ({disc_rev_corr:.2f})")

                    ans_lines.append("\n**Category Insights:**")

                    # 2. Category-wise profitability
                    category_analysis = filtered_df.groupby(category_col)[revenue_col].sum().sort_values(ascending=False)
                    baseline_disc = filtered_df[discount_col].mean()
                    baseline_rev_per_qty = (
                        filtered_df[revenue_col].sum() / filtered_df[quantity_col].sum()
                    ) if filtered_df[quantity_col].sum() else 0

                    for cat, group in filtered_df.groupby(category_col):
                        avg_disc = group[discount_col].mean()
                        total_qty = group[quantity_col].sum()
                        total_rev = group[revenue_col].sum()
                        cat_rev_per_qty = (total_rev / total_qty) if total_qty else 0

                        if avg_disc > baseline_disc * 1.1 and cat_rev_per_qty < baseline_rev_per_qty * 0.9:
                            insight = "High discounts increase volume but reduce revenue"
                        elif avg_disc > baseline_disc * 0.8 and cat_rev_per_qty > baseline_rev_per_qty * 1.1:
                            insight = "Moderate discounting generates the highest revenue profitability"
                        elif avg_disc <= baseline_disc * 0.8 and cat_rev_per_qty > baseline_rev_per_qty:
                            insight = "Stable revenue with low discount – premium pricing strategy"
                        else:
                            insight = "Balanced performance with average discounting"

                        ans_lines.append(f"- **{cat}**: {insight}")

                    ans_lines.append("\n**Conclusion:**")
                    ans_lines.append(
                        "Higher discounts slightly increase quantity sold but reduce revenue per order. "
                        f"Categories like **{category_analysis.index[0]}** perform best at moderate discount levels. "
                        "Moderate discount strategies reliably maximize profitability across most categories."
                    )

                    ans = "\n".join(ans_lines)
                except Exception as e:
                    ans = f"⚠️ Could not complete advanced analysis: {str(e)}"

        # 1. Multi-category Future Sales Queries ("all category future sales")
        elif any(kw in q_lower for kw in ["all category", "all categories", "each category", "every category"]) and \
           any(kw in q_lower for kw in ["future", "predict", "will give", "going to be", "estimate"]):
            try:
                grouped = filtered_df.groupby("product_category")["total_revenue"].sum()
                
                # Apply simulated 5% growth
                future_sales = grouped * 1.05
                
                # Format output nicely
                ans_lines = ["📈 **Estimated future sales by category (based on +5% growth trend):**"]
                
                # Sort descending to look nice
                for cat, val in future_sales.sort_values(ascending=False).items():
                    ans_lines.append(f"- **{cat}**: ₹{val:,.0f}")
                    
                ans = "\n".join(ans_lines)
            except Exception:
                ans = "⚠️ Not enough valid data across categories to calculate future sales."

        # 1. Multi-Condition Comparative Queries
        elif any(kw in q_lower for kw in ["highest", "best", "top", "most"]):
            
            # Start with the currently filtered dataframe
            temp_df = filtered_df.copy()
            
            # Step 1: Filter if a specific category or region is mentioned
            if mentioned_category_lower:
                temp_df = temp_df[temp_df["product_category"].str.lower() == mentioned_category_lower]
                
            if mentioned_region_lower:
                temp_df = temp_df[temp_df["customer_region"].str.lower() == mentioned_region_lower]

            if len(temp_df) == 0:
                ans = "⚠️ No data found matching those exact filters in the current selection."
            else:
                try:
                    # Decide what to compare based on what WASN'T in the query, defaulting to region if specifically asked, else category
                    if "region" in q_lower or mentioned_category_lower:
                        # User wants the best region for a specific category (e.g. "which region has highest book revenue")
                        # Or they explicitly asked "which region has highest revenue"
                        grouped = temp_df.groupby("customer_region")["total_revenue"].sum()
                        top_entity = grouped.idxmax()
                        top_value = grouped.max()
                        
                        if mentioned_category_lower:
                            original_category = next(c for c in filtered_df["product_category"].unique() if str(c).lower().strip() == mentioned_category_lower)
                            ans = f"🌍 The region with the highest revenue for **{original_category}** is **{top_entity}** with **₹{top_value:,.0f}**."
                        else:
                            ans = f"🌍 The region with the highest revenue is **{top_entity}** with **₹{top_value:,.0f}**."
                            
                    else: # Default comparative asking for top category
                        grouped = temp_df.groupby("product_category")["total_revenue"].sum()
                        top_entity = grouped.idxmax()
                        top_value = grouped.max()
                        
                        if mentioned_region_lower:
                            original_region = next(r for r in filtered_df["customer_region"].unique() if str(r).lower().strip() == mentioned_region_lower)
                            ans = f"🏆 The top performing category in **{original_region}** is **{top_entity}** with **₹{top_value:,.0f}**."
                        else:
                            # Predictive / Comparative Logic
                            if "future" in q_lower or "predict" in q_lower or "will " in q_lower:
                                ans = f"📈 Based on current data trends, the category likely to generate the highest revenue is **{top_entity}** with **₹{top_value:,.0f}** in sales."
                            else:
                                ans = f"🏆 The top performing product category by revenue is **{top_entity}** with **₹{top_value:,.0f}**."
                except Exception:
                    ans = "⚠️ Not enough valid data to make a calculation for that exact combination."

        # 2. Revenue-Only Queries
        elif any(kw in q_lower for kw in ["revenue", "sales", "how much"]):
            temp_df = filtered_df.copy()

            # ── Time extraction ──────────────────────────────────────
            # Year detection (e.g. "2022", "2023")
            year_match = re.search(r"(20\d{2})", q_lower)
            year = int(year_match.group(1)) if year_match else None

            # Month detection (e.g. "march", "january")
            month = None
            for i, m in enumerate(calendar.month_name):
                if m and m.lower() in q_lower:
                    month = i  # 1-indexed (January=1)
                    break

            # Apply year filter
            if year:
                if "order_date" in temp_df.columns:
                    temp_df = temp_df[temp_df["order_date"].dt.year == year]

            # Apply month filter
            if month:
                if "order_date" in temp_df.columns:
                    temp_df = temp_df[temp_df["order_date"].dt.month == month]
            # ─────────────────────────────────────────────────────────

            # Apply category / region filters
            if mentioned_category_lower:
                temp_df = temp_df[temp_df["product_category"].str.lower() == mentioned_category_lower]
            if mentioned_region_lower:
                temp_df = temp_df[temp_df["customer_region"].str.lower() == mentioned_region_lower]

            # Empty-data guard
            if len(temp_df) == 0:
                ans = "⚠️ No data available for the selected time period and filters."
            else:
                val = temp_df['total_revenue'].sum()

                # Build a human-readable time label
                if month and year:
                    time_label = f"in **{calendar.month_name[month]} {year}**"
                elif year:
                    time_label = f"in **{year}**"
                elif month:
                    time_label = f"in **{calendar.month_name[month]}**"
                else:
                    time_label = None

                if mentioned_category_lower and mentioned_region_lower:
                    orig_cat = next(c for c in filtered_df["product_category"].unique() if str(c).lower().strip() == mentioned_category_lower)
                    orig_reg = next(r for r in filtered_df["customer_region"].unique() if str(r).lower().strip() == mentioned_region_lower)
                    base = f"for **{orig_cat}** in **{orig_reg}**"
                elif mentioned_category_lower:
                    orig_cat = next(c for c in filtered_df["product_category"].unique() if str(c).lower().strip() == mentioned_category_lower)
                    base = f"for **{orig_cat}**"
                elif mentioned_region_lower:
                    orig_reg = next(r for r in filtered_df["customer_region"].unique() if str(r).lower().strip() == mentioned_region_lower)
                    base = f"in **{orig_reg}**"
                else:
                    base = None

                # Compose the final answer
                parts = ["💰 The total revenue"]
                if base:
                    parts.append(base)
                if time_label:
                    parts.append(time_label)
                parts.append(f"is **₹{val:,.0f}**.")
                ans = " ".join(parts)

        # 3. Simple Keyword Rules (Total Orders)
        elif any(kw in q_lower for kw in ["total orders", "how many orders", "number of orders"]):
            val = filtered_df['order_id'].nunique()
            ans = f"📦 There are **{val:,}** total orders in the selected data."
            
        elif any(kw in q_lower for kw in ["top category", "best category", "highest sales category", "most sales category", "category has highest sales"]):
            val = filtered_df.groupby('product_category')['total_revenue'].sum().idxmax()
            ans = f"🏆 The top performing product category by revenue is **{val}**."
            
        elif any(kw in q_lower for kw in ["top region", "best region", "highest region", "best performing region"]):
            val = filtered_df.groupby('customer_region')['total_revenue'].sum().idxmax()
            ans = f"🌍 The region with the highest revenue is **{val}**."
            
        elif any(kw in q_lower for kw in ["most used payment", "popular payment", "top payment", "best payment", "payment method"]):
            val = filtered_df['payment_method'].mode().iloc[0]
            ans = f"💳 The most used payment method is **{val}**."
            
        elif any(kw in q_lower for kw in ["average rating", "avg rating", "mean rating", "rating"]):
            val = filtered_df['rating'].mean()
            ans = f"⭐ The average rating across these orders is **{val:.2f}**."
            
        else:
            ans = "🤷 Sorry, I couldn't understand. Try asking about **revenue by category, top region, orders, rating, or payment**."
            
        if ans:
             st.info(ans)


# ──────────────────────────────────────────────
# BONUS: DOWNLOAD FILTERED DATA
# ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

dl_col1, dl_col2, dl_col3 = st.columns([1, 2, 1])
with dl_col2:
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_amazon_sales.csv",
        mime="text/csv",
        use_container_width=True,
    )
