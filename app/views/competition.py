import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

CIPLA_BLUES = ["#0056A3", "#003366", "#66AEDC", "#3384C4", "#99CCE8", "#004482", "#1A73B5", "#80BBE0", "#002347", "#4D97CB"]

def render(opp_df, raw_df):
    st.title("Competition Intelligence")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Market Leaders (Overall)")
        if "COMPANY" in raw_df.columns:
            comp_df = raw_df.groupby("COMPANY").agg({"MAT FEB'26": 'sum'}).reset_index()
            comp_df = comp_df.sort_values("MAT FEB'26", ascending=False).head(10)
            
            fig2 = px.pie(comp_df, names='COMPANY', values="MAT FEB'26", hole=0.4, title="Top 10 Companies Market Share",
                          color_discrete_sequence=CIPLA_BLUES)
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
            
    with col2:
        st.markdown("### Market Concentration (HHI)")
        df_local = opp_df.copy()
        fig = px.bar(df_local.head(10), x='MOLECULE_DESC', y='HHI',
                     color='HHI', title="HHI Score (10k = Monopoly, 0 = Red Ocean)",
                     color_continuous_scale='Blues')
        fig.add_hline(y=1500, line_dash="dash", line_color="#0056A3", annotation_text="Concentrated")
        fig.add_hline(y=2500, line_dash="dash", line_color="#003366", annotation_text="Highly Concentrated")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    c3, c4 = st.columns([1.5, 1])
    with c3:
        st.markdown("### Competitive Radar")
        top_mol = opp_df.iloc[0] if not opp_df.empty else None
        if top_mol is not None:
            categories = ['Competition Score', 'Patent Score', 'Right to Win Score', 'Entry Barrier Score', 'Innovation Score']
            
            fig_radar = go.Figure()
            # Top Molecule
            fig_radar.add_trace(go.Scatterpolar(
                r=[top_mol[c] for c in categories],
                theta=categories,
                fill='toself',
                name=top_mol['MOLECULE_DESC']
            ))
            # Average
            fig_radar.add_trace(go.Scatterpolar(
                r=[opp_df[c].mean() for c in categories],
                theta=categories,
                fill='toself',
                name='Portfolio Average'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=True,
                height=450
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
    with c4:
        st.markdown("### Competitor SWOT")
        if top_mol is not None:
            st.write(f"**Focus**: {top_mol['MOLECULE_DESC']}")
            
            s = "High Patent Protection and Strong Innovation." if top_mol['Patent Score'] > 7 else "Established Market Presence."
            w = "Weak Right-to-Win capabilities." if top_mol['Right to Win Score'] < 5 else "Generic erosion imminent." if top_mol['Patent Score'] < 4 else "High development costs."
            o = "High Future Opportunity and Growth." if top_mol['Future Score'] > 7 else "Stable cash-cow segment."
            t = "Fierce red-ocean competition." if top_mol['HHI'] < 1000 else "Monopolistic threats." if top_mol['HHI'] > 2500 else "Regulatory pricing pressure."
            
            st.info(f"**Strengths**: {s}")
            st.warning(f"**Weaknesses**: {w}")
            st.success(f"**Opportunities**: {o}")
            st.error(f"**Threats**: {t}")
            
            st.metric("Entry Barrier Score", f"{top_mol.get('Entry Barrier Score', 0):.1f}/10")

    st.markdown("---")
    
    # Helper function to render premium tables
    def render_premium_table(df, is_comp=False):
        table_html = """
<style>
.premium-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 86, 163, 0.08);
    margin-bottom: 24px;
    background-color: white;
}
.premium-table th {
    background-color: #0056A3;
    color: white;
    font-weight: 600;
    padding: 14px 16px;
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-align: left;
}
.premium-table td {
    padding: 14px 16px;
    border-bottom: 1px solid #E5E7EB;
    color: #374151;
    font-size: 0.95rem;
}
.premium-table tr:last-child td {
    border-bottom: none;
}
.premium-table tr:hover {
    background-color: #F8FAFC;
}
.tag-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
}
.tag-double-down { background: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
.tag-build { background: #DBEAFE; color: #1E40AF; border: 1px solid #BFDBFE; }
.tag-partner { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
.tag-monitor { background: #F3F4F6; color: #374151; border: 1px solid #E5E7EB; }
</style>
<table class="premium-table">
        """
        
        # Headers
        table_html += "<tr>"
        for col in df.columns:
            table_html += f"<th>{col}</th>"
        table_html += "</tr>"
        
        # Rows
        for _, row in df.iterrows():
            table_html += "<tr>"
            for col in df.columns:
                val = row[col]
                # Format Strategy/Recommendation as a bright pill badge
                if col in ['Strategy', 'Recommendation']:
                    s = str(val).lower()
                    tag_class = 'tag-monitor'
                    if 'double' in s: tag_class = 'tag-double-down'
                    elif 'build' in s: tag_class = 'tag-build'
                    elif 'partner' in s: tag_class = 'tag-partner'
                    table_html += f'<td><span class="tag-badge {tag_class}">{val}</span></td>'
                # Format numbers
                elif isinstance(val, (int, float)):
                    table_html += f"<td><b>{val:.1f}</b></td>"
                # Make Molecule Name / Opportunity bold blue
                elif col in ['MOLECULE_DESC', 'Opportunity']:
                    table_html += f'<td style="color:#0056A3; font-weight:700;">{val}</td>'
                else:
                    table_html += f"<td>{val}</td>"
            table_html += "</tr>"
            
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)


    # Section 3: Underpenetrated Opportunities
    st.markdown("### Section 3: Underpenetrated Opportunities")
    
    under_df = opp_df[(opp_df['Growth Score'] > 6) & (opp_df['Right to Win Score'] < 4)].copy()
    if not under_df.empty:
        st.markdown("The following attractive opportunity spaces appear underpenetrated by Cipla (High Market Growth, Low Current Share):")
        df_show = under_df[['MOLECULE_DESC', 'Growth Score', 'Right to Win Score', 'Opportunity Score', 'Strategy']].head(5)
        df_show.rename(columns={'MOLECULE_DESC': 'Opportunity Space'}, inplace=True)
        render_premium_table(df_show)
    else:
        st.warning("No major underpenetrated opportunities detected under current strict thresholds (Growth > 6, RTW < 4).")
        st.info("AI Explanation: The current portfolio is highly concentrated in mature, low-growth segments (Red Oceans). While some molecules show high growth, Cipla already has a dominant Right-to-Win score in them, meaning they are not 'underpenetrated'.")
        
        st.markdown("**Closest Potential White Spaces (Moderate Growth, Low Share):**")
        closest_df = opp_df[opp_df['Right to Win Score'] < 5].sort_values(by='Growth Score', ascending=False).head(3)
        df_show = closest_df[['MOLECULE_DESC', 'Growth Score', 'Right to Win Score', 'Strategy']].copy()
        df_show.rename(columns={'MOLECULE_DESC': 'Opportunity Space'}, inplace=True)
        render_premium_table(df_show)
        
    st.markdown("---")
    
    # Section 5: Competitor Intelligence
    st.markdown("### Section 5: Competitor Intelligence")
    
    comp_data = {
        "Opportunity": ["Amlodipine + Metoprolol", "Rosuvastatin", "Inclisiran"],
        "Competitor": ["Sun Pharma, Dr. Reddy's, Torrent", "Abbott, Lupin", "Novartis"],
        "Cipla Advantage": ["Distribution + physician trust", "Trusted brands / Brand recall", "Local presence / Low current presence"],
        "Recommendation": ["Double Down", "Partner", "Build Capability"]
    }
    comp_table = pd.DataFrame(comp_data)
    
    render_premium_table(comp_table, is_comp=True)
