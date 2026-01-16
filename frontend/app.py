import streamlit as st
from pyvis.network import Network
import torch
import networkx as nx
import streamlit.components.v1 as components
import os
import requests
import random

# 1. Setup & Session State
st.set_page_config(layout="wide", page_title="Dharma-Nexus: Market Simulator", page_icon="🕸️")

# Initialize persistent session graph
if 'G' not in st.session_state:
    st.session_state.G = nx.Graph()
    # Initial seed nodes
    for i in range(15):
        st.session_state.G.add_node(i, label=f"User {i}", color="#4ade80", size=15, title="Verified")
    for _ in range(20):
        st.session_state.G.add_edge(random.randint(0,14), random.randint(0,14))

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 8px; }
    .web-of-trust { background-color: #161b22; border: 2px solid #6366f1; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕸️ Dharma-Debt Nexus: Live Market Simulator")
st.markdown("---")

col1, col2, col3 = st.columns([1, 2.2, 1.3])

# --- COLUMN 1: LIVE USER INJECTION ---
with col1:
    st.subheader("🆕 Add New Borrower")
    new_user_id = st.text_input("Borrower Name/ID", f"User_{random.randint(100,999)}")
    age = st.slider("Age", 18, 80, 25)
    income = st.number_input("Monthly Income (₹)", value=25000)
    dharma = st.slider("Dharma Score", 0.0, 1.0, 0.3)
    
    st.markdown("### 🔗 Connectivity")
    neighbor_id = st.number_input("Connect to Existing Node ID", min_value=0, max_value=len(st.session_state.G.nodes)-1, value=0)
    
    if st.button("🚀 Simulate Market Entry"):
        # Explicitly use the local host address
        API_URL = "https://api.dishasingh.xyz/predict"
        payload = {"age": age, "income": income, "dharma_score": dharma}
        
        try:
            res = requests.post(API_URL, json=payload, timeout=5)
            if res.status_code == 200:
                data = res.json()
                # Support both simple string and complex dict responses
                prediction = data.get('prediction', data) if isinstance(data, dict) else data
                is_high_risk = "High Risk" in str(prediction)
                risk_color = "#f87171" if is_high_risk else "#4ade80"
                
                # Update Session Graph
                new_node_idx = len(st.session_state.G.nodes)
                st.session_state.G.add_node(new_node_idx, label=new_user_id, color=risk_color, size=30, title=f"Risk: {prediction}")
                st.session_state.G.add_edge(new_node_idx, neighbor_id)
                
                # CONTAGION: Influence neighbor
                if is_high_risk:
                    st.session_state.G.nodes[neighbor_id]['color'] = "#fbbf24" # Warning Orange
                    st.session_state.G.nodes[neighbor_id]['title'] = "⚠️ Contagion Warning: Direct connection to default risk"
                
                st.session_state.last_prediction = prediction
                st.session_state.last_id = new_user_id
                st.session_state.last_neighbor = neighbor_id
                st.rerun() 
            else:
                st.error(f"API Error: {res.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Connection Failed. Verify API is running at http://127.0.0.1:8000")

# --- COLUMN 2: THE VISUAL WEB ---
with col2:
    st.subheader("🌐 Relational Topology")
    net = Network(height="600px", width="100%", bgcolor="#0e1117", font_color="white")
    net.from_nx(st.session_state.G)
    net.toggle_physics(True)
    net.set_options('{"physics": {"forceAtlas2Based": {"gravitationalConstant": -100, "springLength": 100}, "solver": "forceAtlas2Based"}}')
    
    net.save_graph("live_nexus.html")
    with open("live_nexus.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=620)

# --- COLUMN 3: ANALYSIS ---
with col3:
    st.subheader("🧠 Web of Trust Analysis")
    if 'last_prediction' in st.session_state:
        st.markdown(f"### Target: **{st.session_state.last_id}**")
        st.markdown('<div class="web-of-trust">', unsafe_allow_html=True)
        st.write(f"📍 Linked to **Node {st.session_state.last_neighbor}**.")
        if "High Risk" in str(st.session_state.last_prediction):
            st.write("🔴 **Risk Detected:** Connection creates a default-risk bridge.")
            st.write(f"🔸 **Contagion:** Node {st.session_state.last_neighbor} flagged (Orange).")
        else:
            st.write("🟢 **Trust Verified:** Social proximity to stable clusters.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.metric("Total Nexus Nodes", len(st.session_state.G.nodes))
    else:
        st.info("Simulate an entry to start.")  