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
st.sidebar.page_link(page="", label="Monte Carlo")
st.sidebar.page_link(page="main.py", label="Black-Scholes-Merton (1973)")
st.sidebar.page_link(page="pages/black.py", label="Black (1976)", disabled=False)
st.sidebar.page_link(page="pages/binomial_tree.py", label="Binomial Tree", disabled=False)
st.sidebar.page_link(page="pages/trinomial_tree.py", label="Trinomial Tree", disabled=False)
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

    # Calculate option prices and trees using the CRR model
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

# ! REVIEW
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

    st.subheader('Option Prices')
    st.write(f'Call Option Price: {call_price:.4f}')
    st.write(f'Put Option Price: {put_price:.4f}')
    st.write('This pricing uses an adaptive non-uniform mesh around the strike price.')

# ! REVIEW
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

    st.subheader('Option Prices')
    st.write(f'Call Option Price: {call_price:.4f}')
    st.write(f'Put Option Price: {put_price:.4f}')
    st.write('This pricing solves the Black-Scholes PDE on a uniform grid in log-price space.')





####################################################################################
# Binomial Tree
####################################################################################

def crr_option_stock(S, K, T, r, sigma, N):
    dt = T / N

    # CRR parameters
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    # stock price tree
    stock = np.zeros((N + 1, N + 1))

    for j in range(N + 1):
        for i in range(j + 1):
            stock[i,j] = S * (u ** (j - i)) * (d ** i)

    return stock


def crr_option_price(S, K, T, r, sigma, N):
    dt = T / N

    # CRR parameters
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    # stock price tree
    stock = np.zeros((N + 1, N + 1))
    for j in range(N + 1):
        for i in range(j + 1):
            stock[i, j] = S * (u ** (j - i)) * (d ** i)

    # Option value trees for call and put
    call_tree = np.zeros((N + 1, N + 1))
    put_tree = np.zeros((N + 1, N + 1))

    # terminal payoff
    call_tree[:, N] = np.maximum(stock[:, N] - K, 0)
    put_tree[:, N] = np.maximum(K - stock[:, N], 0)

    # backward induction
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            call_tree[i, j] = discount * (p * call_tree[i, j + 1] + (1 - p) * call_tree[i + 1, j + 1])
            put_tree[i, j] = discount * (p * put_tree[i, j + 1] + (1 - p) * put_tree[i + 1, j + 1])

    call_price = call_tree[0, 0]
    put_price = put_tree[0, 0]
    return call_price, put_price, stock, call_tree, put_tree


def jr_option_price(S, K, T, r, sigma, N):
    dt = T / N

    u = np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt))
    d = np.exp((r - 0.5*sigma**2)*dt - sigma*np.sqrt(dt))

    p = 0.5

    discount = np.exp(-r*dt)

    stock_tree = np.zeros((N + 1, N + 1))

    for i in range(N+1):
        for j in range(i + 1):
            stock_tree[j, i] = S * (u**j) * (d**(i-j))

    # Option value trees for call and put
    call_tree = np.zeros((N + 1, N + 1))
    put_tree = np.zeros((N + 1, N + 1))


    # Terminal Payoff
    for j in range(N + 1):
        call_tree[j, N] = max(stock_tree[j, N] - K, 0)
        put_tree[j, N] = max(K-stock_tree[j, N], 0)

    # Backward Induction
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            call_tree[j, i] + discount * (p * call_tree[j + 1, i + 1] + (1 - p) * call_tree[j, i + 1])
            put_tree[j, i] + discount * (p * put_tree[j + 1, i + 1] + (1 - p) * put_tree[j, i + 1])

    call_price = call_tree[0, 0]
    put_price = put_tree[0, 0]

    return call_price, put_price, stock_tree, call_tree, put_tree

def h_inverse(z, n):
    """
    Peizer-Pratt inversion used in Leisen Reimer (1996).

    Parameters
    ----------
    z : float
        Usually d1 or d2
    n : int
        Nomber of time steps (proferably odd).

    Returns
    -------
    float
        Probability approximation
    """
    if n % 2 == 0:
        n += 1

    a = n + 1/3
    b = 1/(n + 1/6)

    exponent = -(z/a)**2 * (n + 1/6)

    return 0.5 + np.sign(z) * np.sqrt(0.25 * (1 - np.exp(exponent)))


