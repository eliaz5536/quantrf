import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import streamlit as st
import black_scholes_app as f
import svi
import math_documentation as math_doc

from scipy.interpolate import griddata

plt.rcParams.update({
    "figure.autolayout": True,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})


def configure_tree_axes(ax, N):
    """Use integer x ticks for time step and avoid decimal y labels on stock prices."""
    ax.set_xlim(-0.1, N + 0.1)
    ax.set_xticks(np.arange(0, N + 1, 1))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{int(round(x))}"))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, pos: f"{int(round(y))}"))
    ax.grid(True, alpha=0.3)


def render_tree_figure(fig):
    """Render a Matplotlib figure with layout space reserved for axis labels."""
    fig.tight_layout(pad=1.5)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.12, top=0.9)
    st.pyplot(fig)


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

st.set_page_config(page_title="Binomial Tree", layout="wide", page_icon="quantrf_logo_website.png")
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


program_mode = st.sidebar.radio(
    'Select Model:',
    ('Cox-Ross-Rubinstein', 'Figlewski', 'Jarrow-Rudd', 'Leisen-Reimer', 'Tian', 'Hull-White')
)

if program_mode == 'Cox-Ross-Rubinstein':
    st.title("Cox-Ross-Rubinstein (1979) Binomial Tree Model")
    math_doc.binomial("crr")

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
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, stock[i, j], s=60)
            ax.text(j + 0.03, stock[i, j], f"{stock[i, j]:.1f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [stock[i, j], stock[i, j + 1]], 'b')
            ax.plot([j, j + 1], [stock[i, j], stock[i + 1, j + 1]], 'b')

    ax.set_title("CRR Stock Price Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Stock Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Plot call option value tree
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, call_tree[i, j], color='red', s=60)
            ax.text(j + 0.03, call_tree[i, j], f"{call_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [call_tree[i, j], call_tree[i, j + 1]], 'b')
            ax.plot([j, j + 1], [call_tree[i, j], call_tree[i + 1, j + 1]], 'b')

    ax.set_title("European Call Option Value Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Option Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Plot put option value tree
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, put_tree[i, j], color='green', s=60)
            ax.text(j + 0.03, put_tree[i, j], f"{put_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [put_tree[i, j], put_tree[i, j + 1]], 'b')
            ax.plot([j, j + 1], [put_tree[i, j], put_tree[i + 1, j + 1]], 'b')

    ax.set_title("European Put Option Value Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Option Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Display results
    st.subheader("Option Prices")
    st.write(f"Call Option Price: {call_price:.4f}")
    st.write(f"Put Option Price: {put_price:.4f}")

elif program_mode == 'Jarrow-Rudd':
    st.title("Jarrow-Rudd (1979) Binomial Tree Model")
    math_doc.binomial("jr")

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
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, stock[i, j], s=60)
            ax.text(j + 0.03, stock[i, j], f"{stock[i, j]:.1f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [stock[i, j], stock[i, j + 1]], 'b')
            ax.plot([j, j + 1], [stock[i, j], stock[i + 1, j + 1]], 'b')

    ax.set_title("Jarrow-Rudd Stock Price Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Stock Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Plot call option value tree
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, call_tree[i, j], color='red', s=60)
            ax.text(j + 0.03, call_tree[i, j], f"{call_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [call_tree[i, j], call_tree[i, j + 1]], 'b')
            ax.plot([j, j + 1], [call_tree[i, j], call_tree[i + 1, j + 1]], 'b')

    ax.set_title("European Call Option Value Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Option Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)
    
    # Plot put option value tree
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, put_tree[i, j], color='green', s=60)
            ax.text(j + 0.03, put_tree[i, j], f"{put_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [put_tree[i, j], put_tree[i, j + 1]], 'b')
            ax.plot([j, j + 1], [put_tree[i, j], put_tree[i + 1, j + 1]], 'b')

    ax.set_title("European Put Option Value Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Option Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Display results
    st.subheader("Option Prices")
    st.write(f"Call Option Price: {call_price:.4f}")
    st.write(f"Put Option Price: {put_price:.4f}")

elif program_mode == 'Leisen-Reimer':
    st.title("Leisen-Reimer (1979) Binomial Tree Model")
    math_doc.binomial("lr")

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
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, stock[i, j], s=60)
            ax.text(j + 0.03, stock[i, j], f"{stock[i, j]:.1f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [stock[i, j], stock[i, j + 1]], 'b')
            ax.plot([j, j + 1], [stock[i, j], stock[i + 1, j + 1]], 'b')

    ax.set_title("Leisen-Reimer Stock Price Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Stock Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Plot call option value tree
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, call_tree[i, j], color='red', s=60)
            ax.text(j + 0.03, call_tree[i, j], f"{call_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [call_tree[i, j], call_tree[i, j + 1]], 'b')
            ax.plot([j, j + 1], [call_tree[i, j], call_tree[i + 1, j + 1]], 'b')

    ax.set_title("European Call Option Value Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Option Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)
    
    # Plot put option value tree
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, put_tree[i, j], color='green', s=60)
            ax.text(j + 0.03, put_tree[i, j], f"{put_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [put_tree[i, j], put_tree[i, j + 1]], 'b')
            ax.plot([j, j + 1], [put_tree[i, j], put_tree[i + 1, j + 1]], 'b')

    ax.set_title("European Put Option Value Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Option Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Display results
    st.subheader("Option Prices")
    st.write(f"Call Option Price: {call_price:.4f}")
    st.write(f"Put Option Price: {put_price:.4f}")

elif program_mode == "Tian":
    st.title("Tian (1993) Binomial Tree Model")
    math_doc.binomial("tian")

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
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, stock[i, j], s=60)
            ax.text(j + 0.03, stock[i, j], f"{stock[i, j]:.1f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [stock[i, j], stock[i, j + 1]], 'b')
            ax.plot([j, j + 1], [stock[i, j], stock[i + 1, j + 1]], 'b')

    ax.set_title("Tian Stock Price Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Stock Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Plot call option value tree
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, call_tree[i, j], color='red', s=60)
            ax.text(j + 0.03, call_tree[i, j], f"{call_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [call_tree[i, j], call_tree[i, j + 1]], 'b')
            ax.plot([j, j + 1], [call_tree[i, j], call_tree[i + 1, j + 1]], 'b')

    ax.set_title("European Call Option Value Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Option Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)
    
    # Plot put option value tree
    fig, ax = plt.subplots(figsize=(9, 6))
    for j in range(N + 1):
        for i in range(j + 1):
            ax.scatter(j, put_tree[i, j], color='green', s=60)
            ax.text(j + 0.03, put_tree[i, j], f"{put_tree[i, j]:.2f}", fontsize=9)

    for j in range(N):
        for i in range(j + 1):
            ax.plot([j, j + 1], [put_tree[i, j], put_tree[i, j + 1]], 'b')
            ax.plot([j, j + 1], [put_tree[i, j], put_tree[i + 1, j + 1]], 'b')

    ax.set_title("European Put Option Value Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Option Price")
    configure_tree_axes(ax, N)
    render_tree_figure(fig)

    # Display results
    st.subheader("Option Prices")
    st.write(f"Call Option Price: {call_price:.4f}")
    st.write(f"Put Option Price: {put_price:.4f}")

elif program_mode == 'Figlewski':
    st.title('Figlewski & Gao (1999) Adaptive Mesh Model')
    math_doc.finite_difference('Figlewski & Gao')

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
    math_doc.finite_difference('Hull-White')

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

