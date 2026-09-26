"""Interactive CFA Derivatives put-call parity and replication page."""

import numpy as np
import pandas as pd
import streamlit as st

from quantitative_methods import (
    call_option_premium_from_parity,
    debtholder_payoff,
    fiduciary_call_value,
    forward_option_put_call_difference,
    insolvent,
    present_value_strike,
    put_option_premium_from_parity,
    shareholder_payoff,
    solvent,
    synthetic_protective_put_value,
)


st.set_page_config(page_title="Option Replication Using Put-Call Parity", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Option Replication Using Put-Call Parity")
st.caption("Derivatives | CFA-aligned interactive learning lab")
st.write(
    "Put-call parity links European call and put premiums to the underlying asset and the present value of the strike. "
    "It is a no-arbitrage relationship that lets investors replicate one position using other instruments."
)

parity_tab, premium_tab, solvency_tab = st.tabs(["Parity and replication", "Premiums and forward parity", "Solvency payoffs"])

with parity_tab:
    st.subheader("Value at inception")
    col1, col2, col3, col4 = st.columns(4)
    spot = col1.number_input("Underlying price", value=100.0, min_value=0.0)
    strike = col2.number_input("Strike price", value=100.0, min_value=0.0)
    rate = col3.number_input("Risk-free rate", value=0.05, format="%.4f")
    years = col4.number_input("Time to expiration", value=1.0, min_value=0.0)
    put_premium = st.number_input("Put premium", value=7.00, min_value=0.0)
    pv_strike = present_value_strike(strike, rate, years)
    fiduciary = fiduciary_call_value(spot - pv_strike + put_premium, strike, rate, years)
    synthetic_put = synthetic_protective_put_value(spot, put_premium)
    fiduciary_col, synthetic_col, pv_col = st.columns(3)
    fiduciary_col.metric("Fiduciary call value", f"{fiduciary:,.2f}")
    synthetic_col.metric("Synthetic protective put value", f"{synthetic_put:,.2f}")
    pv_col.metric("Present value of strike", f"{pv_strike:,.2f}")
    st.latex(r"C+PV(K)=S_0+P")
    st.latex(r"Fiduciary\ Call=C+PV(K)\qquad Protective\ Put=S_0+P")
    st.write("A fiduciary call combines a call with risk-free borrowing to fund the strike. A synthetic protective put combines the underlying asset with a put. Put-call parity says both packages have the same value at inception when the options share strike and expiration.")

with premium_tab:
    st.subheader("Call and put option premiums")
    col1, col2, col3 = st.columns(3)
    call_input = col1.number_input("Observed call premium", value=12.00, min_value=0.0)
    put_input = col2.number_input("Observed put premium", value=7.00, min_value=0.0)
    dividend_value = col3.number_input("Present value of dividends", value=0.0, min_value=0.0)
    implied_call = call_option_premium_from_parity(spot, put_input, strike, rate, years, dividend_value)
    implied_put = put_option_premium_from_parity(spot, call_input, strike, rate, years, dividend_value)
    call_col, put_col = st.columns(2)
    call_col.metric("Call premium from parity", f"{implied_call:,.2f}")
    put_col.metric("Put premium from parity", f"{implied_put:,.2f}")
    st.latex(r"C=S_0-PV(Dividends)+P-PV(K)")
    st.latex(r"P=C-S_0+PV(Dividends)+PV(K)")
    st.write("If an observed option premium differs materially from its parity-implied value after transaction costs, the difference may indicate an arbitrage opportunity or reflect dividends, exercise style, funding, or market frictions.")

    st.subheader("Put-call parity for options on a forward contract")
    forward_price = st.number_input("Forward price", value=102.0, min_value=0.0)
    forward_difference = forward_option_put_call_difference(forward_price, strike, rate, years)
    st.metric("Call premium minus put premium", f"{forward_difference:,.2f}")
    st.latex(r"C_{forward}-P_{forward}=DF\times(F_0-K)=\frac{F_0-K}{(1+r)^T}")
    st.write("For options written on a forward, the underlying value is replaced by the forward price and the difference between call and put premiums is discounted. This relationship is useful for checking consistency across forward and option markets.")

with solvency_tab:
    st.subheader("Solvent and insolvent firm payoffs")
    col1, col2 = st.columns(2)
    asset_value = col1.number_input("Firm asset value at debt maturity", value=120.0, min_value=0.0)
    debt_face = col2.number_input("Debt face value", value=100.0, min_value=0.0)
    debt_payoff = debtholder_payoff(asset_value, debt_face)
    equity_payoff = shareholder_payoff(asset_value, debt_face)
    status = "Solvent" if solvent(asset_value, debt_face) else "Insolvent"
    status_col, debt_col, equity_col = st.columns(3)
    status_col.metric("Firm status", status)
    debt_col.metric("Debtholder payoff", f"{debt_payoff:,.2f}")
    equity_col.metric("Shareholder payoff", f"{equity_payoff:,.2f}")
    st.latex(r"Debtholder\ Payoff=min(V_T, D)\qquad Shareholder\ Payoff=max(V_T-D,0)")
    st.write("A solvent firm has assets at least equal to debt, so debtholders receive the promised amount and shareholders receive the residual. An insolvent firm has limited liability: debtholders receive the available asset value and shareholders receive zero.")

    asset_values = np.linspace(0.0, max(debt_face * 2, 1.0), 101)
    payoff_profile = pd.DataFrame(
        {
            "Debtholder": [debtholder_payoff(value, debt_face) for value in asset_values],
            "Shareholder": [shareholder_payoff(value, debt_face) for value in asset_values],
        },
        index=asset_values,
    )
    payoff_profile.index.name = "Firm asset value at maturity"
    st.line_chart(payoff_profile)
    st.caption("The shareholder payoff resembles a call option on firm assets with debt as the strike; risky debt is the residual claim after that option value is separated.")
    st.write(f"At the selected asset value, the insolvent flag is **{insolvent(asset_value, debt_face)}**.")

with st.expander("Practical interpretation"):
    st.markdown("**Put-call parity** is a no-arbitrage test and a replication tool. **Fiduciary calls** and **protective puts** show how combinations of debt, stock, calls, and puts can create equivalent payoffs.")
    st.markdown("The solvency example connects corporate securities to options: equity is a call option on the firm's assets with debt as the strike, while debtholders bear the short-put-like downside created by default risk.")
