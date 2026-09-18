import numpy as np
import pandas as pd
import streamlit as st
import black_scholes_app as f
import math_documentation as math_doc

st.set_page_config(page_title="Interest Rate Models", layout="wide", page_icon="quantrf_logo_website.png")
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

program_mode = st.sidebar.radio("Select Program Mode:", ("Cox-Ingersoll-Ross", "Vasicek"))

st.title("Interest Rate Models")
if program_mode == "Cox-Ingersoll-Ross":
    st.subheader("Cox-Ingersoll-Ross")
    math_doc.interest_rates("cir")
    st.sidebar.header("Cox-Ingersoll-Ross Variables")

    kappa = st.sidebar.number_input("Mean Reversion Speed κ", value=0.80, format="%.4f")
    theta = st.sidebar.number_input("Long-Run Mean θ", value=0.04, format="%.4f")
    sigma = st.sidebar.number_input("Volatility σ", value=0.02, format="%.4f")
    time_to_maturity = st.sidebar.number_input("Time to Maturity (Years)", value=1.00, format="%.2f")
    r0 = st.sidebar.number_input("Initial Short Rate r0", value=0.03, format="%.4f")
    steps = st.sidebar.number_input("Time Steps", min_value=1, value=10, format="%d")

    time, rates = f.cir_short_rate_path(r0, kappa, theta, sigma, time_to_maturity, steps)
    maturity = np.linspace(0.25, 30.0, 120)
    bond_prices = f.cir_show_bond_prices(maturity, r0, kappa, theta, sigma)
    yields = f.cir_yield_curve(bond_prices, maturity)

    st.line_chart(pd.DataFrame({"Short Rate": rates}), use_container_width=True)
    st.line_chart(pd.DataFrame({"Bond Price": bond_prices, "Maturity": maturity}), x="Maturity", y="Bond Price", use_container_width=True)
    st.line_chart(pd.DataFrame({"Yield": yields, "Maturity": maturity}), x="Maturity", y="Yield", use_container_width=True)

elif program_mode == "Vasicek":
    st.subheader("Vasicek")
    math_doc.interest_rates("vasicek")
    st.sidebar.header("Vasicek Variables")

    kappa = st.sidebar.number_input("Mean Reversion Speed κ", value=0.80, format="%.4f")
    theta = st.sidebar.number_input("Long-Run Mean θ", value=0.04, format="%.4f")
    sigma = st.sidebar.number_input("Volatility σ", value=0.02, format="%.4f")
    time_to_maturity = st.sidebar.number_input("Time to Maturity (Years)", value=1.00, format="%.2f")
    r0 = st.sidebar.number_input("Initial Short Rate r0", value=0.03, format="%.4f")
    steps = st.sidebar.number_input("Time Steps", min_value=1, value=10, format="%d")

    time, rates = f.vasicek_short_rate_path(r0, kappa, theta, sigma, time_to_maturity, steps)
    maturity = np.linspace(0.25, 30.0, 120)
    bond_prices = f.vasicek_show_bond_prices(maturity, r0, kappa, theta, sigma)
    yields = f.vasicek_yield_curve(bond_prices, maturity)

    st.line_chart(pd.DataFrame({"Short Rate": rates}), use_container_width=True)
    st.line_chart(pd.DataFrame({"Bond Price": bond_prices, "Maturity": maturity}), x="Maturity", y="Bond Price", use_container_width=True)
    st.line_chart(pd.DataFrame({"Yield": yields, "Maturity": maturity}), x="Maturity", y="Yield", use_container_width=True)