import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="FPGA HFT Pro", layout="wide")

# Sidebar Menu
st.sidebar.title("🎛️ Control Plane")
app_mode = st.sidebar.selectbox("Choose Dashboard", ["Market Overview", "Hardware Diagnostics"])

if app_mode == "Hardware Diagnostics":
    st.header("🛠️ FPGA RTL & Signal Integrity")
    
    col_a, col_b = st.columns()
    
    with col_a:
        st.write("### Resource Utilization")
        st.progress(0.45, text="LUTs (45%)")
        st.progress(0.12, text="BRAM (12%)")
        st.progress(0.88, text="DSP Slices (88%)")
        st.caption("Critical Alert: High DSP usage for Strategy Logic")

    with col_b:
        st.write("### Signal Oscilloscope")
        # Generate a fake clock/signal wave
        chart_data = pd.DataFrame(
            np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.05, 100),
            columns=['GTX Transceiver Signal']
        )
        st.line_chart(chart_data, height=200)

    st.markdown("---")
    st.write("### Live Gate-Level Simulation")
    
    # Logic Gate Animation Loop
    grid_placeholder = st.empty()
    
    if st.button("Start Signal Trace"):
        for _ in range(20):
            with grid_placeholder.container():
                cols = st.columns(10)
                for i in range(10):
                    active = np.random.rand() > 0.5
                    color = "#00FF00" if active else "#1A1A1A"
                    glow = "box-shadow: 0 0 10px #00FF00;" if active else ""
                    cols[i].markdown(f"""
                        <div style="height:30px; background-color:{color}; {glow} border:1px solid #444;"></div>
                    """, unsafe_allow_html=True)
                time.sleep(0.1)
