"""Interactive CFA Portfolio Management risk and return page."""

import numpy as np
import streamlit as st

from quantitative_methods import (
    average_squared_deviation,
    beta,
    capital_market_line_return,
    capital_market_line_risk,
    correlation_coefficient,
    covariance,
    global_minimum_variance_portfolio,
    jensens_alpha,
    msquared_ratio,
    portfolio_return,
    portfolio_standard_deviation,
    portfolio_variance,
    security_market_line_return,
    sharpe_ratio,
    treynor_ratio,
    two_asset_portfolio_variance,
)


def _returns(text):
    return np.asarray([float(value.strip()) / 100 for value in text.split(",") if value.strip()], dtype=float)


def _covariance_matrix(first_returns, second_returns):
    return np.cov(np.vstack([first_returns, second_returns]), ddof=1)


st.set_page_config(page_title="Portfolio Risk and Return", layout="wide", page_icon="quantrf_logo_website.png")
st.sidebar.image("images/sidebar_logo.png")
for page, label, disabled in [
    ("pages/monte_carlo.py", "Monte Carlo", False),
    ("main.py", "Black-Scholes-Merton (1973)", False),
    ("pages/black.py", "Black (1976)", True),
    ("pages/binomial_tree.py", "Binomial Tree", False),
    ("pages/trinomial_tree.py", "Trinomial Tree", True),
    ("pages/interest_rate_models.py", "Interest Rate Models", False),
    ("pages/american_option_pricing.py", "American Option Pricing", False),
    ("pages/credit_risk.py", "Credit Risk", False),
    ("pages/risk_management.py", "Risk Management", False),
    ("pages/volatility_models.py", "Volatility Models", False),
    ("pages/cfa_curriculum.py", "Rates and Returns", False),
    ("pages/time_value_of_money.py", "Time Value of Money", False),
    ("pages/types_of_financial_return.py", "Types of Financial Return", False),
    ("pages/portfolio_risk_return.py", "Portfolio Risk and Return", False),
    ("pages/fixed_income_yield_spreads.py", "Fixed Income Yield Spreads", False),
    ("pages/market_organization_structure.py", "Market Organization and Structure", False),
    ("pages/security_market_indexes.py", "Security Market Indexes", False),
    ("pages/forward_commitment_contingent_claims.py", "Forward Commitments and Contingent Claims", False),
    ("pages/option_replication_put_call_parity.py", "Option Replication Using Put-Call Parity", False),
    ("pages/capital_structure.py", "Capital Structure", False),
    ("pages/alternative_investments.py", "Alternative Investments", False),
    ("pages/alternative_investment_performance.py", "Alternative Investment Performance", False),
    ("pages/references.py", "References", False),
]:
    st.sidebar.page_link(page=page, label=label, disabled=disabled)

st.title("Portfolio Risk and Return")
st.caption("Portfolio Management | CFA-aligned interactive learning lab")
st.write(
    "Portfolio analysis combines expected returns with dispersion and co-movement. "
    "Use the controls below to see how diversification, market exposure, and active performance measures change the investment decision."
)

portfolio_tab, frontier_tab, market_tab, evaluation_tab = st.tabs(
    ["Portfolio statistics", "Efficient frontier", "CAL and SML", "Performance evaluation"]
)

