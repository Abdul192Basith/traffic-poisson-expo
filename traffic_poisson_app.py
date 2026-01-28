import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("3D Traffic Junction (Poisson Model)")

lambdas = [
    st.slider("Lane 1 λ", 0, 25, 10),
    st.slider("Lane 2 λ", 0, 25, 10),
    st.slider("Lane 3 λ", 0, 25, 10),
    st.slider("Lane 4 λ", 0, 25, 10)
]

if st.button("Simulate"):
    arrivals = np.random.poisson(lambdas)

    fig = go.Figure()

    # Roads
    fig.add_surface(
        x=[[-5, 5], [-5, 5]],
        y=[[0, 0], [0, 0]],
        z=[[0, 0], [0, 0]],
        colorscale="gray",
        showscale=False
    )

    fig.add_surface(
        x=[[0, 0], [0, 0]],
        y=[[-5, 5], [-5, 5]],
        z=[[0, 0], [0, 0]],
        colorscale="gray",
        showscale=False
    )

    # Cars (as 3D points)
    for i, n in enumerate(arrivals):
        fig.add_trace(go.Scatter3d(
            x=np.random.uniform(-4, 4, n),
            y=np.random.uniform(-4, 4, n),
            z=np.zeros(n),
            mode='markers',
            marker=dict(size=4),
            name=f"Lane {i+1}"
        ))

    fig.update_layout(
        scene=dict(
            camera=dict(eye=dict(x=1.5, y=1.5, z=1)),
            xaxis_visible=False,
            yaxis_visible=False,
            zaxis_visible=False
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
