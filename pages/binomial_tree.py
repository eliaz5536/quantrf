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

def plot_model_sensitivity_curve(model_name, call_solver, put_solver, S0, K, T, r, sigma, N):
    """Render a reusable Streamlit line-chart sensitivity surface for a public price solver.

    The helper compares call and put surfaces across a narrow spot-price grid,
    keeping the same model branch wiring across selected public app functions.
    """
    spot_grid = np.linspace(max(S0 * 0.75, 1.0), S0 * 1.25, 60)
    call_curve = np.array([
        call_solver(s, K, T, r, sigma, N, option='call')
        for s in spot_grid
    ])
    put_curve = np.array([
        put_solver(s, K, T, r, sigma, N, option='put')
        for s in spot_grid
    ])

    curve_df = pd.DataFrame({
        'Spot Price': spot_grid,
        'Call Price': call_curve,
        'Put Price': put_curve,
    })

    st.subheader(f'{model_name} Model Sensitivity Curve')
    st.line_chart(curve_df.set_index('Spot Price'))


st.set_page_config(page_title="Black (1976)", layout="wide")
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
        <a href='https://www.linkedin.com/in/eliaz-simon/' target='_blank' style='text-decoration: none; display: flex; align-items: center; gap: 12px; margin-top: 8px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='32' height='32'/>
            <span style='color: #0A66C2; font-size: 18px; font-weight: bold;'>Eliaz Simon</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

program_mode = st.sidebar.radio(
    'Select Model:',
    ('Cox-Ross-Rubinstein', 'Figlewski', 'Jarrow-Rudd', 'Leisen-Reimer', 'Tian', 'Hull-White')
)

