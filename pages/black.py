import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

if __package__ in {None, ""}:
    from black_scholes_app import (
        black76_price_from_spot,
        black76_price_from_forward,
        black76_implied_vol_from_spot,
        load_price_history,
        build_market_inputs,
    )
else:
    from ..black_scholes_app import (
        black76_price_from_spot,
        black76_price_from_forward,
        black76_implied_vol_from_spot,
        load_price_history,
        build_market_inputs,
    )

st.set_page_config(page_title="Black (1976)", layout="wide")
st.sidebar.title("Quant Research")
st.sidebar.page_link(page="main.py", label="Black-Scholes-Merton (1973)")
st.sidebar.page_link(page="pages/black.py", label="Black (1976)")

st.title("Black (1976) Pricer")
st.caption("Forward-based option pricing (Black 1976) with heatmaps and implied volatility.)")

with st.sidebar:
    ticker = st.text_input("Ticker", value="ES=F")
    price_history = load_price_history(ticker)
    market_inputs = build_market_inputs(price_history, ticker)
    spot = st.number_input("Spot", value=float(market_inputs.get("spot", 100.0)), min_value=0.01, step=1.0)
    strike = st.number_input("Strike", value=float(market_inputs.get("strike", spot)), min_value=0.01, step=1.0)
    expiry = st.number_input("Time to expiry (years)", value=float(market_inputs.get("expiry", 0.25)), min_value=0.01, step=0.01)
    rate = st.number_input("Risk-free rate", value=float(market_inputs.get("rate", 0.01)), step=0.001)
    sigma = st.number_input("Volatility", value=float(market_inputs.get("volatility", 0.2)), min_value=0.001, step=0.001)
    option_type = st.selectbox("Option type", ["call", "put"])

F = spot * np.exp(rate * expiry)
df = np.exp(-rate * expiry)

price = black76_price_from_forward(F, strike, expiry, sigma, df=df, option=option_type)
implied = None
try:
    implied = black76_implied_vol_from_spot(price, spot, strike, expiry, rate, option=option_type)
except Exception:
    implied = np.nan

col1, col2, col3 = st.columns(3)
col1.metric("Forward (F)", f"{F:.2f}")
col2.metric("Discount factor", f"{df:.4f}")
col3.metric("Black price", f"{price:.2f}")

st.subheader("Heatmap (Black prices)")
spot_grid = np.linspace(max(1.0, spot * 0.7), spot * 1.3, 20)
vol_grid = np.linspace(0.01, 1.0, 20)
spot_mesh, vol_mesh = np.meshgrid(spot_grid, vol_grid, indexing="ij")
F_mesh = spot_mesh * np.exp(rate * expiry)
call_surface = black76_price_from_forward(F_mesh, strike, expiry, vol_mesh, df=np.exp(-rate * expiry), option="call")
heat_df = pd.DataFrame(call_surface, index=np.round(vol_grid, 3), columns=np.round(spot_grid, 2))
heat_df.index.name = "volatility"
heat_df.columns.name = "spot"
fig = px.imshow(heat_df.T, labels=dict(x="Volatility", y="Spot", color="Call price"), color_continuous_scale="Viridis", text_auto='.2f', origin='lower')
fig.update_traces(zmin=0, zmax=75)
fig.update_layout(height=700)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Implied volatility (Black76)")
if np.isfinite(implied):
    st.success(f"Implied vol (Black76) = {implied:.2%}")
else:
    st.info("Couldn't compute implied vol for the current inputs.")