import numpy as np
import pandas as pd
import streamlit as st
import math_documentation as math_doc

st.set_page_config(page_title="Monte Carlo Simulation", layout="wide", page_icon="quantrf_logo_website.png")
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

@st.cache_data(show_spinner=False)
def simulate_gbm_paths(spot, rate, volatility, maturity, steps, paths, seed):
    rng = np.random.default_rng(seed)
    dt = maturity / steps
    shocks = rng.standard_normal((paths, steps))
    increments = (rate - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * shocks
    log_paths = np.concatenate(
        [np.zeros((paths, 1)), np.cumsum(increments, axis=1)], axis=1
    )
    return spot * np.exp(log_paths)


@st.cache_data(show_spinner=False)
def simulate_normal_samples(mean, standard_deviation, sample_size, repetitions, seed):
    rng = np.random.default_rng(seed)
    samples = rng.normal(mean, standard_deviation, (repetitions, sample_size))
    sample_means = samples.mean(axis=1)
    running_means = np.cumsum(sample_means) / np.arange(1, repetitions + 1)
    return samples, sample_means, running_means


def show_sidebar():
    st.sidebar.header("Simulation Settings")
    mode = st.sidebar.radio(
        "Application",
        ("Stock Price (GBM)", "Sample Mean (LLN)"),
    )
    seed = st.sidebar.number_input("Random Seed", min_value=0, value=42, step=1)
    return mode, seed


mode, seed = show_sidebar()
st.title("Monte Carlo Simulation")
st.caption("Explore simulated paths, distributions, and convergence using Streamlit charts.")
math_doc.monte_carlo("gbm" if mode == "Stock Price (GBM)" else "lln")

if mode == "Stock Price (GBM)":
    st.sidebar.subheader("Geometric Brownian Motion")
    spot = st.sidebar.number_input("Initial Stock Price ($)", min_value=0.01, value=100.0, format="%.2f")
    rate = st.sidebar.number_input("Risk-Free Rate", min_value=-1.0, max_value=1.0, value=0.05, format="%.4f")
    volatility = st.sidebar.number_input("Volatility", min_value=0.0, max_value=5.0, value=0.20, format="%.4f")
    maturity = st.sidebar.number_input("Time to Maturity (Years)", min_value=0.01, value=1.0, format="%.2f")
    steps = st.sidebar.number_input("Time Steps", min_value=1, max_value=500, value=50, step=1)
    paths = st.sidebar.number_input("Simulation Paths", min_value=10, max_value=10000, value=1000, step=100)

    paths_array = simulate_gbm_paths(
        spot, rate, volatility, maturity, int(steps), int(paths), int(seed)
    )
    times = np.linspace(0.0, maturity, int(steps) + 1)
    endpoint_prices = paths_array[:, -1]
    expected_endpoint = spot * np.exp(rate * maturity)
    standard_error = endpoint_prices.std(ddof=1) / np.sqrt(len(endpoint_prices))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expected Price", f"${expected_endpoint:,.2f}")
    col2.metric("Simulated Mean", f"${endpoint_prices.mean():,.2f}")
    col3.metric("Simulated Std. Dev.", f"${endpoint_prices.std(ddof=1):,.2f}")
    col4.metric("Standard Error", f"${standard_error:,.2f}")

    st.subheader("Simulated Stock Price Paths")
    path_count = min(100, int(paths))
    path_frame = pd.DataFrame(
        paths_array[:path_count].T,
        index=times,
        columns=[f"Path {i + 1}" for i in range(path_count)],
    )
    path_frame.index.name = "Time (Years)"
    st.line_chart(path_frame, use_container_width=True)

    st.subheader("Terminal Stock Price Distribution")
    histogram_bins = st.slider("Histogram Bins", min_value=10, max_value=100, value=30, step=5)
    histogram, edges = np.histogram(endpoint_prices, bins=histogram_bins)
    histogram_frame = pd.DataFrame(
        {"Frequency": histogram},
        index=[f"{edges[i]:.2f} - {edges[i + 1]:.2f}" for i in range(len(histogram))],
    )
    st.bar_chart(histogram_frame, use_container_width=True)
    st.caption(
        "The terminal-price histogram shows the Monte Carlo distribution at maturity. "
        "Increasing the number of paths makes the estimated distribution and its mean more stable."
    )

    st.subheader("Convergence of the Simulated Mean")
    running_mean = np.cumsum(endpoint_prices) / np.arange(1, len(endpoint_prices) + 1)
    convergence_frame = pd.DataFrame(
        {
            "Running Mean": running_mean,
            "Theoretical Mean": expected_endpoint,
        },
        index=np.arange(1, len(endpoint_prices) + 1),
    )
    convergence_frame.index.name = "Number of Paths"
    st.line_chart(convergence_frame, use_container_width=True)

else:
    st.sidebar.subheader("Independent Normal Samples")
    population_mean = st.sidebar.number_input("Population Mean", value=0.0, format="%.2f")
    standard_deviation = st.sidebar.number_input(
        "Population Standard Deviation", min_value=0.01, value=1.0, format="%.2f"
    )
    sample_size = st.sidebar.number_input("Observations per Sample", min_value=1, max_value=1000, value=30, step=1)
    repetitions = st.sidebar.number_input("Repeated Samples", min_value=10, max_value=10000, value=1000, step=100)

    _, sample_means, running_means = simulate_normal_samples(
        population_mean,
        standard_deviation,
        int(sample_size),
        int(repetitions),
        int(seed),
    )
    standard_error = standard_deviation / np.sqrt(sample_size)

    col1, col2, col3 = st.columns(3)
    col1.metric("Population Mean", f"{population_mean:,.4f}")
    col2.metric("Average of Sample Means", f"{sample_means.mean():,.4f}")
    col3.metric("Theoretical Standard Error", f"{standard_error:,.4f}")

    st.subheader("Distribution of Repeated Sample Means")
    histogram_bins = st.slider("Histogram Bins", min_value=10, max_value=100, value=30, step=5)
    histogram, edges = np.histogram(sample_means, bins=histogram_bins)
    histogram_frame = pd.DataFrame(
        {"Frequency": histogram},
        index=[f"{edges[i]:.3f} - {edges[i + 1]:.3f}" for i in range(len(histogram))],
    )
    st.bar_chart(histogram_frame, use_container_width=True)

    st.subheader("Law of Large Numbers")
    convergence_frame = pd.DataFrame(
        {
            "Running Mean of Sample Means": running_means,
            "Population Mean": population_mean,
        },
        index=np.arange(1, len(running_means) + 1),
    )
    convergence_frame.index.name = "Number of Repeated Samples"
    st.line_chart(convergence_frame, use_container_width=True)
    st.caption(
        "As the number of repeated samples increases, the running average approaches the population mean."
    )
