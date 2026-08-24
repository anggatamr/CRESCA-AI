"""
Cresca AI — Streamlit Enterprise Geospatial Portal & Audit Dashboard
Visualizes:
1. Spatiotemporal risk maps with interactive Folium markers
2. Real-time CDVI distribution & Poisson 90-day projections
3. Manual / Live background trigger with execution logs
4. Direct PDF Action Plan download & Firestore Audit Ledger
"""

import os
import json
from pathlib import Path
import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st

from src.agent.orchestrator import CrescaAgentOrchestrator
from src.persistence.firestore_client import FirestoreManager
from src.config import REPORTS_DIR, DATA_DIR

# Streamlit Page Config
st.set_page_config(
    page_title="CRESCA AI // Autonomous Sentinel",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern dark-glass UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f9d58;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #80868b;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #1e1e24;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #333;
    }
    .status-badge {
        background-color: #0f9d58;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_orchestrator():
    return CrescaAgentOrchestrator()

@st.cache_resource
def get_firestore():
    return FirestoreManager()


orchestrator = get_orchestrator()
firestore_mgr = get_firestore()

# Header
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown('<div class="main-title">🌱 CRESCA AI // AUTONOMOUS SENTINEL</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Autonomous Demographic Risk & Spatiotemporal Nutrition Logistics Protocol</div>', unsafe_allow_html=True)
with col_status:
    st.markdown('<div style="text-align: right; margin-top: 15px;"><span class="status-badge">TASKMASTER 24/7 ACTIVE</span></div>', unsafe_allow_html=True)

st.divider()

# Sidebar: Controls & Audit
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/sprout.png", width=64)
    st.subheader("Autonomous Ops Control")
    st.info("System operates in 24/7 background mode via Google Cloud Scheduler triggers.")

    if st.button("⚡ Trigger Autonomous Run Now", type="primary", use_container_width=True):
        with st.spinner("Executing autonomous agent loop..."):
            result = orchestrator.execute_autonomous_run(trigger_source="STREAMLIT_MANUAL_TRIGGER")
            st.session_state["latest_result"] = result
            st.success(f"Run {result['run_id']} completed in {result['execution_duration_sec']}s!")

    st.divider()
    st.subheader("Audit Ledger History")
    recent_runs = firestore_mgr.get_latest_runs(limit=5)
    for r in recent_runs:
        st.caption(f"**{r['run_id']}**  \n🕒 {r.get('timestamp', '')[:19]}  \n🎯 Proj. Stunting: `{r.get('total_projected_stunting_cases_90d', 0):,}`")

# Fetch current dataset
districts_csv = DATA_DIR / "synthetic_district_indicators.csv"
if districts_csv.exists():
    df_districts = pd.read_csv(districts_csv)
else:
    df_districts = pd.DataFrame()

# Tab Navigation
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Geospatial Risk Map", "📊 Statistical Analytics", "📦 Logistics PO Dispatch", "📑 Audit & PDF Action Plan"])

# TAB 1: Geospatial Risk Map
with tab1:
    st.subheader("Regional Vulnerability & Stunting Risk Heatmap")
    
    # Process through statistical engine for live map rendering
    df_analyzed, stat_summary = orchestrator.stat_engine.run_full_pipeline(df_districts)
    
    # Summary Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Monitored Districts", len(df_analyzed))
    m2.metric("Total Toddlers", f"{df_analyzed['total_toddlers'].sum():,}")
    m3.metric("Projected 90-Day Stunting", f"{df_analyzed['projected_stunting_90d'].sum():,}")
    m4.metric("Critical Hotspots", len(df_analyzed[df_analyzed["risk_tier"] == "CRITICAL"]))

    # Folium Interactive Map
    medan_center = [3.5952, 98.6722]
    m = folium.Map(location=medan_center, zoom_start=11, tiles="CartoDB positron")

    tier_colors = {
        "CRITICAL": "#ea4335",
        "HIGH": "#fbbc04",
        "MODERATE": "#4285f4",
        "LOW": "#34a853",
    }

    for _, row in df_analyzed.iterrows():
        tier = row["risk_tier"]
        color = tier_colors.get(tier, "#34a853")
        radius = 8 + (float(row["cdvi_score"]) * 12)

        popup_html = f"""
        <b>{row['district_name']}</b><br/>
        Risk Tier: <font color="{color}"><b>{tier}</b></font><br/>
        CDVI Score: <b>{row['cdvi_score']}</b><br/>
        90-Day Stunting Proj.: <b>{row['projected_stunting_90d']} cases</b><br/>
        Poor Sanitation: {row['poor_sanitation_pct']}%<br/>
        Extreme Poverty: {row['extreme_poverty_pct']}%
        """

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=250),
        ).add_to(m)

    st_folium(m, width=1100, height=500)

