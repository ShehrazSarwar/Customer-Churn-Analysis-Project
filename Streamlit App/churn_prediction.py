import streamlit as st
import pandas as pd
import joblib
import io

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnRadar · ML Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Background */
.stApp {
    background: #0b0f1a;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Header strip */
.radar-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid #312e81;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.radar-header::before {
    content: "📡";
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 4rem;
    opacity: 0.15;
}
.radar-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #a5b4fc;
    margin: 0;
    letter-spacing: -0.5px;
}
.radar-header p {
    color: #94a3b8;
    margin: 0.3rem 0 0;
    font-size: 0.95rem;
}

/* KPI cards */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.kpi-card.red::after   { background: linear-gradient(90deg,#ef4444,#f97316); }
.kpi-card.amber::after { background: linear-gradient(90deg,#f59e0b,#fbbf24); }
.kpi-card.green::after { background: linear-gradient(90deg,#10b981,#34d399); }
.kpi-card.blue::after  { background: linear-gradient(90deg,#6366f1,#a5b4fc); }
.kpi-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color:#64748b; margin-bottom:0.3rem; }
.kpi-value { font-size: 2rem; font-weight: 700; color:#e2e8f0; font-family:'JetBrains Mono',monospace; }
.kpi-sub   { font-size: 0.78rem; color:#94a3b8; margin-top:0.2rem; }

/* Section headers */
.section-title {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #6366f1;
    font-weight: 600;
    margin: 1.5rem 0 0.75rem;
    border-left: 3px solid #6366f1;
    padding-left: 0.75rem;
}

/* Risk badge */
.badge-critical { background:#450a0a; color:#fca5a5; border:1px solid #7f1d1d; padding:2px 10px; border-radius:99px; font-size:0.7rem; font-weight:600; }
.badge-high     { background:#431407; color:#fed7aa; border:1px solid #7c2d12; padding:2px 10px; border-radius:99px; font-size:0.7rem; font-weight:600; }
.badge-medium   { background:#422006; color:#fde68a; border:1px solid #78350f; padding:2px 10px; border-radius:99px; font-size:0.7rem; font-weight:600; }

/* Probability bar */
.prob-bar-bg { background:#1e293b; border-radius:99px; height:8px; width:100%; }
.prob-bar-fill { height:8px; border-radius:99px; }

/* Dataframe tweaks */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Upload zone */
.uploadedFile { border-radius:10px !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
}

/* Selectbox / inputs */
[data-baseweb="select"] > div {
    background: #1e293b !important;
    border-color: #334155 !important;
    color: #e2e8f0 !important;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #1e293b !important;
    border-color: #334155 !important;
    color: #e2e8f0 !important;
}

/* Expander */
details summary {
    color: #94a3b8 !important;
}

/* Metric */
[data-testid="stMetric"] label { color: #64748b !important; font-size:0.8rem !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-family:'JetBrains Mono',monospace !important; }

/* Tab */
button[data-baseweb="tab"] {
    color: #64748b !important;
    font-family: 'Space Grotesk',sans-serif !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #a5b4fc !important;
    border-bottom-color: #6366f1 !important;
}

/* Info/warn/success boxes */
.stAlert { border-radius:10px !important; }

.footer-note {
    text-align:center;
    color:#334155;
    font-size:0.72rem;
    margin-top:3rem;
    padding-top:1rem;
    border-top:1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def risk_label(p):
    if p >= 0.90: return "Critical", "badge-critical"
    if p >= 0.75: return "High",     "badge-high"
    return "Medium", "badge-medium"

def prob_bar_html(prob, color="#ef4444"):
    pct = int(prob * 100)
    return (
        f'<div class="prob-bar-bg">'
        f'<div class="prob-bar-fill" style="width:{pct}%;background:{color};"></div>'
        f'</div><span style="font-size:0.75rem;color:#94a3b8;font-family:JetBrains Mono,monospace">{pct}%</span>'
    )

def color_for_prob(p):
    if p >= 0.90: return "#ef4444"
    if p >= 0.75: return "#f97316"
    return "#f59e0b"

COLUMNS_TO_DROP = [
    "Customer_ID", "Churn_Category", "Churn_Reason", "Customer_Status",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ ChurnRadar")
    st.markdown("<hr style='border-color:#1e293b;margin:0.5rem 0 1rem'>", unsafe_allow_html=True)

    st.markdown("**Model files**")
    preprocessor_file = st.file_uploader("Preprocessor (.joblib)", type=["joblib"], key="prep")
    model_file        = st.file_uploader("XGBoost model (.joblib)", type=["joblib"], key="mdl")

    st.markdown("<hr style='border-color:#1e293b;margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown("**Data**")
    data_file = st.file_uploader("Customer CSV", type=["csv"], key="data")

    st.markdown("<hr style='border-color:#1e293b;margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown("**Risk threshold**")
    threshold = st.slider("Min churn probability", 0.0, 1.0, 0.50, 0.05,
                          help="Only show customers with churn probability above this value")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="radar-header">
  <h1>ChurnRadar</h1>
  <p>XGBoost-powered customer churn prediction &amp; risk intelligence</p>
</div>
""", unsafe_allow_html=True)

# ── Load / predict pipeline ───────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model(prep_bytes, mdl_bytes):
    preprocessor = joblib.load(io.BytesIO(prep_bytes))
    model        = joblib.load(io.BytesIO(mdl_bytes))
    return preprocessor, model

def run_prediction(df_raw, preprocessor, model):
    df = df_raw.copy()
    X  = df.drop(columns=COLUMNS_TO_DROP, errors="ignore")
    X_proc = preprocessor.transform(X)
    df["Churn_Prediction"]  = model.predict(X_proc)
    df["Churn_Probability"] = model.predict_proba(X_proc)[:, 1]
    return df

# ── Run predictions when all three files are uploaded ────────────────────────
results_df = None

if preprocessor_file and model_file and data_file:
    with st.spinner("Running predictions…"):
        try:
            preprocessor, model = load_model(preprocessor_file.read(), model_file.read())
            raw_df     = pd.read_csv(data_file)
            full_df    = run_prediction(raw_df, preprocessor, model)
            results_df = full_df[full_df["Churn_Prediction"] == 1].sort_values(
                "Churn_Probability", ascending=False
            )
            st.success(f"✅ Predictions complete — {len(results_df):,} at-risk customers found.")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
else:
    st.markdown("""
<div style="background:#111827;border:1px solid #1e293b;border-radius:14px;padding:2rem 2.5rem;margin-top:1rem;">
  <div style="font-size:2rem;margin-bottom:0.75rem;">📂</div>
  <div style="color:#a5b4fc;font-size:1.05rem;font-weight:600;margin-bottom:0.5rem;">Upload your files to get started</div>
  <div style="color:#64748b;font-size:0.88rem;line-height:1.8;">
    <b style="color:#94a3b8;">1.</b> Upload <code>churn_preprocessor.joblib</code> in the sidebar<br>
    <b style="color:#94a3b8;">2.</b> Upload <code>baseline_xgb_model.joblib</code> in the sidebar<br>
    <b style="color:#94a3b8;">3.</b> Upload your joined customer <code>.csv</code> file<br>
    <b style="color:#94a3b8;">4.</b> The dashboard will populate automatically
  </div>
</div>
""", unsafe_allow_html=True)

# ── Dashboard (only when data is available) ───────────────────────────────────
if results_df is not None and len(results_df) > 0:

    # Apply threshold filter
    view_df = results_df[results_df["Churn_Probability"] >= threshold].copy()
    view_df = view_df.sort_values("Churn_Probability", ascending=False).reset_index(drop=True)

    total_at_risk   = len(view_df)
    critical_count  = (view_df["Churn_Probability"] >= 0.90).sum()
    high_count      = ((view_df["Churn_Probability"] >= 0.75) & (view_df["Churn_Probability"] < 0.90)).sum()
    avg_prob        = view_df["Churn_Probability"].mean()
    avg_revenue     = view_df["Total_Revenue"].mean() if "Total_Revenue" in view_df else 0
    revenue_at_risk = view_df["Total_Revenue"].sum()   if "Total_Revenue" in view_df else 0

    # KPI row
    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card red">
        <div class="kpi-label">At-Risk Customers</div>
        <div class="kpi-value">{total_at_risk:,}</div>
        <div class="kpi-sub">above {int(threshold*100)}% threshold</div>
      </div>
      <div class="kpi-card amber">
        <div class="kpi-label">Critical Risk (≥90%)</div>
        <div class="kpi-value">{critical_count:,}</div>
        <div class="kpi-sub">{critical_count/max(total_at_risk,1)*100:.1f}% of flagged</div>
      </div>
      <div class="kpi-card blue">
        <div class="kpi-label">Avg Churn Probability</div>
        <div class="kpi-value">{avg_prob:.1%}</div>
        <div class="kpi-sub">across flagged customers</div>
      </div>
      <div class="kpi-card green">
        <div class="kpi-label">Revenue at Risk</div>
        <div class="kpi-value">₹{revenue_at_risk:,.0f}</div>
        <div class="kpi-sub">avg ₹{avg_revenue:,.0f} / customer</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Risk List", "📊 Analytics", "🔍 Customer Detail", "📥 Export"])

    # ── TAB 1: Risk List ──────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-title">High-Risk Customers</div>', unsafe_allow_html=True)

        # Quick filters
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            risk_filter = st.selectbox("Risk level", ["All", "Critical (≥90%)", "High (75–90%)", "Medium (<75%)"])
        with col_f2:
            state_opts = ["All"] + sorted(view_df["State"].dropna().unique().tolist()) if "State" in view_df else ["All"]
            state_filter = st.selectbox("State", state_opts)
        with col_f3:
            contract_opts = ["All"] + sorted(view_df["Contract"].dropna().unique().tolist()) if "Contract" in view_df else ["All"]
            contract_filter = st.selectbox("Contract type", contract_opts)

        filtered = view_df.copy()
        if risk_filter == "Critical (≥90%)":
            filtered = filtered[filtered["Churn_Probability"] >= 0.90]
        elif risk_filter == "High (75–90%)":
            filtered = filtered[(filtered["Churn_Probability"] >= 0.75) & (filtered["Churn_Probability"] < 0.90)]
        elif risk_filter == "Medium (<75%)":
            filtered = filtered[filtered["Churn_Probability"] < 0.75]
        if state_filter != "All" and "State" in filtered:
            filtered = filtered[filtered["State"] == state_filter]
        if contract_filter != "All" and "Contract" in filtered:
            filtered = filtered[filtered["Contract"] == contract_filter]

        st.caption(f"Showing {len(filtered):,} customers")

        # Display columns
        display_cols = ["Customer_ID", "State", "Age", "Contract", "Internet_Type",
                        "Monthly_Charge", "Total_Revenue", "Churn_Probability"]
        display_cols = [c for c in display_cols if c in filtered.columns]

        show_df = filtered[display_cols].copy()
        show_df["Churn_Probability"] = show_df["Churn_Probability"].map(lambda x: f"{x:.1%}")

        st.dataframe(
            show_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Churn_Probability": st.column_config.ProgressColumn(
                    "Churn Probability",
                    format="%.0f%%",
                    min_value=0,
                    max_value=1,
                ) if False else st.column_config.TextColumn("Churn Probability"),
                "Monthly_Charge": st.column_config.NumberColumn("Monthly ₹", format="₹%.2f"),
                "Total_Revenue":  st.column_config.NumberColumn("Total Revenue ₹", format="₹%.2f"),
            }
        )

    # ── TAB 2: Analytics ──────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Distribution Analytics</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**Churn Probability Distribution**")
            if len(view_df) > 0:
                bins = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.01]
                labels = ["50–60%","60–70%","70–75%","75–80%","80–85%","85–90%","90–95%","95–100%"]
                view_df["_prob_bin"] = pd.cut(view_df["Churn_Probability"], bins=bins, labels=labels, right=False)
                prob_dist = view_df["_prob_bin"].value_counts().reindex(labels).fillna(0)
                st.bar_chart(prob_dist)

        with col_b:
            if "State" in view_df:
                st.markdown("**Top 10 States by At-Risk Count**")
                state_counts = view_df["State"].value_counts().head(10)
                st.bar_chart(state_counts)

        col_c, col_d = st.columns(2)
        with col_c:
            if "Contract" in view_df:
                st.markdown("**Contract Type Breakdown**")
                contract_counts = view_df["Contract"].value_counts()
                st.bar_chart(contract_counts)

        with col_d:
            if "Internet_Type" in view_df:
                st.markdown("**Internet Type Breakdown**")
                inet_counts = view_df["Internet_Type"].value_counts()
                st.bar_chart(inet_counts)

        # Revenue scatter
        if "Monthly_Charge" in view_df and "Churn_Probability" in view_df:
            st.markdown("**Monthly Charge vs Churn Probability**")
            scatter_df = view_df[["Monthly_Charge", "Churn_Probability", "Tenure_in_Months"]].dropna().rename(
                columns={"Monthly_Charge": "Monthly Charge", "Churn_Probability": "Churn Probability"}
            )
            st.scatter_chart(scatter_df, x="Monthly Charge", y="Churn Probability", size="Tenure_in_Months")

    # ── TAB 3: Customer Detail ────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">Individual Customer Lookup</div>', unsafe_allow_html=True)

        if "Customer_ID" in view_df.columns:
            selected_id = st.selectbox("Select Customer ID", view_df["Customer_ID"].tolist())
            cust = view_df[view_df["Customer_ID"] == selected_id].iloc[0]

            prob  = cust["Churn_Probability"]
            label, badge_class = risk_label(prob)

            # Header row
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Customer", cust["Customer_ID"])
            c2.metric("Churn Probability", f"{prob:.1%}")
            c3.metric("State", cust.get("State", "—"))
            c4.metric("Tenure", f"{cust.get('Tenure_in_Months', '—')} mo")

            st.markdown(f'<span class="{badge_class}">{label} Risk</span>', unsafe_allow_html=True)
            st.markdown(prob_bar_html(prob, color_for_prob(prob)), unsafe_allow_html=True)

            st.markdown("")

            # Two detail columns
            left, right = st.columns(2)
            with left:
                st.markdown("**Account Info**")
                for col in ["Age","Gender","Married","Contract","Payment_Method","Paperless_Billing","Value_Deal"]:
                    if col in cust:
                        st.markdown(f"- **{col.replace('_',' ')}**: {cust[col]}")
            with right:
                st.markdown("**Services**")
                for col in ["Phone_Service","Multiple_Lines","Internet_Service","Internet_Type",
                            "Online_Security","Online_Backup","Device_Protection_Plan","Premium_Support",
                            "Streaming_TV","Streaming_Movies","Streaming_Music","Unlimited_Data"]:
                    if col in cust:
                        val = cust[col]
                        icon = "✅" if val == "Yes" else ("❌" if val == "No" else "⬜")
                        st.markdown(f"- {icon} **{col.replace('_',' ')}**: {val}")

            st.markdown("**Financials**")
            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.metric("Monthly Charge", f"₹{cust.get('Monthly_Charge',0):,.2f}")
            fc2.metric("Total Charges",  f"₹{cust.get('Total_Charges',0):,.2f}")
            fc3.metric("Total Revenue",  f"₹{cust.get('Total_Revenue',0):,.2f}")
            fc4.metric("Referrals",      cust.get('Number_of_Referrals', '—'))

        else:
            st.info("Customer_ID column not found in data.")

    # ── TAB 4: Export ─────────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-title">Export Results</div>', unsafe_allow_html=True)

        export_cols = st.multiselect(
            "Columns to export",
            options=view_df.columns.tolist(),
            default=[c for c in ["Customer_ID","State","Age","Contract","Monthly_Charge",
                                  "Total_Revenue","Churn_Probability"] if c in view_df.columns]
        )

        if export_cols:
            export_df = view_df[export_cols].sort_values(
                "Churn_Probability", ascending=False
            ) if "Churn_Probability" in export_cols else view_df[export_cols]

            csv_bytes = export_df.to_csv(index=False).encode()
            st.download_button(
                label="⬇️  Download CSV",
                data=csv_bytes,
                file_name="churn_radar_export.csv",
                mime="text/csv",
            )

            st.caption(f"{len(export_df):,} rows · {len(export_cols)} columns")
            st.dataframe(export_df.head(20), use_container_width=True, hide_index=True)

elif results_df is not None and len(results_df) == 0:
    st.warning("No customers found above the selected probability threshold. Try lowering the threshold in the sidebar.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
  ChurnRadar · XGBoost Churn Prediction Dashboard · Built with Streamlit
</div>
""", unsafe_allow_html=True)