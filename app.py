import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="FPGA HFT Simulator", layout="wide")
st.title("⚡ FPGA-Based High-Frequency Trading Simulation")

# Sidebar - FPGA Parameters
st.sidebar.header("Hardware Configuration")
clock_speed = st.sidebar.slider("FPGA Clock Speed (MHz)", 100, 400, 250)
pipeline_stages = st.sidebar.number_input("Pipeline Stages", 4, 12, 8)
strategy_type = st.sidebar.selectbox("Strategy Logic", ["Market Making", "Cross-Exchange Arb", "Trend Follow"])

# --- DATA GENERATION ---
def get_market_data():
    # Simulating a raw packet stream (e.g., NASDAQ ITCH 5.0)
    return {
        "timestamp": datetime.now(),
        "price": 150.00 + np.random.normal(0, 0.5),
        "bid": 149.95,
        "ask": 150.05,
        "volume": np.random.randint(100, 1000)
    }

# --- SIMULATION LAYOUT ---
col1, col2, col3 = st.columns()

# Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Price', 'Latency_ns'])

# Simulation Loop
run = st.checkbox("Start Live Pipeline")

if run:
    placeholder = st.empty()
    
    while run:
        with placeholder.container():
            data = get_market_data()
            
            # Simulate FPGA Latency (Deterministic)
            # Logic: Latency = (1 / Clock) * Stages * jitter_factor
            base_latency = (1 / clock_speed) * pipeline_stages * 1000 # in ns
            sim_latency = base_latency + np.random.uniform(0, 2) # Minimal jitter
            
            # --- VISUAL 1: Metrics ---
            m1, m2, m3 = st.columns(3)
            m1.metric("Current Price", f"${data['price']:.2f}")
            m2.metric("Pipeline Latency", f"{sim_latency:.2f} ns", delta="-0.05 ns")
            m3.metric("Throughput", f"{clock_speed / 2:.1f} M pps")

            # --- VISUAL 2: Hardware Pipeline Status ---
            st.subheader("Hardware Pipeline Flow")
            cols = st.columns(4)
            stages = ["UDP Parser", "Order Book", "Strategy Engine", "FIX Generator"]
            for i, stage in enumerate(stages):
                with cols[i]:
                    st.success(f"Stage {i+1}: {stage}")
                    st.caption("Active ✅")

            # --- VISUAL 3: Real-time Plot ---
            new_row = {'Time': data['timestamp'], 'Price': data['price'], 'Latency_ns': sim_latency}
            st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])]).tail(30)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=st.session_state.history['Time'], y=st.session_state.history['Price'],
                                     mode='lines+markers', name='Market Price'))
            fig.update_layout(height=400, template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)

            time.sleep(0.1) # UI throttle
