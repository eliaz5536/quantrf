"""Interactive CFA Quantitative Methods financial returns page."""

import streamlit as st

from quantitative_methods import (
    annualized_effective_rate,
    beginning_distribution,
    beginning_price_change,
    complete_investor_outcome,
    distribution_price_interaction,
    effective_annual_rate,
    periods_per_year,
    risk_premium,
)


st.set_page_config(page_title="Types of Financial Return", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Types of Financial Return")
st.caption("Quantitative Methods | CFA-aligned interactive learning lab")
st.write(
    "Investment performance can come from a change in market price, cash distributions, or both. "
    "This page separates those components and annualizes returns so investments with different holding periods can be compared."
)

outcome_tab, distribution_tab, annualization_tab = st.tabs(
    ["Investor outcome", "Distribution mechanics", "Annualized returns"]
)

with outcome_tab:
    st.subheader("Complete investor outcome")
    col1, col2, col3 = st.columns(3)
    beginning_price = col1.number_input("Beginning price", value=100.0, min_value=0.01)
    ending_price = col2.number_input("Ending price", value=108.0, min_value=0.0)
    distribution = col3.number_input("Distribution received", value=2.0, min_value=0.0)
    price_change = beginning_price_change(beginning_price, ending_price)
    cash_received = beginning_distribution(distribution)
    investor_outcome = complete_investor_outcome(beginning_price, ending_price, distribution)
    holding_return = investor_outcome / beginning_price
    price_col, distribution_col, outcome_col = st.columns(3)
    price_col.metric("Change in market value", f"{price_change:,.2f}")
    distribution_col.metric("Beginning distribution", f"{cash_received:,.2f}")
    outcome_col.metric("Complete investor outcome", f"{investor_outcome:,.2f}")
    st.metric("Holding period return", f"{holding_return:.2%}")
    st.latex(r"\Delta P=P_1-P_0\qquad D=\text{cash received while held}\qquad Outcome=\Delta P+D")
    st.latex(r"HPR=\frac{P_1-P_0+D}{P_0}")
    st.info("The price component captures unrealized capital gain or loss. The distribution component captures dividends, coupons, or other cash received. Together they represent the investor's dollar outcome before fees and taxes.")

with distribution_tab:
    st.subheader("Distribution-price interaction")
    col1, col2 = st.columns(2)
    pre_distribution_price = col1.number_input("Price immediately before distribution", value=50.0, min_value=0.0)
    distribution_amount = col2.number_input("Distribution amount", value=1.25, min_value=0.0)
    ex_distribution_price = distribution_price_interaction(pre_distribution_price, distribution_amount)
    st.metric("Approximate price immediately after distribution", f"{ex_distribution_price:,.2f}")
    st.latex(r"P_{ex\text{-}distribution}\approx P_{before\ distribution}-D")
    st.write("On the ex-distribution date, the asset price is reduced approximately by the cash distribution because value has moved from the security into the investor's cash account. The price drop is not by itself a loss when the distribution is included in total return.")

    st.subheader("Risk premium")
    expected_return = st.number_input("Expected investment return", value=0.09, format="%.4f")
    risk_free_rate = st.number_input("Risk-free rate", value=0.04, format="%.4f")
    premium = risk_premium(expected_return, risk_free_rate)
    st.metric("Risk premium", f"{premium:.2%}")
    st.latex(r"Risk\ Premium=E(R_i)-R_f")
    st.write("Risk premium is the additional expected return demanded for bearing investment risk instead of holding a risk-free asset. It supports required-return estimates and asset-pricing comparisons.")

with annualization_tab:
    st.subheader("Annualized effective rate")
    col1, col2, col3 = st.columns(3)
    holding_period = col1.number_input("Holding period return", value=0.06, format="%.4f")
    days_held = col2.number_input("Days held", value=90.0, min_value=0.01)
    days_per_year = col3.number_input("Days per year", value=365.0, min_value=1.0)
    annualized = annualized_effective_rate(holding_period, days_held, days_per_year)
    periods = periods_per_year(days_held, days_per_year)
    annual_col, periods_col = st.columns(2)
    annual_col.metric("Annualized effective rate", f"{annualized:.2%}")
    periods_col.metric("Periods per year", f"{periods:.4f}")
    st.latex(r"Annualized\ Effective\ Rate=(1+HPR)^{365/d}-1")
    st.latex(r"n=\frac{\text{days in year}}{\text{days held}}")
    st.write("Annualizing compounds the observed holding-period return over the number of equivalent holding periods in a year. It enables comparison across investments held for different lengths of time.")

    st.subheader("Effective annual rate from a periodic return")
    periodic_return = st.number_input("Periodic return", value=0.015, format="%.4f")
    effective_rate = effective_annual_rate(periodic_return, periods)
    st.metric("Effective annual rate (EAR)", f"{effective_rate:.2%}")
    st.latex(r"EAR=(1+r_{periodic})^n-1")
    st.write("EAR accounts for intra-year compounding. It is useful when comparing a monthly, quarterly, or short-term quoted rate with an annual investment return on a consistent basis.")

with st.expander("Practical interpretation"):
    st.markdown("**Total return:** combine price change and distributions. **Risk premium:** compare expected compensation with the risk-free alternative. **Annualized return:** compound, rather than simply multiply, a holding-period return.")
    st.markdown("These examples use simplified day-count and distribution assumptions. Production analysis may require taxes, fees, reinvestment assumptions, and an instrument-specific day-count convention.")
