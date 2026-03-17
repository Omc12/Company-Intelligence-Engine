import streamlit as st
import json
import requests
from core.engine import analyze_company

# Page config
st.set_page_config(
    page_title="Company Intelligence Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI styling
st.markdown("""
<style>
    /* Typography and Base Setting */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1F2937;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header styling */
    .main-header {
        font-size: 2.25rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0.25rem;
        letter-spacing: -0.025em;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0F172A;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E2E8F0;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Cards and Containers */
    .metric-container {
        border-label: 1px solid #E2E8F0;
        background-color: #FFFFFF;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        padding: 1.25rem;
    }
    
    .summary-box {
        background-color: #F8FAFC;
        border-left: 4px solid #0EA5E9;
        padding: 1.5rem;
        border-radius: 6px;
        margin-bottom: 2rem;
        color: #334155;
        line-height: 1.6;
        font-size: 1.05rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    
    hr {
        margin: 2em 0;
        border-color: #E2E8F0;
    }

    /* List styling for capabilities */
    .feature-list {
        list-style-type: none;
        padding-left: 0;
        margin-bottom: 1rem;
    }
    .feature-list li {
        margin-bottom: 0.5rem;
        display: flex;
        align-items: flex-start;
        font-size: 0.9rem;
        color: #475569;
    }
    .feature-list.positive li::before {
        content: "✓";
        color: #10B981;
        margin-right: 0.5rem;
        font-weight: bold;
    }
    .feature-list.negative li::before {
        content: "✕";
        color: #EF4444;
        margin-right: 0.5rem;
        font-weight: bold;
    }

    /* List styling for results */
    .bullet-list {
        list-style-type: none;
        padding-left: 0;
    }
    .bullet-list li {
        margin-bottom: 0.75rem;
        position: relative;
        padding-left: 1.25rem;
        line-height: 1.5;
        color: #334155;
    }
    .bullet-list.neutral li::before {
        content: "•";
        color: #94A3B8;
        position: absolute;
        left: 0;
        font-weight: bold;
        font-size: 1.2em;
    }
    .bullet-list.alert li::before {
        content: "!";
        color: #EF4444;
        position: absolute;
        left: 0;
        font-weight: bold;
    }

    /* Logo/Brand placeholder */
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 2rem;
    }
    .brand-icon {
        width: 32px;
        height: 32px;
        background-color: #0F172A;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .brand-text {
        font-weight: 700;
        font-size: 1.25rem;
        color: #0F172A;
        letter-spacing: -0.025em;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=86400) # Cache for 24 hours
def get_sec_companies():
    """Fetch company tickers and CIKs from SEC website."""
    try:
        headers = {"User-Agent": "CompanyIntelligence/1.0 (contact@example.com)"}
        res = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        # Build mapping dictionary: "Title (Ticker)" -> CIK string
        mapping = {}
        for item in data.values():
            title = item['title'].title()
            ticker = item['ticker']
            cik = str(item['cik_str']).zfill(10) # SEC requires 10 digit pad sometimes, but engine might expect int-like. We'll zero pad for safety
            display_name = f"{title} ({ticker})"
            mapping[display_name] = {"cik": cik, "name": item['title']}
            
        return mapping
    except Exception as e:
        st.sidebar.error(f"Failed to load SEC Companies data. {e}")
        return {"Microsoft Corp (MSFT)": {"cik": "0000789019", "name": "MICROSOFT CORP"}}

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="brand-logo">
            <div class="brand-icon">CI</div>
            <div class="brand-text">Intelligence Engine</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-title' style='margin-top:0;'>Analysis Configuration</div>", unsafe_allow_html=True)
        
        # Manual Config
        target_name = st.text_input("Target Company", value="Microsoft Corp", help="Name of the company to analyze.")
        target_cik = st.text_input("SEC CIK Number", value="0000789019", help="Central Index Key for SEC filings.")
        
        query = st.text_area(
            "Intelligence Directive", 
            value="What competitive risks affect the AI business?", 
            height=120, 
            help="Provide a specific directive or question for the extraction engine."
        )
        
        st.write("") # Spacing
        submit_btn = st.button("Generate Intelligence Report", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        # Capabilities Expander - Clean design
        with st.expander("System Capabilities", expanded=False):
            st.markdown("""
            <div style="font-weight: 600; font-size: 0.9rem; color: #0F172A; margin-bottom: 0.5rem;">Supported Operations</div>
            <ul class="feature-list positive">
                <li>Deep document retrieval (10-K, 10-Q)</li>
                <li>Qualitative risk extraction & summarization</li>
                <li>Strategy and competitive advantage synthesis</li>
                <li>Section-specific context routing</li>
            </ul>
            
            <div style="font-weight: 600; font-size: 0.9rem; color: #0F172A; margin-top: 1rem; margin-bottom: 0.5rem;">Unsupported Operations</div>
            <ul class="feature-list negative">
                <li>Real-time financial metrics or stock pricing</li>
                <li>External news sentiment analysis</li>
                <li>Definite quantitative forecasting</li>
            </ul>
            """, unsafe_allow_html=True)
            
        return target_name, target_cik, query, submit_btn

def render_hero():
    st.markdown('<div class="main-header">Company Intelligence Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered deep analysis of SEC filings and corporate disclosures.</div>', unsafe_allow_html=True)
    
    # 3-column feature display instead of colorful boxes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 1rem; border-left: 3px solid #64748B; background: #F8FAFC;">
            <div style="font-weight: 600; color: #0F172A; margin-bottom: 0.25rem;">Information Retrieval</div>
            <div style="font-size: 0.9rem; color: #475569;">Extracts sections directly from primary regulatory filings.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="padding: 1rem; border-left: 3px solid #64748B; background: #F8FAFC;">
            <div style="font-weight: 600; color: #0F172A; margin-bottom: 0.25rem;">Contextual Inference</div>
            <div style="font-size: 0.9rem; color: #475569;">Synthesizes answers based strictly on retrieved documents.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="padding: 1rem; border-left: 3px solid #64748B; background: #F8FAFC;">
            <div style="font-weight: 600; color: #0F172A; margin-bottom: 0.25rem;">Structured Data</div>
            <div style="font-size: 0.9rem; color: #475569;">Normalizes outputs into standard schemas for downstream integration.</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 1.05rem; color: #334155; max-width: 800px; line-height: 1.6;">
        <b>System Readiness:</b> The environment is initialized. Use the configuration panel to select a target entity and define your intelligence directive. The engine will retrieve relevant documentation and compile a structured assessment.
    </div>
    """, unsafe_allow_html=True)

def render_results(company, query, intel, features):
    st.markdown('<div class="main-header">Intelligence Assessment</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Subject: <b>{company}</b></div>', unsafe_allow_html=True)
    
    # Top Metrics - Streamlit native metrics look professional enough, but we control the layout
    col1, col2 = st.columns(2)
    
    with col1:
        conf_color = "normal"
        if intel.confidence > 0.8:
            conf_color = "inverse"
        elif intel.confidence < 0.5:
            conf_color = "off"
            
        st.metric(label="System Confidence Level", value=f"{intel.confidence:.2%}", 
                 delta="High Reliability" if intel.confidence > 0.7 else "Low Reliability", delta_color=conf_color)
                 
    with col2:
        outlook_val = intel.outlook.value.upper()
        
        st.metric(label="Synthesized Outlook", value=outlook_val, delta="Engine Output", delta_color="off")

    st.write("") # Spacing
    
    # Executive Summary
    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-box">{intel.summary}</div>', unsafe_allow_html=True)
    
    # Detailed Tabs
    tab1, tab2, tab3 = st.tabs(["Strengths & Advantages", "Risks & Weaknesses", "Engineered Features"])
    
    with tab1:
        col_s, col_ca = st.columns(2)
        with col_s:
            st.markdown('<div class="section-title" style="margin-top:0.5rem; border:none; padding:0;">Corporate Strengths</div>', unsafe_allow_html=True)
            if intel.strengths:
                st.markdown('<ul class="bullet-list neutral">', unsafe_allow_html=True)
                for s in intel.strengths:
                    st.markdown(f"<li>{s}</li>", unsafe_allow_html=True)
                st.markdown('</ul>', unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#64748B; font-style:italic;'>No explicit strengths extracted for this directive.</p>", unsafe_allow_html=True)
                
        with col_ca:
            st.markdown('<div class="section-title" style="margin-top:0.5rem; border:none; padding:0;">Competitive Moat</div>', unsafe_allow_html=True)
            if intel.competitive_advantage:
                st.markdown('<ul class="bullet-list neutral">', unsafe_allow_html=True)
                for ca in intel.competitive_advantage:
                    st.markdown(f"<li><strong>{ca}</strong></li>", unsafe_allow_html=True)
                st.markdown('</ul>', unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#64748B; font-style:italic;'>No specific competitive advantages identified.</p>", unsafe_allow_html=True)
                
    with tab2:
        col_r, col_w = st.columns(2)
        with col_r:
            st.markdown('<div class="section-title" style="margin-top:0.5rem; border:none; padding:0;">Identified Risk Factors</div>', unsafe_allow_html=True)
            if intel.risk_factors:
                st.markdown('<ul class="bullet-list alert">', unsafe_allow_html=True)
                for r in intel.risk_factors:
                    st.markdown(f"<li>{r}</li>", unsafe_allow_html=True)
                st.markdown('</ul>', unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#64748B; font-style:italic;'>No significant risk factors identified.</p>", unsafe_allow_html=True)
                
        with col_w:
            st.markdown('<div class="section-title" style="margin-top:0.5rem; border:none; padding:0;">Extracted Weaknesses</div>', unsafe_allow_html=True)
            if intel.weaknesses:
                st.markdown('<ul class="bullet-list alert">', unsafe_allow_html=True)
                for w in intel.weaknesses:
                    st.markdown(f"<li>{w}</li>", unsafe_allow_html=True)
                st.markdown('</ul>', unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#64748B; font-style:italic;'>No structural weaknesses retrieved.</p>", unsafe_allow_html=True)
                
    with tab3:
        st.markdown('<div class="section-title" style="margin-top:0.5rem; border:none; padding:0;">Raw Feature Extraction Layer</div>', unsafe_allow_html=True)
        st.markdown("<p style='color:#475569; font-size:0.95rem;'>Representation of the normalized JSON output used by downstream models.</p>", unsafe_allow_html=True)
        try:
            st.json(features)
        except Exception:
            st.write(features)

def main():
    company, cik, query, submit_btn = render_sidebar()
    
    if not submit_btn:
        render_hero()
    else:
        with st.status("Initializing Intelligence Pipeline...", expanded=True) as status_container:
            try:
                def update_status(msg):
                    status_container.update(label=msg)
                    st.write(f"✓ {msg}")
                    
                # Call the core engine method
                intel, features = analyze_company(company, cik, query, status_callback=update_status)
                
                status_container.update(label="Intelligence Assessment Complete", state="complete", expanded=False)
                
                # Render results outside or inside, usually fine inside, but better to keep results visible 
            except Exception as e:
                status_container.update(label="Analysis Pipeline Failed", state="error", expanded=True)
                st.error(f"Analysis Generation Failed: {str(e)}")
                st.info("The language model might have encountered an unexpected format or token limit. Please try restarting the query, or verify the inputs.")
                return # Stop execution if failed
                
        # Render the UI after the status block closes so it takes up the full width beautifully
        render_results(company, query, intel, features)

if __name__ == "__main__":
    main()
