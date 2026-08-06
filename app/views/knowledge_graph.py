import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import numpy as np

def render(opp_df, raw_df):
    st.title("Strategic Knowledge Graph")
    st.markdown("Visualizing the interconnectivity between Cardiac Segments, Molecules, Competitors, and Strategic Recommendations.")
    
    G = nx.Graph()
    
    # Let's limit to top 15 molecules to avoid massive hairball
    top_df = opp_df.head(15)
    
    # Add nodes
    # Strategies
    strategies = top_df['Investment Matrix'].unique()
    for s in strategies:
        G.add_node(s, type='Strategy', color='#003366', size=40)

    for _, row in top_df.iterrows():
        mol = row['MOLECULE_DESC']
        strat = row['Investment Matrix']
        G.add_node(mol, type='Molecule', color='#0056A3', size=30)
        G.add_edge(mol, strat)
        
    # Competitors and Segments from raw_df
    if "CARDIAC SEGMENT" in raw_df.columns and "COMPANY" in raw_df.columns:
        # We need to map molecule to segment. We can do an approximation or just use raw_df
        # Since opp_df has MOLECULE_DESC and raw_df has MOLECULE_DESC
        for mol in top_df['MOLECULE_DESC']:
            m_data = raw_df[raw_df['MOLECULE_DESC'] == mol]
            if not m_data.empty:
                seg = m_data['CARDIAC SEGMENT'].iloc[0]
                # Add top competitor
                top_comp = m_data.sort_values("MAT FEB'26", ascending=False)['COMPANY'].iloc[0]

                G.add_node(seg, type='Segment', color='#66AEDC', size=35)
                G.add_edge(mol, seg)

                G.add_node(top_comp, type='Competitor', color='#99CCE8', size=25)
                G.add_edge(mol, top_comp)

    pos = nx.spring_layout(G, seed=42)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#B0C4D9'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_color.append(G.nodes[node]['color'])
        node_size.append(G.nodes[node]['size'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="bottom center",
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title=dict(text='<br>Strategic Knowledge Graph', font=dict(size=16)),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.info("Segments: light blue | Molecules: Cipla blue | Strategies: navy | Competitors: pale blue")
