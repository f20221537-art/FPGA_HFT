import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="FPGA HFT Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("⚡ FPGA HFT Lab")
    st.markdown("---")
    menu = st.radio(
        "Simulation Views",
        ["System Overview", "Pipeline Flow", "Latency Analysis", "Order Book & Packets", "Hardware Health"]
    )
    st.markdown("---")
    st.info("Status: FPGA Simulation Active")

# --- 1. System Overview ---
if menu == "System Overview":
    st.header("Real-Time HFT Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Tick-to-Trade", "1.102 μs", "-0.002 μs")
    col2.metric("Packet Rate", "4.2M / sec", "+12k")
    col3.metric("FPGA Temp", "48.5 °C", "Stable")
    col4.metric("Uptime", "14d 02h", "100%")

    st.subheader("Profit & Loss (Simulated Strategy)")
    chart_data = pd.DataFrame(
        np.random.randn(50, 2).cumsum(axis=0), 
        columns=['Arbitrage Core', 'Market Maker']
    )
    st.line_chart(chart_data)

# --- 2. Pipeline Flow ---
elif menu == "Pipeline Flow":
    st.header("Hardware Logic Pipeline")
    st.write("Visualizing data movement through FPGA RTL Gates.")
    
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

# --- 3. Latency Analysis ---
elif menu == "Latency Analysis":
    st.header("Microsecond Latency Distribution")
    
    @st.fragment(run_every=2)
    def show_latency():
        latencies = np.random.lognormal(mean=0.1, sigma=0.05, size=1000)
        fig = px.histogram(
            latencies, 
            nbins=50, 
            title="Wire-to-Wire Latency (μs)",
            color_discrete_sequence=['#00f2ff']
        )
        fig.update_layout(template="plotly_dark", bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
    
    show_latency()

# --- 4. Order Book & Packets (FIXED SECTION) ---
elif menu == "Order Book & Packets":
    st.header("Live Order Book (L2 Depth)")
    
    col1, col2 = st.columns()
    
    with col1:
        # Simplified dictionary to prevent SyntaxError
        prices = [150.10, 150.09, 150.08, 150.07, 150.06]
        sizes =
        df_ladder = pd.DataFrame({"Price": prices, "Size": sizes})
        st.table(df_ladder)
        
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
        st.subheader("System Health")
        st.progress(72, text="Core Temperature: 72°C")
        st.warning("BRAM usage approaching 80% limit.")
