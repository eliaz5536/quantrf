import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import streamlit as st
import black_scholes_app as f
import svi

from scipy.interpolate import griddata
from scipy.stats import ncx2

st.set_page_config(page_title="Black-Scholes-Merton (1973)", layout="wide")
st.sidebar.title("Quant Research Framework")
st.sidebar.page_link(page="", label="Monte Carlo")
st.sidebar.page_link(page="main.py", label="Black-Scholes-Merton (1973)")
st.sidebar.page_link(page="pages/black.py", label="Black (1976)")
st.sidebar.page_link(page="pages/binomial_tree.py", label="Binomial Tree")
st.sidebar.page_link(page="pages/trinomial_tree.py", label="Trinomial Tree")
st.sidebar.page_link(page="pages/interest_rate_models.py", label="Interest Rate Models")
st.sidebar.page_link(page="pages/american_option_pricing.py", label="American Option Pricing")
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

program_mode = st.sidebar.radio(
    'Select Program Mode:',
    ('Cox-Ingersoll-Ross', 'Vasicek')
)

if program_mode == "Cox-Ingersoll-Ross":
    st.title("Cox-Ingersoll-Ross")

    # st.markdown("<h1 style='text-align: center;'>Black Scholes Option Pricing</h1>", unsafe_allow_html=True)
    st.sidebar.header('Cox-Ingersoll-Ross Variables')

    kappa = st.sidebar.number_input('Spot Price($)', value=100.00, format="%.2f")
    theta = st.sidebar.number_input('Strike Price($)', value=80.00, format="%.2f")
    sigma = st.sidebar.number_input('Volatility (σ)', value=0.20, format="%.2f")
    time_to_maturity = st.sidebar.number_input('Time to Maturity (in Years, days/365)', value=1.00, format="%.2f")
    r0 = st.sidebar.number_input('Risk-Free Rate', min_value=0.0, max_value=1.0, value=0.03, format="%.4f")
    steps = st.sidebar.number_input('Dividend Yield', min_value=0.0, max_value=1.0, value=0.0, format="%.4f")

    dt = time_to_maturity / steps

    rates = np.zeros(steps+1)
    rates[0] = r0

    for i in range(steps):
        z = np.random.normal()
        dr = (
            kappa * (theta - rates[i]) * dt
            + sigma * np.sqrt(max(rates[i], 0)) * np.sqrt(dt) * z
        )
        rates[i+1] = max(rates[i] + dr,0)
    time = np.linspace(0, time_to_maturity, steps+1)

    plt.figure(figsize=(12,5))

    plt.plot(time ,rates, lw=2)

    plt.xlabel("Time")
    plt.ylabel("Short Rate")
    plt.title("CIR Short Rate Simulation")
    plt.show()

    r = f.CIR(r0, kappa, theta, sigma, time_to_maturity, steps)

    plt.figure(figsize=(12,5))

    plt.plot(time, r)

    plt.title("Exact CIR simulation")
    plt.xlabel("Years")
    plt.ylabel("Rate")
    plt.show()    

    maturity = np.linspace(.25, 30, 120)
    prices = f.CIR_show_bond_prices(maturity, r0, kappa, theta, sigma, tau)

    plt.figure(figize=(10,5))
    plt.plot(maturity, prices)
    plt.xlabel("Maturity")
    plt.ylabel("Bond Prices")
    plt.title("Zero Coupon Bond Prices under CIR")
    plt.show()

    yield_curve = f.CIR_yield_curve(prices, maturity)

    plt.figure(figsize=(10,5))

    plt.plot(maturity, yield_curve,lw=2)

    plt.xlabel("Maturity")
    plt.ylabel("Yield")

    plt.title("Yield Curve from CIR Model")

    plt.show()

elif program_mode == "Vasicek":
    st.title("Vasicek")

    # st.markdown("<h1 style='text-align: center;'>Black Scholes Option Pricing</h1>", unsafe_allow_html=True)
    st.sidebar.header('Vasicek Variables')

    # Distribution at Final Time
    plt.figure(figsize=(8,5))
    # plt.hist(rates[-1], bins=30, density=True)
    plt.xlabel("Interest Rate")
    plt.ylabel("Density")
    plt.title("Distribution of $r(T)$")
    plt.show()