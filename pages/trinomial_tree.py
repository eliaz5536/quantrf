import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import streamlit as st
import black_scholes_app as f
import svi

from scipy.interpolate import griddata

st.set_page_config(page_title="Black (1976)", layout="wide")
st.sidebar.title("Quant Research Framework")
st.sidebar.page_link(page="main.py", label="Black-Scholes-Merton (1973)")
st.sidebar.page_link(page="pages/black.py", label="Black (1976)")
st.sidebar.page_link(page="pages/binomial_tree.py", label="Binomial Tree")
st.sidebar.page_link(page="pages/trinomial_tree.py", label="Trinomial Tree")
st.sidebar.page_link(page="pages/interest_rate_models.py", label="Interest Rate Models")
st.sidebar.page_link(page="pages/american_option_pricing.py", label="American Option Pricing")

st.sidebar.markdown(
    """
    <div style='margin-bottom: 25px;'>
        <a href='https://www.linkedin.com/in/eliaz-simon/' target='_blank' style='text-decoration: none; display: flex; align-items: center; gap: 12px; margin-top: 8px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='32' height='32'/>
            <span style='color: #0A66C2; font-size: 18px; font-weight: bold;'>Eliaz Simon</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