def lr_option_price(S, K, T, r, sigma, N):
    if N % 2 == 0:
        N += 1    

    dt = T / N

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    p = h_inverse(d2, N)
    p_prime = h_inverse(d1, N)

    growth = np.exp(r * dt)

    u = growth * p_prime / p
    d = (growth - p * u) / (1 - p)

    # build full stock price tree (same shape as other models)
    stock = np.zeros((N + 1, N + 1))
    for j in range(N + 1):
        for i in range(j + 1):
            stock[i, j] = S * (u ** (j - i)) * (d ** i)

    # Option value trees for call and put
    call_tree = np.zeros((N + 1, N + 1))
    put_tree = np.zeros((N + 1, N + 1))

    # Terminal payoff
    call_tree[:, N] = np.maximum(stock[:, N] - K, 0.0)
    put_tree[:, N] = np.maximum(K - stock[:, N], 0.0)

    disc = np.exp(-r * dt)

    # Backward induction
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            call_tree[i, j] = disc * (p * call_tree[i, j + 1] + (1 - p) * call_tree[i + 1, j + 1])
            put_tree[i, j] = disc * (p * put_tree[i, j + 1] + (1 - p) * put_tree[i + 1, j + 1])

    call_price = call_tree[0, 0]
    put_price = put_tree[0, 0]

    return call_price, put_price, stock, call_tree, put_tree


## ! REVIEW
def _solve_tridiagonal(lower, diag, upper, rhs):
    lower = lower.astype(float).copy()
    diag = diag.astype(float).copy()
    upper = upper.astype(float).copy()
    rhs = rhs.astype(float).copy()
    n = len(diag)
    for i in range(1, n):
        w = lower[i - 1] / diag[i - 1]
        diag[i] -= w * upper[i - 1]
        rhs[i] -= w * rhs[i - 1]

    x = np.empty(n, dtype=float)
    x[-1] = rhs[-1] / diag[-1]
    for i in range(n - 2, -1, -1):
        x[i] = (rhs[i] - upper[i] * x[i + 1]) / diag[i]

    return x

##! REVIEW
def _black_scholes_pde_log_grid(S, K, T, r, sigma, N, x_grid, option="call"):
    if T <= 0:
        return max(S - K, 0.0) if option == "call" else max(K - S, 0.0)

    M = len(x_grid) - 1
    S_grid = np.exp(x_grid)
    dt = T / N

    V = np.zeros((M + 1, N + 1), dtype=float)
    t_grid = np.arange(N + 1) * dt

    if option == "call":
        V[:, -1] = np.maximum(S_grid - K, 0.0)
        V[0, :] = 0.0
        V[-1, :] = S_grid[-1] - K * np.exp(-r * (T - t_grid))
    else:
        V[:, -1] = np.maximum(K - S_grid, 0.0)
        V[0, :] = K * np.exp(-r * (T - t_grid))
        V[-1, :] = 0.0

    mu = r - 0.5 * sigma**2
    sigma2 = 0.5 * sigma**2

    lower = np.zeros(M - 1, dtype=float)
    diag = np.zeros(M - 1, dtype=float)
    upper = np.zeros(M - 1, dtype=float)

    for i in range(1, M):
        dx_plus = x_grid[i + 1] - x_grid[i]
        dx_minus = x_grid[i] - x_grid[i - 1]
        dx_sum = dx_plus + dx_minus

        a = mu / dx_sum + sigma2 / (dx_minus * dx_sum)
        c = -mu / dx_sum + sigma2 / (dx_plus * dx_sum)
        b = -r + sigma2 * (1.0 / dx_plus + 1.0 / dx_minus) / dx_sum

        lower[i - 1] = -0.5 * dt * a
        diag[i - 1] = 1.0 - 0.5 * dt * b
        upper[i - 1] = -0.5 * dt * c

    for j in range(N - 1, -1, -1):
        rhs = np.zeros(M - 1, dtype=float)
        for i in range(1, M):
            dx_plus = x_grid[i + 1] - x_grid[i]
            dx_minus = x_grid[i] - x_grid[i - 1]
            dx_sum = dx_plus + dx_minus

            a = mu / dx_sum + sigma2 / (dx_minus * dx_sum)
            c = -mu / dx_sum + sigma2 / (dx_plus * dx_sum)
            b = -r + sigma2 * (1.0 / dx_plus + 1.0 / dx_minus) / dx_sum

            idx = i - 1
            rhs[idx] = (
                (1.0 + 0.5 * dt * b) * V[i, j + 1]
                + 0.5 * dt * a * V[i - 1, j + 1]
                + 0.5 * dt * c * V[i + 1, j + 1]
            )

        rhs[0] -= lower[0] * V[0, j]
        rhs[-1] -= upper[-1] * V[-1, j]

        V[1:-1, j] = _solve_tridiagonal(lower, diag, upper, rhs)

    v0 = np.interp(np.log(S), x_grid, V[:, 0])
    return float(v0)

