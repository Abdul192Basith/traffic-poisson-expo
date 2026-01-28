import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("3D Traffic Junction Simulation (Poisson Model)")

st.markdown(
    """
Each lane arrival follows a **Poisson distribution**.
Cars move toward the junction, and signals adapt dynamically.
"""
)

# ---------- Sidebar ----------
st.sidebar.header("Arrival Rates (λ per minute)")

lambdas = [
    st.sidebar.slider("Lane 1 (North) λ", 0, 25, 10),
    st.sidebar.slider("Lane 2 (East) λ", 0, 25, 10),
    st.sidebar.slider("Lane 3 (South) λ", 0, 25, 10),
    st.sidebar.slider("Lane 4 (West) λ", 0, 25, 10),
]

animate = st.sidebar.button("Simulate & Animate")

# ---------- Simulation ----------
if animate:

    arrivals = np.random.poisson(lambdas)

    order = arrivals.argsort()[::-1]
    signals = ["RED"] * 4
    signals[order[0]] = "GREEN"
    signals[order[1]] = "YELLOW"

    signal_colors = {
        "GREEN": "green",
        "YELLOW": "yellow",
        "RED": "red"
    }

    fig = go.Figure()

    # ---------- Roads ----------
    fig.add_surface(
        x=[[-6, 6], [-6, 6]],
        y=[[0, 0], [0, 0]],
        z=[[0, 0], [0, 0]],
        colorscale=[[0, "#444"], [1, "#444"]],
        showscale=False
    )

    fig.add_surface(
        x=[[0, 0], [0, 0]],
        y=[[-6, 6], [-6, 6]],
        z=[[0, 0], [0, 0]],
        colorscale=[[0, "#444"], [1, "#444"]],
        showscale=False
    )

# ---------- Buildings (Town Background) ----------
def building(x, y, w=1.5, d=1.5, h=3):
    return go.Mesh3d(
        x=[x, x+w, x+w, x, x, x+w, x+w, x],
        y=[y, y, y+d, y+d, y, y, y+d, y+d],
        z=[0, 0, 0, 0, h, h, h, h],
        color="gray",
        opacity=0.6
    )

for bx, by in [(-5, -5), (5, -5), (-5, 5), (5, 5)]:
    fig.add_trace(building(bx, by))

    # ---------- Traffic Light Poles ----------
    pole_positions = [(0, 1.8), (1.8, 0), (0, -1.8), (-1.8, 0)]

    for i, (px, py) in enumerate(pole_positions):
        fig.add_scatter3d(
            x=[px], y=[py], z=[1.5],
            mode="markers",
            marker=dict(
                size=10,
                color=signal_colors[signals[i]]
            ),
            name=f"Lane {i+1} Signal"
        )

    # ---------- Animated Cars ----------
    frames = []
    steps = 12

    for t in range(steps):
        cars = []

        # Lane 1 (North → South)
        cars.append(go.Scatter3d(
            x=np.zeros(arrivals[0]),
            y=np.linspace(5, 0.5, arrivals[0]) - t * 0.3,
            z=np.zeros(arrivals[0]),
            mode="markers",
            marker=dict(size=4, color="blue")
        ))

        # Lane 2 (East → West)
        cars.append(go.Scatter3d(
            x=np.linspace(5, 0.5, arrivals[1]) - t * 0.3,
            y=np.zeros(arrivals[1]),
            z=np.zeros(arrivals[1]),
            mode="markers",
            marker=dict(size=4, color="orange")
        ))

        # Lane 3 (South → North)
        cars.append(go.Scatter3d(
            x=np.zeros(arrivals[2]),
            y=np.linspace(-5, -0.5, arrivals[2]) + t * 0.3,
            z=np.zeros(arrivals[2]),
            mode="markers",
            marker=dict(size=4, color="purple")
        ))

        # Lane 4 (West → East)
        cars.append(go.Scatter3d(
            x=np.linspace(-5, -0.5, arrivals[3]) + t * 0.3,
            y=np.zeros(arrivals[3]),
            z=np.zeros(arrivals[3]),
            mode="markers",
            marker=dict(size=4, color="cyan")
        ))

        frames.append(go.Frame(data=cars, name=str(t)))

    fig.frames = frames

    fig.update_layout(
        scene=dict(
            xaxis_visible=False,
            yaxis_visible=False,
            zaxis_visible=False,
            camera=dict(eye=dict(x=1.6, y=1.6, z=1))
        ),
        height=700,
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(
                        label="▶ Play",
                        method="animate",
                        args=[None, {"frame": {"duration": 200, "redraw": True}}]
                    )
                ]
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success(
        f"Signals → Lane {order[0]+1}: GREEN, Lane {order[1]+1}: YELLOW"
    )

else:
    st.info("Set λ values and click **Simulate & Animate**")
