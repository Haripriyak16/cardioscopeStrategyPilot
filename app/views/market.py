import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

CIPLA_BLUES = ["#0056A3", "#003366", "#66AEDC", "#3384C4", "#99CCE8", "#004482"]

def render(opp_df, raw_df):
    st.title("Market Intelligence")
    
    # Export Options
    st.markdown("### Export Data")
    csv = opp_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Market Data (CSV)", data=csv, file_name="market_intelligence.csv", mime="text/csv")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Market Structure", "Growth Matrix", "Value Distribution"])
    
    with tab1:
        st.markdown("### Therapy Area Overview (Sunburst)")
        fig_sun = px.sunburst(opp_df, path=['Strategy', 'MOLECULE_DESC'], values='Opportunity Score',
                              title="Strategy & Molecule Composition", color='Opportunity Score', color_continuous_scale='Blues')
        fig_sun.update_layout(height=600)
        st.plotly_chart(fig_sun, use_container_width=True)
        
        st.markdown("### Segment Hierarchy (Treemap)")
        if "CARDIAC SEGMENT" in raw_df.columns:
            seg_df = raw_df.groupby("CARDIAC SEGMENT").agg({"MAT FEB'26": 'sum'}).reset_index()
            seg_df = seg_df[seg_df["MAT FEB'26"] > 0]
            fig_tree = px.treemap(seg_df, path=["CARDIAC SEGMENT"], values="MAT FEB'26",
                                  title="Market Size by Cardiac Segment", color="MAT FEB'26", color_continuous_scale='Blues')
            st.plotly_chart(fig_tree, use_container_width=True)
            
    with tab2:
        st.markdown("### Growth vs Market Size (Bubble Matrix)")
        opp_df_sorted = opp_df.sort_values(by="Opportunity Score", ascending=False)
        fig_bubble = px.scatter(opp_df_sorted, x="Market Score", y="Growth Score",
                                size="Opportunity Score", color="Strategy",
                                hover_name="MOLECULE_DESC", size_max=50,
                                title="Molecule Landscape: Growth vs Size",
                                color_discrete_sequence=CIPLA_BLUES,
                                labels={"Market Score": "Market Attractiveness (0-10)", "Growth Score": "Growth Potential (0-10)"})
        fig_bubble.add_vline(x=5, line_width=1, line_dash="dash", line_color="rgba(0,86,163,0.3)")
        fig_bubble.add_hline(y=5, line_width=1, line_dash="dash", line_color="rgba(0,86,163,0.3)")
        fig_bubble.update_layout(height=600)
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    with tab3:
        colA, colB = st.columns(2)
        with colA:
            st.markdown("### Top Molecule Value (Waterfall)")
            if not opp_df.empty:
                top = opp_df.iloc[0]
                fig_water = go.Figure(go.Waterfall(
                    name="2026", orientation="v",
                    measure=["relative", "relative", "relative", "relative", "relative", "total"],
                    x=["Market Base", "Growth Premium", "Patent Premium", "Innovation", "Regulatory", "Final Score"],
                    y=[top['Market Score']*2, top['Growth Score']*2, top['Patent Score']*2, top['Innovation Score']*2, top['Regulatory Score']*2, top['Opportunity Score']],
                    connector={"line":{"color":"rgb(63, 63, 63)"}},
                ))
                fig_water.update_layout(title=f"Value Build: {top['MOLECULE_DESC']}")
                st.plotly_chart(fig_water, use_container_width=True)
                
        with colB:
            st.markdown("### Pareto Analysis (Opportunity Concentration)")
            df_pareto = opp_df.sort_values(by='Opportunity Score', ascending=False).head(20).reset_index(drop=True)
            df_pareto['Cumulative'] = df_pareto['Opportunity Score'].cumsum() / df_pareto['Opportunity Score'].sum() * 100
            
            fig_pareto = go.Figure([
                go.Bar(x=df_pareto['MOLECULE_DESC'], y=df_pareto['Opportunity Score'], name="Opportunity Score"),
                go.Scatter(x=df_pareto['MOLECULE_DESC'], y=df_pareto['Cumulative'], name="Cumulative %", yaxis="y2", mode='lines+markers', line=dict(color='#003366'))
            ])
            fig_pareto.update_layout(
                title="Top 20 Molecules Pareto (80/20 Rule)",
                yaxis=dict(title="Score"),
                yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105])
            )
            st.plotly_chart(fig_pareto, use_container_width=True)
