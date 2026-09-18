import numpy as np
import pandas as pd
import streamlit as st
import black_scholes_app as f
from credit_models import (
    merton_equity_value,
    merton_debt_value,
    distance_to_default,
    probability_of_default,
    solve_asset_value,
)

st.set_page_config(page_title="Credit Risk", layout="wide", page_icon="quantrf_logo_website.png")
st.sidebar.title("Quant Research Framework")
st.sidebar.page_link(page="pages/monte_carlo.py", label="Monte Carlo")
st.sidebar.page_link(page="main.py", label="Black-Scholes-Merton (1973)")
st.sidebar.page_link(page="pages/black.py", label="Black (1976)", disabled=True)
st.sidebar.page_link(page="pages/binomial_tree.py", label="Binomial Tree")
st.sidebar.page_link(page="pages/trinomial_tree.py", label="Trinomial Tree", disabled=True)
st.sidebar.page_link(page="pages/interest_rate_models.py", label="Interest Rate Models")
st.sidebar.page_link(page="pages/american_option_pricing.py", label="American Option Pricing")
st.sidebar.page_link(page="pages/credit_risk.py", label="Credit Risk")
st.sidebar.page_link(page="pages/risk_management.py", label="Risk Management")
st.sidebar.page_link(page="pages/volatility_models.py", label="Volatility Models")
st.sidebar.page_link(page="pages/references.py", label="References")
st.sidebar.markdown(
    """
    <div style='margin-bottom: 25px;'>
        <!-- <span style='font-weight: bold; font-size: 18px;'>Created by:</span><br> -->
        <a href='https://www.linkedin.com/in/eliaz-simon/' target='_blank' style='text-decoration: none; display: flex; align-items: center; gap: 12px; margin-top: 8px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='32' height='32'/>
            <span style='color: #0A66C2; font-size: 18px; font-weight: bold;'>Eliaz Simon</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("KMV-Merton Structural Credit Risk")
st.markdown("Equity is treated as a call option on the firm's assets. Default occurs when asset value is below the debt face value at maturity.")

asset_value = st.sidebar.number_input("Firm Asset Value", min_value=0.01, value=150.0)
equity_value = st.sidebar.number_input("Observed Equity Value", min_value=0.01, value=100.0)
debt_face = st.sidebar.number_input("Debt Face Value", min_value=0.01, value=100.0)
maturity = st.sidebar.number_input("Debt Maturity (Years)", min_value=0.01, value=1.0)
rate = st.sidebar.number_input("Risk-Free Rate", value=0.05, format="%.4f")
asset_volatility = st.sidebar.number_input("Asset Volatility", min_value=0.001, value=0.25, format="%.4f")

st.latex(r"E=A\Phi(d_1)-De^{-rT}\Phi(d_2),\qquad d_2=d_1-\sigma_A\sqrt{T}")
st.latex(r"DD=\frac{\ln(A/D)+(r-\frac12\sigma_A^2)T}{\sigma_A\sqrt{T}},\qquad PD=\Phi(-DD)")

model_equity = merton_equity_value(asset_value, debt_face, maturity, rate, asset_volatility)
debt_value = merton_debt_value(asset_value, debt_face, maturity, rate, asset_volatility)
dd = distance_to_default(asset_value, debt_face, maturity, rate, asset_volatility)
default_probability = probability_of_default(asset_value, debt_face, maturity, rate, asset_volatility)
try:
    inferred_assets = solve_asset_value(equity_value, debt_face, maturity, rate, asset_volatility)
except ValueError:
    inferred_assets = np.nan

col1, col2, col3, col4 = st.columns(4)
col1.metric("Model Equity Value", f"{model_equity:,.2f}")
col2.metric("Risky Debt Value", f"{debt_value:,.2f}")
col3.metric("Distance to Default", f"{dd:.3f}")
col4.metric("Probability of Default", f"{default_probability:.2%}")

st.subheader("Balance Sheet Interpretation")
frame = pd.DataFrame({"Value": [asset_value, model_equity, debt_value, debt_face, inferred_assets]}, index=["Assets", "Equity", "Risky Debt", "Debt Face", "Inferred Assets"])
st.bar_chart(frame)
st.caption("Distance to default is measured in asset-volatility units. The probability shown is risk-neutral; KMV commonly replaces it with an empirically calibrated expected default frequency.")
