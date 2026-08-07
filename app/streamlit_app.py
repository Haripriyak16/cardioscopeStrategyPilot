"""
streamlit_app.py
Main App Router for CardioScope AI Strategy Copilot
"""
import streamlit as st
st.set_page_config(page_title="CardioScope Strategy Copilot", layout="wide", initial_sidebar_state="collapsed")
import os
import sys

# Ensure src modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set default Plotly theme for uniformity
import plotly.io as pio
pio.templates.default = "plotly_white"
# Update plotly default font
pio.templates["plotly_white"].layout.font.family = "'Poppins', sans-serif"
pio.templates["plotly_white"].layout.colorway = ["#0056A3", "#66AEDC", "#003366", "#99CCE8", "#3384C4", "#004482"]

# Inject Custom CSS for Premium Look and Fonts
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    /* Apply font globally */
    html, body, [class*="st-"], .stMarkdown, .stText, h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Base app background - Cipla white/light blue */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Headers - Cipla Blue */
    h1, h2, h3 {
        color: #0056A3 !important;
        font-weight: 700 !important;
    }
    
    /* Improve metric cards spacing and look */
    [data-testid="stMetric"], div.css-1r6slb0, div.st-emotion-cache-1r6slb0 {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 86, 163, 0.08); /* Subtle Cipla blue shadow */
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #E5E7EB;
    }
    
    /* Clean up dividers */
    hr {
        border-color: rgba(0, 86, 163, 0.15) !important;
        margin: 2em 0 !important;
    }
    
    /* Remove default padding to make everything full length fit */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 96% !important;
    }
    
    /* Button styling to match Cipla blue theme */
    button[kind="primary"] {
        background-color: #0056A3 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important; /* Rounded like the website */
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
    }
    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #0056A3 !important;
        border: 1px solid #0056A3 !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
    }
    button[kind="primary"]:hover {
        background-color: #004482 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #F0F7FF !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        border-right: 1px solid #E5E7EB !important;
        background-color: #F8F9FA !important;
    }

    /* Cipla brand header */
    .cipla-header {
        display: flex;
        align-items: baseline;
        gap: 16px;
        margin-bottom: 6px;
    }
    .cipla-wordmark {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 1.6rem;
        color: #0056A3;
        letter-spacing: -0.5px;
    }
    .cipla-subtitle {
        font-size: 0.85rem;
        color: #6B7280;
        font-weight: 500;
        border-left: 2px solid #D9E4F1;
        padding-left: 16px;
    }

    /* Embossed tile look for all buttons */
    .stButton > button, .stDownloadButton > button {
        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 0.82rem !important;
        padding: 0.55rem 0.9rem !important;
        transition: all 0.15s ease;
    }
    button[kind="primary"] {
        background: linear-gradient(180deg, #1568B8 0%, #0056A3 100%) !important;
        box-shadow: 0 3px 10px rgba(0, 51, 102, 0.30), inset 0 1px 0 rgba(255,255,255,0.25) !important;
    }
    button[kind="secondary"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F3F8FC 100%) !important;
        box-shadow: 0 2px 6px rgba(0, 86, 163, 0.12), inset 0 1px 0 rgba(255,255,255,0.7) !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 5px 12px rgba(0, 86, 163, 0.25) !important;
    }

    /* Embossed tile look for metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(160deg, #FFFFFF 0%, #EEF5FC 100%) !important;
        box-shadow: 0 4px 14px rgba(0, 86, 163, 0.10), inset 0 1px 0 rgba(255,255,255,0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

from app.views import home, market, competition, external, copilot, explorer, simulator, report, comparison, knowledge_graph, executive_hub

PAGES = {
    "Home": home,
    "Executive Intelligence Hub": executive_hub,
    "AI Strategy Copilot": copilot,
    "Market Intelligence": market,
    "Competition Intelligence": competition,
    "External Intelligence": external,
    "Opportunity Explorer": explorer,
    "Scenario Simulator": simulator,
    "Human vs AI": comparison,
    "Knowledge Graph": knowledge_graph,
    "Executive Report": report
}

# (full page name, short nav label)
NAV_ITEMS = [
    ("Home", "Home"),
    ("Executive Intelligence Hub", "Exec Hub"),
    ("AI Strategy Copilot", "Copilot"),
    ("Market Intelligence", "Market"),
    ("Competition Intelligence", "Competition"),
    ("External Intelligence", "External"),
    ("Opportunity Explorer", "Explorer"),
    ("Scenario Simulator", "Simulator"),
    ("Human vs AI", "Human vs AI"),
    ("Knowledge Graph", "Knowledge"),
    ("Executive Report", "Report"),
]

def main():
    st.markdown("""
    <div class="cipla-header">
        <span class="cipla-wordmark">Cipla</span>
        <span class="cipla-subtitle">CardioScope AI &middot; Executive Strategy Copilot</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if 'nav_selection' not in st.session_state:
        st.session_state.nav_selection = "Home"

    # Top Navigation Bar using columns
    cols = st.columns(len(NAV_ITEMS))
    for idx, (page_name, short_label) in enumerate(NAV_ITEMS):
        is_active = (st.session_state.nav_selection == page_name)
        button_type = "primary" if is_active else "secondary"
        if cols[idx].button(short_label, use_container_width=True, type=button_type):
            st.session_state.nav_selection = page_name
            st.rerun()

    st.markdown("---")
    
    page = PAGES[st.session_state.nav_selection]
    
    # Load data once and pass to pages via session state or just function calls
    import pandas as pd
    @st.cache_data
    def load_data():
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        opp_path = f"{base_dir}/outputs/tables/final_recommendations.csv" # Fixed path
        raw_path = f"{base_dir}/data/processed/cardiac_clean.csv"
        
        if os.path.exists(opp_path) and os.path.exists(raw_path):
            opp_df = pd.read_csv(opp_path)
            raw_df = pd.read_csv(raw_path)
            # Parse json in Explanation column
            import json
            def safe_parse(x):
                try: return json.loads(x)
                except: return {}
            if 'Explanation' in opp_df.columns:
                opp_df['Explanation_Dict'] = opp_df['Explanation'].apply(safe_parse)
            
            # V2 Strategy Copilot Metrics Injection
            import numpy as np
            # Simulate HHI (Herfindahl-Hirschman Index) based on competitor counts. 10000 = monopoly.
            opp_df['HHI'] = 10000 / (opp_df['Num Competitors'] + 1).clip(upper=20)
            opp_df['Entry Barrier Score'] = (opp_df['Patent Score'] + (10 - opp_df['Competition Score'])) / 2
            opp_df['Future Opportunity Score'] = (opp_df['Opportunity Score'] + opp_df['Growth Score']*10) / 2
            
            # Investment Matrix Mapping
            def map_investment(strat):
                if strat == 'Double Down': return 'Double Down'
                elif strat == 'Build': return 'Build Capability'
                elif strat == 'Partner / Selective Approach': return 'Partner'
                elif strat == 'Explore/Monitor': return 'Monitor'
                elif strat == 'Divest': return 'Avoid'
                else: return 'Expand'
            opp_df['Investment Matrix'] = opp_df['Strategy'].apply(map_investment)
            
            return opp_df, raw_df
        return None, None
        
    opp_df, raw_df = load_data()
    
    if opp_df is None:
        st.error("Data not found. Please run `python main.py` to generate the outputs first.")
        return
        
    # Render the selected page
    page.render(opp_df, raw_df)

if __name__ == "__main__":
    main()