with portfolio_tab:
    st.subheader("Portfolio return and dispersion")
    col1, col2, col3 = st.columns(3)
    asset_one_return = col1.number_input("Asset 1 expected return", value=0.08, format="%.4f")
    asset_two_return = col2.number_input("Asset 2 expected return", value=0.12, format="%.4f")
    asset_one_weight = col3.slider("Asset 1 weight", 0.0, 1.0, 0.50, 0.05)
    asset_two_weight = 1.0 - asset_one_weight
    weights = np.array([asset_one_weight, asset_two_weight])
    expected_returns = np.array([asset_one_return, asset_two_return])
    return_value = portfolio_return(weights, expected_returns)
    st.metric("Portfolio return", f"{return_value:.2%}")
    st.latex(r"E(R_p)=\sum_{i=1}^{n}w_iE(R_i)")
    st.write("Portfolio return is the weighted average of the component expected returns. The weights should sum to one for a fully invested long-only portfolio.")

    first_text = st.text_input("Asset 1 historical returns (%)", "8, 4, -2, 10, 6, 12")
    second_text = st.text_input("Asset 2 historical returns (%)", "5, 7, 1, 9, 3, 8")
    first_returns = _returns(first_text)
    second_returns = _returns(second_text)
    if first_returns.size == second_returns.size and first_returns.size >= 2:
        avg_deviation = average_squared_deviation(first_returns)
        covariance_value = covariance(first_returns, second_returns)
        correlation_value = correlation_coefficient(first_returns, second_returns)
        covariance_matrix = _covariance_matrix(first_returns, second_returns)
        variance_value = portfolio_variance(weights, covariance_matrix)
        standard_deviation = portfolio_standard_deviation(variance_value)
        deviation_col, covariance_col, correlation_col, standard_col = st.columns(4)
        deviation_col.metric("Average squared deviation", f"{avg_deviation:.6f}")
        covariance_col.metric("Covariance", f"{covariance_value:.6f}")
        correlation_col.metric("Correlation coefficient", f"{correlation_value:.4f}")
        standard_col.metric("Portfolio standard deviation", f"{standard_deviation:.2%}")
        st.latex(r"ASD=\frac{\sum_{t=1}^{T}(R_t-\bar R)^2}{T}\qquad Cov_{12}=E[(R_1-\bar R_1)(R_2-\bar R_2)]")
        st.latex(r"\rho_{12}=\frac{Cov_{12}}{\sigma_1\sigma_2}\qquad \sigma_p=\sqrt{w^T\Sigma w}")
        st.write("Average squared deviation measures dispersion around a mean. Covariance and correlation measure co-movement; lower or negative co-movement can reduce portfolio risk even when individual asset risk is unchanged.")
    else:
        st.warning("Enter two return series with the same number of observations and at least two observations.")

    st.subheader("Two-asset portfolio variance")
    variance_one = st.number_input("Asset 1 variance", value=0.04, min_value=0.0, format="%.5f")
    variance_two = st.number_input("Asset 2 variance", value=0.09, min_value=0.0, format="%.5f")
    covariance_between = st.number_input("Covariance between assets", value=0.01, format="%.5f")
    two_asset_variance = two_asset_portfolio_variance(asset_one_weight, asset_two_weight, variance_one, variance_two, covariance_between)
    st.metric("Two-asset portfolio variance", f"{two_asset_variance:.6f}")
    st.latex(r"\sigma_p^2=w_1^2\sigma_1^2+w_2^2\sigma_2^2+2w_1w_2Cov_{12}")
    st.write("The covariance term is the diversification term: it determines whether combining the assets creates more or less risk than a simple weighted average of their standalone variances.")

with frontier_tab:
    st.subheader("Global minimum variance portfolio")
    if first_returns.size == second_returns.size and first_returns.size >= 2:
        covariance_matrix = _covariance_matrix(first_returns, second_returns)
        gmvp_weights, gmvp_variance, gmvp_standard_deviation = global_minimum_variance_portfolio(covariance_matrix)
        weight_col, variance_col, risk_col = st.columns(3)
        weight_col.metric("GMVP asset 1 weight", f"{gmvp_weights[0]:.2%}")
        variance_col.metric("GMVP variance", f"{gmvp_variance:.6f}")
        risk_col.metric("GMVP standard deviation", f"{gmvp_standard_deviation:.2%}")
        st.latex(r"w_{GMVP}=\frac{\Sigma^{-1}\mathbf{1}}{\mathbf{1}^T\Sigma^{-1}\mathbf{1}}")
        st.write("The global minimum variance portfolio is the fully invested portfolio with the lowest variance for the supplied covariance matrix. It is the left-most point of the feasible risk-return set, not necessarily the highest-return portfolio.")
    else:
        st.info("Use matching historical return series in the Portfolio statistics tab to calculate the GMVP.")

