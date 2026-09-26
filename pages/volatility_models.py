import numpy as np
import pandas as pd
import streamlit as st
import black_scholes_app as f

st.set_page_config(page_title="Volatility Models", layout="wide", page_icon="quantrf_logo_website.png")
st.sidebar.image("images/sidebar_logo.png")
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
st.sidebar.page_link(page="pages/cfa_curriculum.py", label="Rates and Returns")
st.sidebar.page_link(page="pages/time_value_of_money.py", label="Time Value of Money")
st.sidebar.page_link(page="pages/types_of_financial_return.py", label="Types of Financial Return")
st.sidebar.page_link(page="pages/portfolio_risk_return.py", label="Portfolio Risk and Return")
st.sidebar.page_link(page="pages/fixed_income_yield_spreads.py", label="Fixed Income Yield Spreads")
st.sidebar.page_link(page="pages/market_organization_structure.py", label="Market Organization and Structure")
st.sidebar.page_link(page="pages/security_market_indexes.py", label="Security Market Indexes")
st.sidebar.page_link(page="pages/forward_commitment_contingent_claims.py", label="Forward Commitments and Contingent Claims")
st.sidebar.page_link(page="pages/option_replication_put_call_parity.py", label="Option Replication Using Put-Call Parity")
st.sidebar.page_link(page="pages/capital_structure.py", label="Capital Structure")
st.sidebar.page_link(page="pages/alternative_investments.py", label="Alternative Investments")
st.sidebar.page_link(page="pages/alternative_investment_performance.py", label="Alternative Investment Performance")
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

st.title("GARCH(1,1) Volatility Model")
st.markdown("GARCH models allow volatility to cluster: large shocks tend to be followed by large shocks, and calm periods tend to persist.")

sample_size = st.sidebar.slider("Synthetic Return Observations", 100, 3000, 750, 50)
horizon = st.sidebar.slider("Forecast Horizon", 1, 30, 10)
rng = np.random.default_rng(7)
returns = rng.normal(0.0002, 0.012, sample_size)
fit = f.fit_garch11(returns)
forecast = f.forecast_garch11(fit, horizon)

st.latex(r"h_t=\omega+\alpha\epsilon_{t-1}^2+\beta h_{t-1}")
st.latex(r"\alpha+\beta<1\quad\Rightarrow\quad\text{finite long-run variance}")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Omega", f"{fit['omega']:.6g}")
col2.metric("Alpha", f"{fit['alpha']:.4f}")
col3.metric("Beta", f"{fit['beta']:.4f}")
col4.metric("Persistence", f"{fit['alpha'] + fit['beta']:.4f}")

conditional = pd.DataFrame({"Conditional Volatility": fit["conditional_volatility"]})
st.subheader("Estimated Conditional Volatility")
st.line_chart(conditional)
forecast_frame = pd.DataFrame({"Forecast Volatility": np.sqrt(forecast)}, index=np.arange(1, horizon + 1))
forecast_frame.index.name = "Forecast Step"
st.subheader("Volatility Forecast")
st.line_chart(forecast_frame)
st.caption("Alpha measures the immediate response to a return shock. Beta measures volatility persistence. A persistence value near one implies slow mean reversion of volatility.")
