import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import streamlit as st
import black_scholes_app as f
import svi
import math_documentation as math_doc

from scipy.interpolate import griddata

st.set_page_config(page_title="Trinomial Tree", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Trinomial Tree Model")
math_doc.trinomial()
st.info("The trinomial pricing implementation is not yet connected to this page.")