## ! REVIEW
def figlewski_option_price(S, K, T, r, sigma, N, option="call"):
    M = max(200, N * 5)
    x_mid = np.log(K)
    x_std = max(4.0 * sigma * np.sqrt(T), 1.0)
    x_min = x_mid - x_std * 2.5
    x_max = x_mid + x_std * 2.5

    xi = np.linspace(-1.0, 1.0, M + 1)
    alpha = 4.0
    x_grid = x_mid + 0.5 * (x_max - x_min) * np.tanh(alpha * xi) / np.tanh(alpha)

    price = _black_scholes_pde_log_grid(S, K, T, r, sigma, N, x_grid, option=option)
    return price

## ! REVIEW
def hull_white_option_price(S, K, T, r, sigma, N, option="call"):
    M = max(200, N * 5)
    x_mid = np.log(K)
    width = max(8.0 * sigma * np.sqrt(T), abs(np.log(S / K)) * 2.0 + 1.0)
    x_grid = np.linspace(x_mid - width, x_mid + width, M + 1)

    price = _black_scholes_pde_log_grid(S, K, T, r, sigma, N, x_grid, option=option)
    return price

# ! REVIEW
def tian_option_price(S, K, T, r, sigma, N):
    dt = T / N

    R = np.exp(r * dt)
    V = np.exp(sigma**2 * dt)

    u = (R * V / 2) * (V + 1 + np.sqrt(V**2 + 2 * V - 3))
    d = (R * V / 2) * (V + 1 - np.sqrt(V**2 + 2 * V - 3))

    p = (R - d) / (u - d)

    disc = np.exp(-r * dt)

    stock = np.zeros((N + 1, N + 1))
    for j in range(N + 1):
        for i in range(j + 1):
            stock[i, j] = S * (u**i) * (d**(j - i))

    call_tree = np.zeros((N + 1, N + 1))
    put_tree = np.zeros((N + 1, N + 1))

    call_tree[:, N] = np.maximum(stock[:, N] - K, 0.0)
    put_tree[:, N] = np.maximum(K - stock[:, N], 0.0)

    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            call_tree[i, j] = disc * (p * call_tree[i, j + 1] + (1 - p) * call_tree[i + 1, j + 1])
            put_tree[i, j] = disc * (p * put_tree[i, j + 1] + (1 - p) * put_tree[i + 1, j + 1])

    call_price = call_tree[0, 0]
    put_price = put_tree[0, 0]

    return call_price, put_price, stock, call_tree, put_tree

####################################################################################
# Interest Rate Models
####################################################################################

# Cox-Ingersoll-Ross (1985)
def CIR(r0, kappa, theta, sigma, T, steps):
    dt = T / steps

    r = np.zeros(steps+1)
    r[0] = 0

    d= 4 * kappa * theta / sigma ** 2

    for i in range(steps):
        c = (sigma ** 2 * (1 - np.exp(-kappa * dt))) / (4*kappa)

        lam=(
            4 * kappa * np.exp(-kappa * dt) *r[i]
            / (sigma ** 2 * (1 - np.exp(-kappa * dt)))
        )

        r[i+1] = c * ncx2.rvs(d,lam)

    return r


def CIR_bond_price(r, kappa, theta, sigma, tau):
    gamma = np.sqrt(kappa ** 2 + 2 * sigma ** 2)
    numerator = 2 * (np.exp(gamma.tau) - 1)
    denominator = (gamma + kappa) * (np.exp(gamma * tau) - 1) + 2 * gamma

    B = numerator / denominator

    A = ((2 ** gamma * np.exp((kappa + gamma) * tau / 2) / denominator)) ** (2 * kappa * theta / sigma ** 2)

    return A * np.exp(-B * r)

# def CIR_show_bond_prices(r0, kappa, theta, sigma, tau):
def CIR_show_bond_prices(maturity, r0, kappa, theta, sigma, tau):
    maturity = np.linspace(.25, 30, 120)

    prices = []

    for tau in maturity:
        prices.append(CIR_bond_price(r0, kappa, theta, sigma, tau))
        prices = np.array(prices)

    return prices


def CIR_yield_curve(prices, maturity):
    return -np.log(prices) / maturity

# Vasicek
def vasicek_option_price(S, K, T, r, sigma, N):

    return call_price, put_price, stock, call_tree, put_tree
