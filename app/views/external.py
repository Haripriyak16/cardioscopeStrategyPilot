import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render(opp_df, raw_df):
    st.title("External Intelligence")
    st.markdown("### Macro & Future Signals")
    
    st.caption("Visualizing Disease Burden, Patent Expiry, Clinical Guidelines, Innovation Pipeline, and Regulatory Trends.")
    
    # Top Metrics
    top_mol = opp_df.iloc[0] if not opp_df.empty else None
    if top_mol is not None:
        st.markdown(f"**Focus Molecule**: {top_mol['MOLECULE_DESC']}")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Disease Burden", f"{top_mol['Disease Score']}/10")
        c2.metric("Patent Expiry", f"{top_mol['Patent Score']}/10")
        c3.metric("Clinical Guidelines", f"{top_mol['Guideline Score']}/10")
        c4.metric("Innovation Pipeline", f"{top_mol['Innovation Score']}/10")
        c5.metric("Regulatory Trends", f"{top_mol['Regulatory Score']}/10")
        c6.metric("Future Opp Score™", f"{top_mol.get('Future Opportunity Score', 0):.1f}/10")
        st.markdown("---")
        
    df_top = opp_df.head(20).copy()
    
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### External Factor Distribution")
        fig = px.parallel_coordinates(df_top, color="Future Opportunity Score", 
                                      dimensions=['Disease Score', 'Patent Score', 'Innovation Score', 'Guideline Score', 'Regulatory Score'],
                                      color_continuous_scale='Blues',
                                      color_continuous_midpoint=df_top['Future Opportunity Score'].mean())
        st.plotly_chart(fig, use_container_width=True)
        
    with colB:
        st.markdown("### Deep Dive Radar")
        mol = st.selectbox("Select Molecule for External Profile", opp_df['MOLECULE_DESC'].unique())
        mol_data = opp_df[opp_df['MOLECULE_DESC'] == mol].iloc[0]
        
        categories = ['Disease Score', 'Patent Score', 'Innovation Score', 'Guideline Score', 'Regulatory Score']
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[mol_data[c] for c in categories],
            theta=categories,
            fill='toself',
            name=mol
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig_radar, use_container_width=True)
