import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="FPGA HFT Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("⚡ FPGA HFT Lab")
    st.markdown("---")
    menu = st.radio(
        "Simulation Views",
        ["System Overview", "Pipeline Flow", "Latency Analysis", "Order Book & Packets", "Hardware Health"]
    )
    st.markdown("---")
    st.info("Status: FPGA Processing Active")

# --- Mock Data Generator ---
def get_mock_data():
    return {
        "latency": np.random.normal(1.2, 0.15, 100), # Microseconds
        "temp": 45 + np.random.uniform(0, 5),
        "power": 12.5 + np.random.uniform(0, 2),
        "utilization": {"LUT": 65, "FF": 42, "BRAM": 78}
    }

# --- 1. System Overview (Dashboard) ---
if menu == "System Overview":
    st.header("Real-Time HFT Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    data = get_mock_data()
    
    col1.metric("Tick-to-Trade", f"{data['latency'].mean():.3f} μs", "-0.002 μs")
    col2.metric("Packet Rate", "4.2M / sec", "+12k")
    col3.metric("FPGA Temp", f"{data['temp']:.1f} °C", "Stable")
    col4.metric("Uptime", "14d 02h", "100%")

    st.subheader("Profit & Loss (Simulated)")
    chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Strategy A', 'Strategy B']).cumsum()
    st.line_chart(chart_data)

# --- 2. Pipeline Flow (Logic Map) ---
elif menu == "Pipeline Flow":
    st.header("Hardware Logic Pipeline")
    st.write("Visualizing data movement through FPGA Gates.")
    
    # Using Graphviz for the Architecture Map
    st.graphviz_chart('''
        digraph G {
            rankdir=LR;
            node [shape=box, style=filled, color="#1f77b4", fontcolor=white, fontname="Arial"];
            "10G PHY" -> "Packet Parser" [label="Raw Frames"];
            "Packet Parser" -> "LOB Engine" [label="Price Updates"];
            "LOB Engine" -> "Strategy Logic" [label="Book Depth"];
            "Strategy Logic" -> "Order Generator" [label="Signal"];
            "Order Generator" -> "MAC/TX" [label="FIX/Binary"];
            
            subgraph cluster_0 {
                label = "Ultra-Low Latency Core";
                color = "#ff4b4b";
                "LOB Engine"; "Strategy Logic";
            }
        }
    ''')
    st.success("Current State: All stages running within 250ns clock cycles.")

# --- 3. Latency Analysis (Ridge Plot) ---
elif menu == "Latency Analysis":
    st.header("Microsecond Latency Distribution")
    
    @st.fragment(run_every=2)
    def show_latency():
        latencies = np.random.lognormal(mean=0.2, sigma=0.1, size=1000)
        fig = px.histogram(latencies, nbins=50, title="Wire-to-Wire Latency (μs)",
                           color_discrete_sequence=['#00f2ff'])
        fig.update_layout(template="plotly_dark", bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Monitoring tail latency (P99.9) to ensure deterministic execution.")
    
    show_latency()

# --- 4. Order Book & Packets ---
elif menu == "Order Book & Packets":
    st.header("Live Order Book (L2 Depth)")
    
    col1, col2 = st.columns()
    
    with col1:
        # Mock Ladder Data - Ensure no hidden spaces exist here
        ladder_data = {
            'Price': [150.10, 150.09, 150.08, 150.07, 150.06],
            'Size':
        }
        df = pd.DataFrame(ladder_data)
        st.table(df)
        
    with col2:
        st.subheader("Raw Packet Stream (Parser View)")
        st.code("""
[RX] 0x48 0x65 0x6c 0x6c 0x6f ... ID: 8829 | T: 14:02:01.000342
[TX] 0x5a 0x21 0x0c 0x00 0x12 ... NEW ORDER | T: 14:02:01.000343
[RX] 0x48 0x65 0x6c 0x6c 0x6f ... ID: 8830 | T: 14:02:01.000345
        """, language="bash")

# --- 5. Hardware Health ---
elif menu == "Hardware Health":
    st.header("FPGA Resource Utilization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        labels = ['LUTs', 'Flip-Flops', 'BRAM', 'DSP Slices']
        values =
        fig = px.pie(names=labels, values=values, hole=0.4, title="Resource Usage")
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig)
        
    with col2:
        st.subheader("Power & Thermal Simulation")
        progress = st.progress(0)
        for i in range(72):
            progress.progress(i + 1)
        st.write("Core Temperature: **72°C**")
        st.warning("Warning: BRAM usage exceeding 75% threshold.")
