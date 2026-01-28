import streamlit as st
import numpy as np

st.set_page_config(layout="centered")
st.title("🚦 Traffic Junction – Top View (India: Left-Hand Drive)")

st.write(
    "Vehicle arrivals on each lane follow a **Poisson distribution**. "
    "Vehicles queue on the **left side of the road** (Indian traffic rule). "
    "The busiest lane receives the **green signal**."
)

# ---------------- Sidebar ----------------
st.sidebar.header("Arrival Rates (λ per minute)")

lambdas = [
    st.sidebar.slider("Lane 1 (East → Center)", 0, 25, 10),
    st.sidebar.slider("Lane 2 (South → Center)", 0, 25, 10),
    st.sidebar.slider("Lane 3 (West → Center)", 0, 25, 10),
    st.sidebar.slider("Lane 4 (North → Center)", 0, 25, 10),
]

if st.sidebar.button("Simulate"):

    arrivals = np.random.poisson(lambdas)

    # Signal logic
    order = arrivals.argsort()[::-1]
    signals = ["🔴"] * 4
    signals[order[0]] = "🟢"
    signals[order[1]] = "🟡"

    st.markdown("## 🛣️ Junction View (Top View – Left-Hand Drive)")

    # ---------------- Layout Grid ----------------
    col_top = st.columns([1, 3, 1])
    col_mid = st.columns([3, 2, 3])
    col_bot = st.columns([1, 3, 1])

    # ---------- Lane 4 (North → Center) ----------
    with col_top[1]:
        st.markdown(f"### 🚦 Lane 4 {signals[3]}")
        for _ in range(min(arrivals[3], 8)):
            st.markdown("🚗")
        st.caption(f"Vehicles: {arrivals[3]}")

    # ---------- Lane 3 (West → Center) ----------
    with col_mid[0]:
        st.markdown(f"### 🚦 Lane 3 {signals[2]}")
        st.markdown("🚗 " * min(arrivals[2], 12))
        st.caption(f"Vehicles: {arrivals[2]}")

    # ---------- Junction ----------
    with col_mid[1]:
        st.markdown("## ⛔ JUNCTION")
        st.markdown("⬅️⬆️⬇️➡️")
        st.markdown("**Vehicles keep LEFT**")

    # ---------- Lane 1 (East → Center) ----------
    with col_mid[2]:
        st.markdown(f"### 🚦 Lane 1 {signals[0]}")
        st.markdown("🚗 " * min(arrivals[0], 12))
        st.caption(f"Vehicles: {arrivals[0]}")

    # ---------- Lane 2 (South → Center) ----------
    with col_bot[1]:
        st.markdown(f"### 🚦 Lane 2 {signals[1]}")
        for _ in range(min(arrivals[1], 8)):
            st.markdown("🚗")
        st.caption(f"Vehicles: {arrivals[1]}")

    # ---------------- Explanation ----------------
    st.markdown("---")
    st.markdown(
        f"""
### 🚦 Signal Decision Logic
- 🟢 **Green** → Lane {order[0] + 1} (highest arrivals)
- 🟡 **Yellow** → Lane {order[1] + 1}
- 🔴 **Red** → Other lanes

Vehicles are queued on the **left side of each road**,  
which matches **Indian left-hand traffic rules**.
"""
    )

else:
    st.info("Set λ values and click **Simulate**")
