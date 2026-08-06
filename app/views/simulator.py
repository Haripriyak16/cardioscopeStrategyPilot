import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render(opp_df, raw_df):
    st.title("Scenario Simulator")
    
    st.markdown("Adjust macro variables to see real-time impact on Opportunity Rankings and Confidence.")
    
    colA, colB = st.columns([1, 2])
    with colA:
        st.markdown("### Simulation Parameters")
        comp_mod = st.slider("Competitive Intensity Multiplier", 0.5, 2.0, 1.0, 0.1)
        growth_mod = st.slider("Market Growth Multiplier", 0.5, 2.0, 1.0, 0.1)
        disease_mod = st.slider("Disease Burden Multiplier", 0.5, 2.0, 1.0, 0.1)
        patent_mod = st.slider("Patent Delay (Years Extension)", -5.0, 5.0, 0.0, 1.0)
        pricing_mod = st.slider("Pricing Power Multiplier", 0.5, 1.5, 1.0, 0.1)
        hc_spend_mod = st.slider("Healthcare Spending Multiplier", 0.5, 2.0, 1.0, 0.1)
        reg_mod = st.slider("Regulation Strictness Multiplier", 0.5, 2.0, 1.0, 0.1)
        adopt_mod = st.slider("Physician Adoption Multiplier", 0.5, 2.0, 1.0, 0.1)
    
    with colB:
        st.markdown("### Live Scenario Results")
        
        sim_df = opp_df.copy()
        
        # Apply multipliers to sub-scores
        sim_df['Competition Score'] = (sim_df['Competition Score'] / comp_mod).clip(0, 10) # Inverse
        sim_df['Growth Score'] = (sim_df['Growth Score'] * growth_mod * hc_spend_mod).clip(0, 10)
        sim_df['Disease Score'] = (sim_df['Disease Score'] * disease_mod).clip(0, 10)
        sim_df['Patent Score'] = (sim_df['Patent Score'] + patent_mod).clip(0, 10)
        sim_df['Regulatory Score'] = (sim_df['Regulatory Score'] / reg_mod).clip(0, 10)
        sim_df['Right to Win Score'] = (sim_df['Right to Win Score'] * adopt_mod * pricing_mod).clip(0, 10)
        
        # Re-calc Future Score
        sim_df['Future Score'] = (sim_df['Disease Score']*0.3 + sim_df['Patent Score']*0.3 + sim_df['Regulatory Score']*0.2 + sim_df['Innovation Score']*0.2)
        
        # Re-calc Opportunity Score
        w_market = 0.25
        w_growth = 0.20
        w_comp = 0.15
        w_future = 0.20
        w_rtw = 0.20
        
        sim_df['Opportunity Score'] = (
            sim_df['Market Score'] * w_market +
            sim_df['Growth Score'] * w_growth +
            sim_df['Competition Score'] * w_comp +
            sim_df['Future Score'] * w_future +
            sim_df['Right to Win Score'] * w_rtw
        ) * 10
        sim_df['Opportunity Score'] = sim_df['Opportunity Score'].clip(0, 100).round(1)
        
        # Re-calc Confidence Score based on parameter extremeness
        extremeness = abs(1-comp_mod) + abs(1-growth_mod) + abs(1-disease_mod) + abs(1-hc_spend_mod) + abs(1-reg_mod) + abs(1-adopt_mod) + abs(1-pricing_mod) + (abs(patent_mod)/5)
        sim_df['Confidence Score'] = (sim_df['Confidence Score'] - (extremeness * 5)).clip(0, 100).round(1)
        
        sim_df = sim_df.sort_values(by='Opportunity Score', ascending=False).reset_index(drop=True)
        sim_df['Rank'] = sim_df.index + 1
        
        merged = pd.merge(sim_df[['MOLECULE_DESC', 'Rank', 'Opportunity Score', 'Confidence Score']], 
                          opp_df[['MOLECULE_DESC', 'Rank', 'Opportunity Score']], 
                          on='MOLECULE_DESC', suffixes=('_Simulated', '_Original'))
        
        merged['Rank Change'] = merged['Rank_Original'] - merged['Rank_Simulated']
        
        # Highlight top 10 changes
        st.dataframe(merged.head(15), use_container_width=True)
        
        st.markdown("### Impact Analysis")
        # Waterfall chart of opportunity shift for top molecule
        top_mol_orig = opp_df[opp_df['MOLECULE_DESC'] == merged.iloc[0]['MOLECULE_DESC']].iloc[0]
        top_mol_sim = sim_df.iloc[0]
        
        delta = top_mol_sim['Opportunity Score'] - top_mol_orig['Opportunity Score']
        color = "green" if delta >= 0 else "red"
        st.metric(f"Impact on {top_mol_sim['MOLECULE_DESC']} (Opportunity Index)", f"{top_mol_sim['Opportunity Score']:.1f}", f"{delta:.1f}")
