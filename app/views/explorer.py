import streamlit as st
import plotly.graph_objects as go
import json

def render(opp_df, raw_df):
    st.title("Opportunity Explorer")
    
    st.markdown("Deep dive into specific molecules and clusters.")
    
    # Search
    search_term = st.text_input("Search by Molecule Name", "")
    if search_term:
        filtered_df = opp_df[opp_df['MOLECULE_DESC'].str.contains(search_term, case=False, na=False)]
    else:
        filtered_df = opp_df
        
    # Full V2 Table
    display_cols = [
        'Rank', 'MOLECULE_DESC', 'Investment Matrix', 'Strategy', 'Opportunity Score', 
        'Confidence Score', 'Strategic Fit Score', 'Business Impact Score', 'Risk Score',
        'Market Score', 'Growth Score', 'Patent Score', 'Innovation Score'
    ]
    st.dataframe(filtered_df[[c for c in display_cols if c in filtered_df.columns]], use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Executive Deep Dive")
    if not filtered_df.empty:
        mol = st.selectbox("Select Molecule for Deep Dive", filtered_df['MOLECULE_DESC'].unique())
        mol_data = filtered_df[filtered_df['MOLECULE_DESC'] == mol].iloc[0]
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Opportunity Index", f"{mol_data['Opportunity Score']:.1f}/100")
        c2.metric("Confidence Score", f"{mol_data['Confidence Score']:.1f}%")
        c3.metric("Strategic Fit", f"{mol_data.get('Strategic Fit Score', 0):.1f}/100")
        c4.metric("Business Impact", f"{mol_data.get('Business Impact Score', 0):.1f}/100")
        
        # AI Reasoning Chain
        st.markdown("### AI Reasoning Chain")
        st.markdown("The recommendation is procedurally generated through the following decision nodes:")
        rc1, rc2, rc3, rc4, rc5 = st.columns(5)
        rc1.info(f"**1. Market & Growth**\n\nAttractiveness: {mol_data['Market Score']}/10\nGrowth: {mol_data['Growth Score']}/10")
        rc2.info(f"**2. Competition**\n\nIntensity: {mol_data['Competition Score']}/10\nHHI Score: {mol_data.get('HHI', 0):.0f}")
        rc3.info(f"**3. External**\n\nPatent/Innovation: {mol_data.get('Future Opportunity Score', 0):.1f}/10")
        rc4.info(f"**4. Right-to-Win**\n\nCapability Match: {mol_data['Right to Win Score']}/10")
        rc5.success(f"**5. Decision**\n\n{mol_data.get('Investment Matrix', mol_data['Strategy'])}")
        
        st.markdown("---")
        
        colA, colB, colC = st.columns([1, 1, 1])
        with colA:
            # Radar chart
            categories = ['Market Score', 'Growth Score', 'Competition Score', 'Future Score', 'Right to Win Score']
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[mol_data[c] for c in categories],
                theta=categories,
                fill='toself',
                name=mol
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False, title="Strategic Footprint", margin=dict(t=30, b=30, l=30, r=30))
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with colB:
            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = mol_data['Opportunity Score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Opportunity Index"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#007bff"},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255,0,0,0.1)"},
                        {'range': [50, 70], 'color': "rgba(255,255,0,0.1)"},
                        {'range': [70, 100], 'color': "rgba(0,255,0,0.1)"}
                    ]
                }
            ))
            fig_gauge.update_layout(margin=dict(t=30, b=30, l=30, r=30))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with colC:
            st.markdown("#### AI Executive Summary")
            exp = mol_data.get('Explanation_Dict', {})
            if exp:
                st.success("**Why?**")
                for w in exp.get('Why', []): st.write(f"- {w}")
                st.error("**Why Not?**")
                for w in exp.get('Why Not', []): st.write(f"- {w}")
                st.warning("**Trade-offs & Risks**")
                for r in exp.get('Risks', []): st.write(f"- {r}")
                for t in exp.get('Trade-offs', []): st.write(f"- {t}")
            else:
                st.write(mol_data['Explanation'])