if program_mode == 'Cox-Ross-Rubinstein':
    st.title("Cox-Ross-Rubinstein (1979) Binomial Tree Model")

    # Input parameters
    S0 = st.sidebar.number_input('Initial Stock Price (S0)', min_value=0.0, value=100.0)
    K = st.sidebar.number_input('Strike Price (K)', min_value=0.0, value=100.0)
    T = st.sidebar.number_input('Time to Maturity (T) in years', min_value=0.01, value=1.0)
    r = st.sidebar.number_input('Risk-Free Rate (r)', min_value=0.0, max_value=1.0, value=0.05, format="%.4f")
    sigma = st.sidebar.number_input('Volatility (σ)', min_value=0.0, max_value=1.0, value=0.2, format="%.4f")
    N = st.sidebar.number_input('Number of Steps (N)', min_value=1, value=100)

    # Calculate option prices and trees using the CRR model
    call_price, put_price, stock, call_tree, put_tree = f.crr_option_price(S0, K, T, r, sigma, N)

    # Plot stock price tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, stock[i, j], s=60)
            plt.text(j + 0.03, stock[i, j], f"{stock[i, j]:.1f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [stock[i, j], stock[i, j + 1]], 'b')
            plt.plot([j, j + 1], [stock[i, j], stock[i + 1, j + 1]], 'b')

    plt.title("CRR Stock Price Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Stock Price")
    plt.grid(True)
    st.pyplot(fig)

    # Plot call option value tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, call_tree[i, j], color='red', s=60)
            plt.text(j + 0.03, call_tree[i, j], f"{call_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [call_tree[i, j], call_tree[i, j + 1]], 'b')
            plt.plot([j, j + 1], [call_tree[i, j], call_tree[i + 1, j + 1]], 'b')

    plt.title("European Call Option Value Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Option Price")
    plt.grid(True)
    st.pyplot(fig)

    # Plot put option value tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, put_tree[i, j], color='green', s=60)
            plt.text(j + 0.03, put_tree[i, j], f"{put_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [put_tree[i, j], put_tree[i, j + 1]], 'b')
            plt.plot([j, j + 1], [put_tree[i, j], put_tree[i + 1, j + 1]], 'b')

    plt.title("European Put Option Value Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Option Price")
    plt.grid(True)
    st.pyplot(fig)

    # Display results
    st.subheader("Option Prices")
    st.write(f"Call Option Price: {call_price:.4f}")
    st.write(f"Put Option Price: {put_price:.4f}")

elif program_mode == 'Jarrow-Rudd':
    st.title("Jarrow-Rudd (1979) Binomial Tree Model")

    # Input parameters
    S0 = st.sidebar.number_input('Initial Stock Price (S0)', min_value=0.0, value=100.0)
    K = st.sidebar.number_input('Strike Price (K)', min_value=0.0, value=100.0)
    T = st.sidebar.number_input('Time to Maturity (T) in years', min_value=0.01, value=1.0)
    r = st.sidebar.number_input('Risk-Free Rate (r)', min_value=0.0, max_value=1.0, value=0.05, format="%.4f")
    sigma = st.sidebar.number_input('Volatility (σ)', min_value=0.0, max_value=1.0, value=0.2, format="%.4f")
    N = st.sidebar.number_input('Number of Steps (N)', min_value=1, value=100)

    # Calculate option prices and trees using the Jarrow-Rudd model
    call_price, put_price, stock, call_tree, put_tree = f.jr_option_price(S0, K, T, r, sigma, N)

    # Plot stock price tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, stock[i, j], s=60)
            plt.text(j + 0.03, stock[i, j], f"{stock[i, j]:.1f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [stock[i, j], stock[i, j + 1]], 'b')
            plt.plot([j, j + 1], [stock[i, j], stock[i + 1, j + 1]], 'b')

    plt.title("CRR Stock Price Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Stock Price")
    plt.grid(True)
    st.pyplot(fig)

    # Plot call option value tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, call_tree[i, j], color='red', s=60)
            plt.text(j + 0.03, call_tree[i, j], f"{call_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [call_tree[i, j], call_tree[i, j + 1]], 'b')
            plt.plot([j, j + 1], [call_tree[i, j], call_tree[i + 1, j + 1]], 'b')

    plt.title("European Call Option Value Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Option Price")
    plt.grid(True)
    st.pyplot(fig)
    
    # Plot put option value tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, put_tree[i, j], color='green', s=60)
            plt.text(j + 0.03, put_tree[i, j], f"{put_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [put_tree[i, j], put_tree[i, j + 1]], 'b')
            plt.plot([j, j + 1], [put_tree[i, j], put_tree[i + 1, j + 1]], 'b')

    plt.title("European Put Option Value Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Option Price")
    plt.grid(True)
    st.pyplot(fig)

    # Display results
    st.subheader("Option Prices")
    st.write(f"Call Option Price: {call_price:.4f}")
    st.write(f"Put Option Price: {put_price:.4f}")

elif program_mode == 'Leisen-Reimer':
    st.title("Leisen-Reimer (1979) Binomial Tree Model")

    # Input parameters
    S0 = st.sidebar.number_input('Initial Stock Price (S0)', min_value=0.0, value=100.0)
    K = st.sidebar.number_input('Strike Price (K)', min_value=0.0, value=100.0)
    T = st.sidebar.number_input('Time to Maturity (T) in years', min_value=0.01, value=1.0)
    r = st.sidebar.number_input('Risk-Free Rate (r)', min_value=0.0, max_value=1.0, value=0.05, format="%.4f")
    sigma = st.sidebar.number_input('Volatility (σ)', min_value=0.0, max_value=1.0, value=0.2, format="%.4f")
    N = st.sidebar.number_input('Number of Steps (N)', min_value=1, value=100)

    # Calculate option prices and trees using the Leisen-Reimer model
    call_price, put_price, stock, call_tree, put_tree = f.lr_option_price(S0, K, T, r, sigma, N)

    # Plot stock price tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, stock[i, j], s=60)
            plt.text(j + 0.03, stock[i, j], f"{stock[i, j]:.1f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [stock[i, j], stock[i, j + 1]], 'b')
            plt.plot([j, j + 1], [stock[i, j], stock[i + 1, j + 1]], 'b')

    plt.title("Leisen-Reimer Stock Price Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Stock Price")
    plt.grid(True)
    st.pyplot(fig)

    # Plot call option value tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, call_tree[i, j], color='red', s=60)
            plt.text(j + 0.03, call_tree[i, j], f"{call_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [call_tree[i, j], call_tree[i, j + 1]], 'b')
            plt.plot([j, j + 1], [call_tree[i, j], call_tree[i + 1, j + 1]], 'b')

    plt.title("European Call Option Value Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Option Price")
    plt.grid(True)
    st.pyplot(fig)
    
    # Plot put option value tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, put_tree[i, j], color='green', s=60)
            plt.text(j + 0.03, put_tree[i, j], f"{put_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [put_tree[i, j], put_tree[i, j + 1]], 'b')
            plt.plot([j, j + 1], [put_tree[i, j], put_tree[i + 1, j + 1]], 'b')

    plt.title("European Put Option Value Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Option Price")
    plt.grid(True)
    st.pyplot(fig)

    # Display results
    st.subheader("Option Prices")
    st.write(f"Call Option Price: {call_price:.4f}")
    st.write(f"Put Option Price: {put_price:.4f}")

elif program_mode == "Tian":
    st.title("Tian (1993) Binomial Tree Model")

    # Input parameters
    S0 = st.sidebar.number_input('Initial Stock Price (S0)', min_value=0.0, value=100.0)
    K = st.sidebar.number_input('Strike Price (K)', min_value=0.0, value=100.0)
    T = st.sidebar.number_input('Time to Maturity (T) in years', min_value=0.01, value=1.0)
    r = st.sidebar.number_input('Risk-Free Rate (r)', min_value=0.0, max_value=1.0, value=0.05, format="%.4f")
    sigma = st.sidebar.number_input('Volatility (σ)', min_value=0.0, max_value=1.0, value=0.2, format="%.4f")
    N = st.sidebar.number_input('Number of Steps (N)', min_value=1, value=100)

    # Calculate option prices and trees using the Tian model
    call_price, put_price, stock, call_tree, put_tree = f.tian_option_price(S0, K, T, r, sigma, N)

    # Plot stock price tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, stock[i, j], s=60)
            plt.text(j + 0.03, stock[i, j], f"{stock[i, j]:.1f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [stock[i, j], stock[i, j + 1]], 'b')
            plt.plot([j, j + 1], [stock[i, j], stock[i + 1, j + 1]], 'b')

    plt.title("Tian Stock Price Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Stock Price")
    plt.grid(True)
    st.pyplot(fig)

    # Plot call option value tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, call_tree[i, j], color='red', s=60)
            plt.text(j + 0.03, call_tree[i, j], f"{call_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [call_tree[i, j], call_tree[i, j + 1]], 'b')
            plt.plot([j, j + 1], [call_tree[i, j], call_tree[i + 1, j + 1]], 'b')

    plt.title("European Call Option Value Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Option Price")
    plt.grid(True)
    st.pyplot(fig)
    
    # Plot put option value tree
    fig = plt.figure(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            plt.scatter(j, put_tree[i, j], color='green', s=60)
            plt.text(j + 0.03, put_tree[i, j], f"{put_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            plt.plot([j, j + 1], [put_tree[i, j], put_tree[i, j + 1]], 'b')
            plt.plot([j, j + 1], [put_tree[i, j], put_tree[i + 1, j + 1]], 'b')

    plt.title("European Put Option Value Tree")
    plt.xlabel("Time Step")
    plt.ylabel("Option Price")
    plt.grid(True)
    st.pyplot(fig)

    # Display results
    st.subheader("Option Prices")
    st.write(f"Call Option Price: {call_price:.4f}")
    st.write(f"Put Option Price: {put_price:.4f}")

elif program_mode == 'Figlewski':
    st.title('Figlewski & Gao (1999) Adaptive Mesh Model')

    S0 = st.sidebar.number_input('Initial Stock Price (S0)', min_value=0.0, value=100.0)
    K = st.sidebar.number_input('Strike Price (K)', min_value=0.0, value=100.0)
    T = st.sidebar.number_input('Time to Maturity (T) in years', min_value=0.01, value=1.0)
    r = st.sidebar.number_input('Risk-Free Rate (r)', min_value=0.0, max_value=1.0, value=0.05, format='%.4f')
    sigma = st.sidebar.number_input('Volatility (σ)', min_value=0.0, max_value=1.0, value=0.2, format='%.4f')
    N = st.sidebar.number_input('Number of Time Steps (N)', min_value=10, value=200)

    call_price = f.figlewski_option_price(S0, K, T, r, sigma, N, option='call')
    put_price = f.figlewski_option_price(S0, K, T, r, sigma, N, option='put')

    plot_model_sensitivity_curve(
        'Figlewski',
        f.figlewski_option_price,
        f.figlewski_option_price,
        S0,
        K,
        T,
        r,
        sigma,
        N,
    )

    st.subheader('Option Prices')
    st.write(f'Call Option Price: {call_price:.4f}')
    st.write(f'Put Option Price: {put_price:.4f}')
    st.write('This pricing uses an adaptive non-uniform mesh around the strike price.')

elif program_mode == 'Hull-White':
    st.title('Hull-White (2004) Finite Difference Model')

    S0 = st.sidebar.number_input('Initial Stock Price (S0)', min_value=0.0, value=100.0)
    K = st.sidebar.number_input('Strike Price (K)', min_value=0.0, value=100.0)
    T = st.sidebar.number_input('Time to Maturity (T) in years', min_value=0.01, value=1.0)
    r = st.sidebar.number_input('Risk-Free Rate (r)', min_value=0.0, max_value=1.0, value=0.05, format='%.4f')
    sigma = st.sidebar.number_input('Volatility (σ)', min_value=0.0, max_value=1.0, value=0.2, format='%.4f')
    N = st.sidebar.number_input('Number of Time Steps (N)', min_value=10, value=200)

    call_price = f.hull_white_option_price(S0, K, T, r, sigma, N, option='call')
    put_price = f.hull_white_option_price(S0, K, T, r, sigma, N, option='put')

    plot_model_sensitivity_curve(
        'Hull-White',
        f.hull_white_option_price,
        f.hull_white_option_price,
        S0,
        K,
        T,
        r,
        sigma,
        N,
    )

    st.subheader('Option Prices')
    st.write(f'Call Option Price: {call_price:.4f}')
    st.write(f'Put Option Price: {put_price:.4f}')
    st.write('This pricing solves the Black-Scholes PDE on a uniform grid in log-price space.')

