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
