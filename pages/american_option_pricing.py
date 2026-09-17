import numpy as np
import pandas as pd
import streamlit as st
import black_scholes_app as f
import math_documentation as math_doc
from american_models import ju_zhong_option_price, brenner_galai_option_price

st.set_page_config(page_title="American Option Pricing", layout="wide")
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

st.title("American Option Approximation Models")
model = st.sidebar.radio(
    "Select American Approximation Model:",
    ("Bjerksund-Stensland 1993", "Bjerksund-Stensland 2002", "Ju-Zhong 1999", "Brenner-Galai 1989"),
)
math_doc.american_options(model.split()[-1])

S0 = st.sidebar.number_input("Spot Price", value=100.0, format="%.2f")
K = st.sidebar.number_input("Strike", value=100.0, format="%.2f")
T = st.sidebar.number_input("Time to Maturity", value=1.0, format="%.2f")
r = st.sidebar.number_input("Risk-Free Rate", value=0.05, format="%.4f")
b = st.sidebar.number_input("Cost of Carry / Dividend Yield", value=0.03, format="%.4f")
sigma = st.sidebar.number_input("Volatility", value=0.20, format="%.4f")
option = st.sidebar.radio("Option Type", ("call", "put"))

spots = np.linspace(80.0, 120.0, 25)
prices_1993 = []
prices_2002 = []
prices_ju_zhong = []
prices_brenner_galai = []
for S in spots:
    prices_1993.append(float(f.bs1993_option_price(S, K, T, r, b, sigma, option=option)))
    prices_2002.append(float(f.bs2002_option_price(S, K, T, r, b, sigma, option=option)))
    prices_ju_zhong.append(float(ju_zhong_option_price(S, K, T, r, b, sigma, option=option)))
    prices_brenner_galai.append(float(brenner_galai_option_price(S, K, T, r, b, sigma, option=option)))

frame = pd.DataFrame({
    "Spot": spots,
    "Bjerksund-Stensland 1993": prices_1993,
    "Bjerksund-Stensland 2002": prices_2002,
    "Ju-Zhong 1999": prices_ju_zhong,
    "Brenner-Galai 1989": prices_brenner_galai,
})

series = {
    "Bjerksund-Stensland 1993": "Bjerksund-Stensland 1993",
    "Bjerksund-Stensland 2002": "Bjerksund-Stensland 2002",
    "Ju-Zhong 1999": "Ju-Zhong 1999",
    "Brenner-Galai 1989": "Brenner-Galai 1989",
}
st.subheader(model)
st.line_chart(frame, x="Spot", y=series[model])

st.write(frame)

