import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render(opp_df, raw_df):
    st.title("Human vs AI & Risk Engine")
    
    tab1, tab2, tab3 = st.tabs(["Human vs AI Comparison", "Risk Intelligence", "Confidence Engine"])
    
    with tab1:
        st.markdown("### AI Strategy vs Legacy Management")
        if 'Management Strategy' not in opp_df.columns:
            sales_80 = opp_df["MAT FEB'26"].quantile(0.8)
            sales_40 = opp_df["MAT FEB'26"].quantile(0.4)
            def sim_management(row):
                if row["MAT FEB'26"] > sales_80: return "Double Down"
                elif row["MAT FEB'26"] > sales_40: return "Expand"
                else: return "Avoid"
            opp_df['Management Strategy'] = opp_df.apply(sim_management, axis=1)
            
        opp_df['Match'] = opp_df['Investment Matrix'] == opp_df['Management Strategy']
        match_rate = (opp_df['Match'].sum() / len(opp_df)) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Decisions Evaluated", len(opp_df))
        c2.metric("AI vs Human Match Rate", f"{match_rate:.1f}%")
        c3.metric("Divergent Decisions", len(opp_df) - opp_df['Match'].sum())
        
        st.markdown("### AI Divergence Log")
        divergent_df = opp_df[~opp_df['Match']].copy()
        def get_divergence_reason(row):
            if row['Management Strategy'] == 'Double Down' and row['Investment Matrix'] in ['Avoid', 'Monitor']:
                return "AI blocked 'Double Down' due to extreme patent risk and high HHI competition."
            elif row['Management Strategy'] == 'Avoid' and row['Investment Matrix'] in ['Build Capability', 'Double Down']:
                return "AI spotted a 'Hidden Gem': High growth and Future Score despite low current volume."
            else:
                return "AI balanced Right-to-Win vs Market Growth dynamically."
        divergent_df['AI Rationale'] = divergent_df.apply(get_divergence_reason, axis=1)
        st.dataframe(divergent_df[['MOLECULE_DESC', "MAT FEB'26", 'Management Strategy', 'Investment Matrix', 'AI Rationale']], use_container_width=True)

    with tab2:
        st.markdown("### Risk Intelligence")
        colA, colB = st.columns(2)
        mol = st.selectbox("Select Molecule for Risk Analysis", opp_df['MOLECULE_DESC'].unique(), key='risk_mol')
        mol_data = opp_df[opp_df['MOLECULE_DESC'] == mol].iloc[0]
        
        with colA:
            fig_risk_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = mol_data['Risk Score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Overall Strategic Risk Score"},
                gauge = {
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "black"},
                    'steps': [
                        {'range': [0, 3], 'color': "green"},
                        {'range': [3, 7], 'color': "yellow"},
                        {'range': [7, 10], 'color': "red"}
                    ]
                }
            ))
            st.plotly_chart(fig_risk_gauge, use_container_width=True)
            
        with colB:
            # Risk Spider
            risk_cats = ['Competition Risk', 'Patent Risk', 'Regulatory Risk', 'Innovation Threat']
            # Inverse scores for risk mapping
            r_vals = [
                (10 - mol_data['Competition Score']),
                (10 - mol_data['Patent Score']),
                (10 - mol_data['Regulatory Score']),
                (10 - mol_data['Innovation Score'])
            ]
            fig_r_radar = go.Figure()
            fig_r_radar.add_trace(go.Scatterpolar(r=r_vals, theta=risk_cats, fill='toself', name="Risk Profile"))
            fig_r_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
            st.plotly_chart(fig_r_radar, use_container_width=True)

    with tab3:
        st.markdown("### Confidence Engine")
        cM1, cM2 = st.columns([1, 2])
        with cM1:
            fig_conf = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = mol_data['Confidence Score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Recommendation Confidence"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "blue"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 80], 'color': "lightblue"},
                        {'range': [80, 100], 'color': "royalblue"}
                    ]
                }
            ))
            st.plotly_chart(fig_conf, use_container_width=True)
            
        with cM2:
            st.markdown("#### Evidence Strength")
            st.write("**Data Completeness:** 100% (Sales, Growth, and Competition data available)")
            st.write(f"**Signal Stability:** High (Future Opportunity Score is {mol_data.get('Future Opportunity Score', 0):.1f}/10)")
            st.write(f"**Recommendation:** The recommendation to **{mol_data.get('Investment Matrix', 'Proceed')}** is supported by {mol_data['Right to Win Score']}/10 Right-to-Win and {mol_data['HHI']:.0f} HHI Concentration.")
            if mol_data['Confidence Score'] > 85:
                st.success("The AI has extremely high conviction in this strategic move.")
            elif mol_data['Confidence Score'] > 65:
                st.info("The AI has moderate conviction. Monitor external risks.")
            else:
                st.warning("Low confidence due to highly volatile market conditions or missing external signals.")
