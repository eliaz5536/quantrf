import numpy as np
import pandas as pd
import streamlit as st
from risk_models import historical_cvar, historical_var, parametric_cvar, parametric_var

st.set_page_config(page_title="Risk Management", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Value at Risk and Conditional Value at Risk")
method = st.sidebar.radio("Risk Measure", ("Historical", "Parametric Normal"))
confidence = st.sidebar.slider("Confidence Level", 0.90, 0.99, 0.95, 0.01)
portfolio_value = st.sidebar.number_input("Portfolio Value", min_value=0.0, value=100000.0, step=1000.0)

rng = np.random.default_rng(42)
returns = rng.normal(0.0003, 0.012, 1000)
if method == "Historical":
    var = historical_var(returns, confidence, portfolio_value)
    cvar = historical_cvar(returns, confidence, portfolio_value)
else:
    mean_return = float(returns.mean())
    volatility = float(returns.std(ddof=1))
    var = parametric_var(mean_return, volatility, confidence, portfolio_value)
    cvar = parametric_cvar(mean_return, volatility, confidence, portfolio_value)

st.latex(r"VaR_\alpha=\inf\{\ell:P(L\leq\ell)\geq\alpha\}")
st.latex(r"CVaR_\alpha=E[L\mid L\geq VaR_\alpha]")
col1, col2 = st.columns(2)
col1.metric(f"VaR ({confidence:.0%})", f"${var:,.2f}")
col2.metric(f"CVaR ({confidence:.0%})", f"${cvar:,.2f}")

losses = -portfolio_value * returns
hist, edges = np.histogram(losses, bins=40)
frame = pd.DataFrame({"Frequency": hist}, index=[f"{edges[i]:.0f} to {edges[i + 1]:.0f}" for i in range(len(hist))])
st.subheader("Simulated Loss Distribution")
st.bar_chart(frame)
st.caption("VaR is the loss quantile at the selected confidence. CVaR averages the losses in the tail beyond that quantile and is therefore more sensitive to extreme outcomes.")
