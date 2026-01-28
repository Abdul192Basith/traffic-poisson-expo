import streamlit as st
import numpy as np

st.set_page_config(layout="centered")
st.title("🚦 Traffic Junction – Top View (Poisson Model)")

st.write(
    "Vehicle arrivals on each lane follow a **Poisson distribution**. "
    "The lane with the highest arrivals receives the **green signal**."
)

# ---------------- Sidebar ----------------
st.sidebar.header("Arrival Rates (λ per minute)")

lambdas = [
    st.sidebar.slider("Lane 1 (East → West)", 0, 25, 10),
    st.sidebar.slider("Lane 2 (South → North)", 0, 25, 10),
    st.sidebar.slider("Lane 3 (West → East)", 0, 25, 10),
    st.sidebar.slider("Lane 4 (North → South)", 0, 25, 10),
]

if st.sidebar.button("Simulate"):

    arrivals = np.random.poisson(lambdas)

    # Signal logic
    order = arrivals.argsort()[::-1]
    signals = ["🔴"] * 4
    signals[order[0]] = "🟢"
    signals[order[1]] = "🟡"

    st.markdown("## 🚧 Junction View (Top View)")

    # ---------------- Layout Grid ----------------
    col_top = st.columns([1, 2, 1])
    col_mid = st.columns([1, 2, 1])
    col_bot = st.columns([1, 2, 1])

    # -------- Lane 4 (North → South) --------
    with col_top[1]:
        st.markdown(f"### Lane 4 {signals[3]}")
        st.markdown("🚗 " * min(arrivals[3], 12))
        st.caption(f"Vehicles: {arrivals[3]}")

    # -------- Lane 3 (West → East) --------
    with col_mid[0]:
        st.markdown(f"### Lane 3 {signals[2]}")
        st.markdown("🚗 " * min(arrivals[2], 12))
        st.caption(f"Vehicles: {arrivals[2]}")

    # -------- Junction Center --------
    with col_mid[1]:
        st.markdown("## ⛔ JUNCTION")
        st.markdown("⬆️⬇️  ⬅️➡️")

    # -------- Lane 1 (East → West) --------
    with col_mid[2]:
        st.markdown(f"### Lane 1 {signals[0]}")
        st.markdown("🚗 " * min(arrivals[0], 12))
        st.caption(f"Vehicles: {arrivals[0]}")

    # -------- Lane 2 (South → North) --------
    with col_bot[1]:
        st.markdown(f"### Lane 2 {signals[1]}")
        st.markdown("🚗 " * min(arrivals[1], 12))
        st.caption(f"Vehicles: {arrivals[1]}")

    # ---------------- Explanation ----------------
    st.markdown("---")
    st.markdown(
        f"""
**Signal Decision:**  
- 🟢 Green → Lane {order[0]+1}  
- 🟡 Yellow → Lane {order[1]+1}  
- 🔴 Red → Remaining lanes  

Each signal is positioned **before the junction**, facing incoming vehicles,
exactly as in a real road intersection.
"""
    )

else:
