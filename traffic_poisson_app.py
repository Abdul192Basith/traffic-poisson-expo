import streamlit as st
import numpy as np

st.set_page_config(layout="centered")
st.title("Visual Traffic Junction (Poisson Model)")

st.write(
    "Vehicle arrivals on each lane follow a **Poisson distribution**. "
    "The busiest lane receives the **green signal**."
)

# ---------- Inputs ----------
st.sidebar.header("Arrival Rates (λ per minute)")

lambdas = [
    st.sidebar.slider("Lane 1 λ", 0, 25, 10),
    st.sidebar.slider("Lane 2 λ", 0, 25, 10),
    st.sidebar.slider("Lane 3 λ", 0, 25, 10),
    st.sidebar.slider("Lane 4 λ", 0, 25, 10),
]

if st.sidebar.button("Simulate"):

    arrivals = np.random.poisson(lambdas)

    # Rank lanes
    order = arrivals.argsort()[::-1]
    signals = ["🔴"] * 4
    signals[order[0]] = "🟢"
    signals[order[1]] = "🟡"

    st.markdown("## 🚦 Junction View")

    # ---------- Visual Layout ----------
    col_top = st.columns([1, 2, 1])
    col_mid = st.columns([1, 2, 1])
    col_bot = st.columns([1, 2, 1])

    # Lane 1 (Top)
    with col_top[1]:
        st.markdown(f"### Lane 1 {signals[0]}")
        st.write("🚗" * min(arrivals[0], 10))
        st.caption(f"Vehicles: {arrivals[0]}")

    # Lane 4 (Left)
    with col_mid[0]:
        st.markdown(f"### Lane 4 {signals[3]}")
        st.write("🚗" * min(arrivals[3], 10))
        st.caption(f"Vehicles: {arrivals[3]}")

    # Center
    with col_mid[1]:
        st.markdown("## ⛔ Junction")

    # Lane 2 (Right)
    with col_mid[2]:
        st.markdown(f"### Lane 2 {signals[1]}")
        st.write("🚗" * min(arrivals[1], 10))
        st.caption(f"Vehicles: {arrivals[1]}")

    # Lane 3 (Bottom)
    with col_bot[1]:
        st.markdown(f"### Lane 3 {signals[2]}")
        st.write("🚗" * min(arrivals[2], 10))
        st.caption(f"Vehicles: {arrivals[2]}")

else:
    st.info("Set λ values and click **Simulate**")