# TAB 2: Statistical Analytics
with tab2:
    st.subheader("Multivariate Decomposition & Epidemiological Projections")
    col_pca, col_rank = st.columns([1, 1])

    with col_pca:
        st.markdown("#### Principal Component Analysis (CDVI Weights)")
        weights = stat_summary["pca_analysis"]["feature_weights"]
        df_weights = pd.DataFrame(list(weights.items()), columns=["Indicator", "Loading Weight"]).sort_values("Loading Weight", ascending=True)
        st.bar_chart(data=df_weights.set_index("Indicator"), color="#0f9d58")
        st.info(f"💡 **First Principal Component (PC1)** explains **{stat_summary['pca_analysis']['pc1_explained_variance_pct']}%** of total demographic variance.")

    with col_rank:
        st.markdown("#### 90-Day Poisson GLM Projections by Urgency")
        df_top_urgent = df_analyzed[["urgency_rank", "district_name", "risk_tier", "cdvi_score", "projected_stunting_90d", "proj_ci_lower_95", "proj_ci_upper_95"]].head(8)
        st.dataframe(df_top_urgent, use_container_width=True)

# TAB 3: Logistics PO Dispatch
with tab3:
    st.subheader("Autonomous Purchase Order & Supplement Allocation")
    logistics = orchestrator.optimizer.optimize_allocation(df_analyzed)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget Cap", f"IDR {logistics['total_budget_cap_idr']:,}")
    c2.metric("Budget Utilized", f"IDR {logistics['total_budget_utilized_idr']:,}", f"{logistics['budget_utilization_pct']}%")
    c3.metric("Formula F-75 Tins", f"{logistics['total_f75_units']:,}")
    c4.metric("PMT Biscuit Boxes", f"{logistics['total_pmt_boxes']:,}")

    df_alloc = pd.DataFrame(logistics["district_allocations"])
    st.dataframe(
        df_alloc[["urgency_rank", "district_name", "risk_tier", "allocated_f75_tins", "allocated_pmt_boxes", "allocated_iron_packs", "district_cost_idr", "allocation_status"]],
        use_container_width=True
    )

# TAB 4: Audit & PDF Action Plan
with tab4:
    st.subheader("Audit-Ready PDF Action Plan & Cryptographic Ledger")
    
    # Check latest generated PDF
    pdf_files = sorted(REPORTS_DIR.glob("CRESCA-RUN-*.pdf"), reverse=True)
    if pdf_files:
        latest_pdf = pdf_files[0]
        st.success(f"Latest Compiled Action Plan: **{latest_pdf.name}**")
        with open(latest_pdf, "rb") as pdf_data:
            st.download_button(
                label="📥 Download Official Action Plan PDF",
                data=pdf_data,
                file_name=latest_pdf.name,
                mime="application/pdf",
                type="primary",
            )
    else:
        st.warning("No PDF report generated yet. Click 'Trigger Autonomous Run Now' in the sidebar.")

    st.markdown("---")
    st.subheader("Gemma 2 Privacy Guardrail Compliance")
    st.markdown("""
    - **Zero-Shot Entity Redaction:** Patient NIK, Child Full Names, and Guardian Identifiers are scrubbed into irreversible hashes before cloud transmission.
    - **Regulatory Adherence:** 100% compliant with healthcare data privacy regulations & Google Cloud AI ethics standards.
    """)
