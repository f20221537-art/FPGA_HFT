import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration - Must be the first Streamlit command
st.set_page_config(
    page_title="FPGA HFT Monitor", 
    page_icon="⚡", 
    layout="wide"
)

# Custom CSS for a "Hardware Terminal" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Ultra-Low Latency FPGA HFT Pipeline")
st.markdown("---")

# --- SIDEBAR: HARDWARE CONTROLS ---
st.sidebar.header("FPGA Logic Configuration")
clock_mhz = st.sidebar.slider("Clock Speed (MHz)", 100, 450, 322) # 322MHz is standard for 10G/25G
pipeline_depth = st.sidebar.slider("Pipeline Stages", 2, 20, 8)
show_raw_packets = st.sidebar.toggle("Stream Raw Hex Packets", value=True)

# --- SIMULATION ENGINE ---
def simulate_fpga_processing(price, clock, stages):
    """Calculates deterministic hardware latency."""
    # FPGA Latency = (Cycles / Frequency) + wire delay
    # 322MHz cycle is ~3.1ns
    cycle_time_ns = 1000 / clock
    logic_latency = cycle_time_ns * stages
    # Add minimal jitter to simulate transceiver noise (0.1 - 0.5ns)
    total_ns = logic_latency + np.random.uniform(0.1, 0.5)
    return total_ns

# Initialize Session Data
if 'trade_log' not in st.session_state:
    st.session_state.trade_log = pd.DataFrame(columns=['Time', 'Price', 'Latency'])

# --- MAIN DASHBOARD ---
# FIXED: Passing an integer to columns()
col1, col2, col3 = st.columns(3)

placeholder = st.empty()
run_sim = st.sidebar.button("Execute Pipeline")

if run_sim:
    for _ in range(50):  # Run for 50 iterations
        with placeholder.container():
            # 1. Generate Fake Market Data
            current_price = 150.00 + np.random.normal(0, 0.1)
            latency = simulate_fpga_processing(current_price, clock_mhz, pipeline_depth)
            
            # 2. Top Level Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Market Price", f"${current_price:.4f}")
            m2.metric("Tick-to-Trade", f"{latency:.2f} ns", delta="-0.02ns", delta_color="inverse")
            m3.metric("Link Status", "25GbE Up", delta="0 Packets Dropped")

            # 3. Pipeline Visualization
            st.write("### Internal Logic State")
            p_cols = st.columns(4)
            stages = ["PHY/MAC", "Parser", "Book Builder", "Strategy"]
            for i, s in enumerate(stages):
                p_cols[i].info(f"**{s}**\n\nProcessing...")

            # 4. Latency Graph
            new_entry = {'Time': datetime.now(), 'Price': current_price, 'Latency': latency}
            st.session_state.trade_log = pd.concat([st.session_state.trade_log, pd.DataFrame([new_entry])]).tail(20)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=st.session_state.trade_log['Time'], 
                y=st.session_state.trade_log['Latency'],
                line=dict(color='#00ff00', width=2),
                fill='tozeroy',
                name='Latency (ns)'
            ))
            fig.update_layout(
                title="Deterministic Latency Profile",
                template="plotly_dark",
                height=300,
                yaxis_title="Nanoseconds",
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

            if show_raw_packets:
                st.caption(f"Raw Frame Trace: `0x55 0xAA {np.random.bytes(4).hex().upper()}`")
            
            time.sleep(0.2)
else:
    st.info("Adjust the FPGA clock parameters in the sidebar and click 'Execute Pipeline' to begin.")