with market_tab:
    st.subheader("Capital Market Line")
    st.write("In this example, the market is defined as the domestic stock market index. The CML describes optimal combinations of the risk-free asset and that market portfolio.")
    col1, col2, col3 = st.columns(3)
    risk_free = col1.number_input("Risk-free rate", value=0.04, format="%.4f")
    market_return = col2.number_input("Domestic market index return", value=0.10, format="%.4f")
    market_risk = col3.number_input("Domestic market index standard deviation", value=0.18, min_value=0.0001, format="%.4f")
    target_risk = st.number_input("Target portfolio standard deviation", value=0.12, min_value=0.0, format="%.4f")
    cal_return = capital_market_line_return(risk_free, market_return, market_risk, target_risk)
    target_return = st.number_input("Target portfolio return", value=0.08, format="%.4f")
    cal_risk = capital_market_line_risk(risk_free, market_return, market_risk, target_return)
    return_col, risk_col = st.columns(2)
    return_col.metric("CML return at target risk", f"{cal_return:.2%}")
    risk_col.metric("CML risk at target return", f"{cal_risk:.2%}")
    st.latex(r"E(R_C)=R_f+\frac{E(R_M)-R_f}{\sigma_M}\sigma_C")
    st.write("The CML uses total standard deviation and applies only to efficient portfolios formed from the risk-free asset and the market portfolio. Its slope is the market Sharpe ratio.")

    st.subheader("Security Market Line and beta")
    market_text = st.text_input("Market index returns (%)", "5, 7, 1, 9, 3, 8")
    asset_text = st.text_input("Security returns (%)", "6, 9, 0, 11, 4, 10")
    market_series = _returns(market_text)
    asset_series = _returns(asset_text)
    if market_series.size == asset_series.size and market_series.size >= 2:
        beta_value = beta(asset_series, market_series)
        sml_return = security_market_line_return(risk_free, beta_value, market_return)
        beta_col, sml_col = st.columns(2)
        beta_col.metric("Beta", f"{beta_value:.4f}")
        sml_col.metric("SML required return", f"{sml_return:.2%}")
        st.latex(r"\beta_i=\frac{Cov(R_i,R_M)}{Var(R_M)}\qquad E(R_i)=R_f+\beta_i[E(R_M)-R_f]")
        st.write("Beta measures a security's sensitivity to market returns. Unlike the CML, the SML applies to any security, efficient or not, and prices systematic risk through beta rather than total volatility.")

with evaluation_tab:
    st.subheader("Risk-adjusted performance")
    portfolio_return_value = st.number_input("Portfolio realized return", value=0.11, format="%.4f")
    portfolio_risk = st.number_input("Portfolio standard deviation", value=0.16, min_value=0.0001, format="%.4f")
    portfolio_beta = st.number_input("Portfolio beta", value=1.10, format="%.4f")
    sharpe = sharpe_ratio(portfolio_return_value, risk_free, portfolio_risk)
    treynor = treynor_ratio(portfolio_return_value, risk_free, portfolio_beta)
    msquared = msquared_ratio(portfolio_return_value, risk_free, portfolio_risk, market_risk)
    alpha = jensens_alpha(portfolio_return_value, risk_free, portfolio_beta, market_return)
    sharpe_col, treynor_col, msquared_col, alpha_col = st.columns(4)
    sharpe_col.metric("Sharpe ratio", f"{sharpe:.4f}")
    treynor_col.metric("Treynor ratio", f"{treynor:.4%}")
    msquared_col.metric("M-squared return", f"{msquared:.2%}")
    alpha_col.metric("Jensen's alpha", f"{alpha:.2%}")
    st.latex(r"Sharpe=\frac{R_p-R_f}{\sigma_p}\qquad Treynor=\frac{R_p-R_f}{\beta_p}")
    st.latex(r"M^2=R_f+Sharpe_p\sigma_M\qquad \alpha_J=R_p-[R_f+\beta_p(R_M-R_f)]")
    st.write("Sharpe uses total risk, so it is useful for evaluating a complete portfolio. Treynor uses systematic risk, so it is useful when the portfolio is already diversified. M-squared converts Sharpe performance into return units, while Jensen's alpha measures performance above or below the SML prediction.")
