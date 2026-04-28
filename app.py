import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# --- GLOBAL CONFIG ---
st.set_page_config(page_title="FPGA HFT Pro", layout="wide", page_icon="📟")

# Custom CSS for the "Hardware Console" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff41; font-family: 'Courier New', Courier, monospace; }
    .stMetric { border: 1px solid #00ff41; padding: 10px; border-radius: 5px; background: #161b22; }
    div[data-testid="stMetricValue"] { color: #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("⚡ FPGA HFT SYSTEM")
page = st.sidebar.radio("Navigation", ["1. Trading Pipeline", "2. Hardware Logic (RTL)", "3. Signal Integrity"])

# --- PAGE 1: TRADING PIPELINE ---
if page == "1. Trading Pipeline":
    st.header("🚀 Ultra-Low Latency Pipeline")
    st.subheader("Tick-to-Trade Simulation")
    
    col1, col2, col3 = st.columns(3)
    m1 = col1.empty()
    m2 = col2.empty()
    m3 = col3.empty()
    
    chart_placeholder = st.empty()
    log_placeholder = st.empty()
    
    # Simulation Data
    prices = [150.0]
    latencies = # Nanoseconds
    
    if st.button("Start Live Stream"):
        for i in range(30):
            # Generate dummy HFT data
            new_price = prices[-1] + np.random.normal(0, 0.05)
            new_lat = 420 + np.random.uniform(-5, 5)
            prices.append(new_price)
            latencies.append(new_lat)
            
            # Metrics
            m1.metric("Market Price", f"${new_price:.4f}")
            m2.metric("Pipeline Latency", f"{new_lat:.2f} ns", delta="-0.02 ns", delta_color="inverse")
            m3.metric("Throughput", "15.2M pps")
            
            # Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=prices, mode='lines+markers', name='Price', line=dict(color='#00ff41')))
            fig.update_layout(template="plotly_dark", height=300, margin=dict(l=0,r=0,t=0,b=0))
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            
            log_placeholder.code(f"EXECUTE ORDER: BUY 100 SHARES AT ${new_price:.4f} | RTT: {new_lat:.1f}ns")
            time.sleep(0.1)

# --- PAGE 2: HARDWARE LOGIC (RTL) ---
elif page == "2. Hardware Logic (RTL)":
    st.header("🧬 FPGA Gate-Level Simulation")
    st.write("Visualizing Register Transfer Level (RTL) data movement.")
    
    cols = st.columns(8)
    placeholders = [col.empty() for col in cols]
    
    st.markdown("### Data Bus State (AXI4-Stream)")
    bus_log = st.empty()

    if st.button("Simulate Clock Cycles"):
        for _ in range(20):
            # Animate Register bits
            for p in placeholders:
                active = np.random.choice([True, False])
                color = "#00ff41" if active else "#333"
                p.markdown(f"""<div style="height:60px; width:100%; background:{color}; border:1px solid white; border-radius:5px;"></div>""", unsafe_allow_html=True)
            
            hex_data = "".join(np.random.choice(list("0123456789ABCDEF"), 16))
            bus_log.markdown(f"`TX_DATA_BUS: 0x{hex_data} | VALID: 1 | READY: 1`")
            time.sleep(0.2)

# --- PAGE 3: SIGNAL INTEGRITY ---
elif page == "3. Signal Integrity":
    st.header("📡 Transceiver & Link Diagnostics")
    
    col_left, col_right = st.columns()
    
    with col_left:
        st.write("### Utilization")
        st.progress(0.72, text="LUT Usage (72%)")
        st.progress(0.45, text="BRAM (45%)")
        st.progress(0.90, text="DSP Slices (90%)")
    
    with col_right:
        st.write("### GT SerDes Eye Diagram (Simulated)")
        # Simulated "Eye Diagram" for high-speed serial links
        x = np.linspace(-1, 1, 1000)
        y = np.sin(x*np.pi) + np.random.normal(0, 0.05, 1000)
        
        fig = go.Figure()
        for i in range(10): # Overlap signals to create the "eye"
            fig.add_trace(go.Scatter(x=x, y=y + np.random.normal(0, 0.02), mode='lines', line=dict(width=1, color='rgba(0, 255, 65, 0.3)')))
        
        fig.update_layout(template="plotly_dark", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
