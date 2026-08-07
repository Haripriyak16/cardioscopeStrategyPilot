import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

def render(opp_df, raw_df):
    st.markdown("""
    <style>
    /* Glassmorphism premium card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 86, 163, 0.1);
        margin-bottom: 24px;
    }
    .kpi-title {
        font-size: 0.9rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 2.2rem;
        color: #0056A3;
        font-weight: 800;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 0.85rem;
        color: #10B981;
        font-weight: 500;
        margin-top: 4px;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #111827;
        margin-top: 32px;
        margin-bottom: 16px;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 8px;
    }
    .strat-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .tag-double-down { background: #DCFCE7; color: #166534; }
    .tag-build { background: #DBEAFE; color: #1E40AF; }
    .tag-partner { background: #FEF3C7; color: #92400E; }
    .tag-monitor { background: #F3F4F6; color: #374151; }
    .tag-avoid { background: #FEE2E2; color: #991B1B; }
    </style>
    """, unsafe_allow_html=True)

    st.title("Executive Intelligence Hub")
    st.markdown("A unified, premium executive dashboard synthesizing all AI strategy outputs.")

    # Sort opportunities
    top_opps = opp_df.sort_values(by='Opportunity Score', ascending=False)
    top_molecule = top_opps.iloc[0]

    # --- 1. Executive KPI Cards ---
    st.markdown('<div class="section-header">1. Executive Overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-title">Top Opportunity</div>
            <div class="kpi-value" style="font-size:1.4rem;">{top_molecule['MOLECULE_DESC'][:20]}</div>
            <div class="kpi-sub" style="color:#6B7280;">Highest priority</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-title">Opp Score</div>
            <div class="kpi-value">{top_molecule['Opportunity Score']:.1f}</div>
            <div class="kpi-sub">Out of 100</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        conf = top_molecule.get('Confidence Score', 85)
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-title">AI Confidence</div>
            <div class="kpi-value">{conf:.1f}%</div>
            <div class="kpi-sub">Data reliability</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-title">Right-to-Win</div>
            <div class="kpi-value">{top_molecule['Right to Win Score']:.1f}</div>
            <div class="kpi-sub">Out of 10</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        strat = top_molecule.get('Investment Matrix', top_molecule['Strategy'])
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-title">Strategy</div>
            <div class="kpi-value" style="font-size:1.2rem; margin-top:8px;">{strat}</div>
        </div>
        """, unsafe_allow_html=True)

    # --- 2. Top Opportunity Spaces ---
    st.markdown('<div class="section-header">2. Top Opportunity Spaces</div>', unsafe_allow_html=True)
    
    def get_tag_class(strategy):
        s = str(strategy).lower()
        if 'double' in s: return 'tag-double-down'
        if 'build' in s: return 'tag-build'
        if 'partner' in s: return 'tag-partner'
        if 'avoid' in s: return 'tag-avoid'
        return 'tag-monitor'

    table_html = """
    <table style="width:100%; text-align:left; border-collapse:collapse; background:white; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
        <tr style="background:#F3F4F6; color:#374151; font-weight:600; font-size:0.85rem; text-transform:uppercase;">
            <th style="padding:12px 16px;">Rank</th>
            <th style="padding:12px 16px;">Representative Molecule</th>
            <th style="padding:12px 16px;">Opportunity Score</th>
            <th style="padding:12px 16px;">Recommendation</th>
        </tr>
    """
    for idx, row in top_opps.head(5).iterrows():
        rank = idx + 1
        strat = row.get('Investment Matrix', row['Strategy'])
        tag = get_tag_class(strat)
        table_html += f"""
        <tr style="border-top:1px solid #E5E7EB;">
            <td style="padding:12px 16px; font-weight:600; color:#0056A3;">#{rank}</td>
            <td style="padding:12px 16px; font-weight:500;">{row['MOLECULE_DESC']}</td>
            <td style="padding:12px 16px;">{row['Opportunity Score']}</td>
            <td style="padding:12px 16px;"><span class="strat-tag {tag}">{strat}</span></td>
        </tr>
        """
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

    # --- 3. Priority Ranking & 4. Trade-off Resolution ---
    c_left, c_right = st.columns([1.5, 1])
    
    with c_left:
        st.markdown('<div class="section-header" style="margin-top:24px;">3. Priority Ranking & AI Reasoning</div>', unsafe_allow_html=True)
        for idx, row in top_opps.head(3).iterrows():
            reason = "High overall metrics."
            try:
                exp = json.loads(row.get('Explanation', '{}'))
                if 'Why' in exp and len(exp['Why']) > 0: reason = exp['Why'][0]
            except: pass
            
            st.markdown(f"""
            <div style="background:white; border:1px solid #E5E7EB; border-left:4px solid #0056A3; padding:16px; margin-bottom:12px; border-radius:4px;">
                <div style="font-weight:700; color:#111827; margin-bottom:4px;">{row['MOLECULE_DESC']}</div>
                <div style="font-size:0.9rem; color:#4B5563; margin-bottom:8px;"><b>Reason:</b> {reason}</div>
                <div style="font-size:0.85rem;"><b>Recommended Action:</b> <span style="color:#0056A3; font-weight:600;">{row.get('Investment Matrix', row['Strategy'])}</span></div>
            </div>
            """, unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="section-header" style="margin-top:24px;">4. AI Trade-off Analysis</div>', unsafe_allow_html=True)
        # Radar Chart for Top Molecule
        categories = ['Market Size', 'Growth', 'Right-to-Win', 'Competition', 'Future Potential']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[top_molecule['Market Score'], top_molecule['Growth Score'], top_molecule['Right to Win Score'], top_molecule['Competition Score'], top_molecule.get('Future Score', 5)],
            theta=categories,
            fill='toself',
            name=top_molecule['MOLECULE_DESC'],
            line_color='#0056A3',
            fillcolor='rgba(0, 86, 163, 0.2)'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- 5. Right-to-Win Analysis & 6. Competitor Intelligence ---
    st.markdown('<div class="section-header">5. Right-to-Win & 6. Competitor Intelligence</div>', unsafe_allow_html=True)
    c_rtw, c_comp = st.columns(2)
    
    with c_rtw:
        st.markdown("**Right-to-Win Breakdown**")
        for idx, row in top_opps.head(3).iterrows():
            st.markdown(f"""
            <div class="glass-card" style="padding:16px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#0056A3;">{row['MOLECULE_DESC']}</b>
                    <span style="background:#E0E7FF; color:#4338CA; padding:2px 8px; border-radius:12px; font-weight:bold; font-size:0.8rem;">Score: {row['Right to Win Score']}/10</span>
                </div>
                <div style="font-size:0.85rem; color:#4B5563; margin-top:8px;">Current Cipla Market Share indicates strategic fitness.</div>
            </div>
            """, unsafe_allow_html=True)
            
    with c_comp:
        st.markdown("**Competitive Landscape**")
        for idx, row in top_opps.head(3).iterrows():
            comp_score = row['Competition Score']
            st.markdown(f"""
            <div class="glass-card" style="padding:16px; margin-bottom:12px;">
                <b style="color:#0056A3;">{row['MOLECULE_DESC']}</b>
                <div style="font-size:0.85rem; margin-top:4px;">
                    <div><b>Competitor Intensity:</b> {row.get('Num Competitors', 'N/A')} active players</div>
                    <div><b>Market Defensibility (Score):</b> {comp_score:.1f}/10</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 7. Underpenetrated Opportunities ---
    st.markdown('<div class="section-header">7. Underpenetrated Opportunities (Blind Spots)</div>', unsafe_allow_html=True)
    # Filter: High Opp (>60), High Growth (>6), Low RTW (<4)
    under = opp_df[(opp_df['Opportunity Score'] > 60) & (opp_df['Growth Score'] > 6) & (opp_df['Right to Win Score'] < 4)]
    if not under.empty:
        for idx, row in under.head(2).iterrows():
            st.warning(f"**{row['MOLECULE_DESC']}**: High Growth ({row['Growth Score']:.1f}/10) but Low Cipla Presence ({row['Right to Win Score']:.1f}/10). Recommended Action: **Build Capability / M&A**.")
    else:
        st.info("No major underpenetrated blind spots detected based on current thresholds.")

    # --- 8. Strategic Actions ---
    st.markdown('<div class="section-header">8. Strategic Actions</div>', unsafe_allow_html=True)
    sa1, sa2, sa3 = st.columns(3)
    
    def get_first_strat(strat_type):
        df_strat = opp_df[opp_df['Strategy'].str.contains(strat_type, case=False, na=False)]
        if not df_strat.empty: return df_strat.iloc[0]['MOLECULE_DESC']
        return "None identified"

    with sa1:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid #166534;">
            <h4>🚀 Double Down</h4>
            <p style="font-size:0.9rem; color:#4B5563;">Prime target: <b>{get_first_strat('Double')}</b></p>
            <p style="font-size:0.8rem;">High market attractiveness and high Cipla Right-to-Win.</p>
        </div>
        """, unsafe_allow_html=True)
    with sa2:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid #1E40AF;">
            <h4>🏗️ Build Capability</h4>
            <p style="font-size:0.9rem; color:#4B5563;">Prime target: <b>{get_first_strat('Build')}</b></p>
            <p style="font-size:0.8rem;">High market attractiveness but requires new investments to win.</p>
        </div>
        """, unsafe_allow_html=True)
    with sa3:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid #991B1B;">
            <h4>🛑 Avoid / Divest</h4>
            <p style="font-size:0.9rem; color:#4B5563;">Prime target: <b>{get_first_strat('Avoid')}</b></p>
            <p style="font-size:0.8rem;">Low market attractiveness, high competition, low future potential.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- 9. Executive Summary ---
    st.markdown('<div class="section-header">9. Executive Summary Generation</div>', unsafe_allow_html=True)
    st.markdown("Download a compiled PDF or Text summary of all metrics for board presentations.")
    
    sum_text = f"""EXECUTIVE STRATEGY SUMMARY - CARDIOSCOPE AI

1. Highest Priority Opportunity: {top_molecule['MOLECULE_DESC']} (Score: {top_molecule['Opportunity Score']})
2. Highest Growth Opportunity: {opp_df.sort_values(by='Growth Score', ascending=False).iloc[0]['MOLECULE_DESC']}
3. Strongest Right-to-Win: {opp_df.sort_values(by='Right to Win Score', ascending=False).iloc[0]['MOLECULE_DESC']}
4. Overall AI Confidence: {top_molecule.get('Confidence Score', 85):.1f}%

STRATEGIC DIRECTIVE:
Aggressively pursue '{top_molecule.get('Investment Matrix', top_molecule['Strategy'])}' strategies in top-ranked markets while mitigating competitive risks.
"""
    st.download_button("📥 Download Executive Summary (TXT)", data=sum_text.encode('utf-8'), file_name="Executive_Summary.txt", mime="text/plain")

