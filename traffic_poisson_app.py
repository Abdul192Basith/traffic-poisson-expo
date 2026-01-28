import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Traffic Simulation", layout="wide")

st.title("Virtual Traffic Signal Control using Poisson Distribution")

st.write("""
Each lane arrival is modeled as a **Poisson random variable**.
The lane with the highest observed arrivals gets the **green signal**.
""")

# ---------- Sidebar: Lambda Inputs ----------
st.sidebar.header("Arrival Rates (λ per minute)")

lambdas = {}

for j in range(1, 5):
    st.sidebar.subheader(f"Junction {j}")
    for i in range(1, 5):
        lambdas[(j, i)] = st.sidebar.slider(
            f"J{j} Lane {i} λ",
            min_value=0,
            max_value=25,
            value=10,
            key=f"j{j}l{i}"
        )

simulate = st.sidebar.button("Simulate Traffic")

# ---------- Simulation ----------
def simulate_junction(j):
    lam = [lambdas[(j, i)] for i in range(1, 5)]
    arrivals = np.random.poisson(lam)

    ranks = arrivals.argsort()[::-1]
    signals = ["RED"] * 4
    signals[ranks[0]] = "GREEN"
    signals[ranks[1]] = "YELLOW"

    return pd.DataFrame({
        "Lane": [f"Lane {i}" for i in range(1, 5)],
        "Lambda": lam,
        "Vehicles": arrivals,
        "Signal": signals
    })

# ---------- Display ----------
if simulate:
    cols = st.columns(4)

    for j in range(1, 5):
        with cols[j-1]:
            st.subheader(f"Junction {j}")
            df = simulate_junction(j)

            st.dataframe(df, use_container_width=True)

            for _, row in df.iterrows():
                color = {
                    "GREEN": "🟢",
                    "YELLOW": "🟡",
                    "RED": "🔴"
                }[row["Signal"]]

                st.markdown(f"**{row['Lane']}** : {color} {row['Signal']}")

else:
    st.info("Adjust λ values and click **Simulate Traffic**")

