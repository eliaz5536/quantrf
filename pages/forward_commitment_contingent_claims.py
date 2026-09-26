"""Interactive CFA Derivatives forward and contingent-claim page."""

import numpy as np
import pandas as pd
import streamlit as st

from quantitative_methods import (
    call_option_payoff,
    long_forward_payoff,
    mark_to_market_change,
    netting,
    payoff_at_maturity,
    put_option_payoff,
    settlement_amount,
    short_forward_payoff,
)


st.set_page_config(page_title="Forward Commitment and Contingent Claim Features and Instruments", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Forward Commitment and Contingent Claim Features and Instruments")
st.caption("Derivatives | CFA-aligned interactive learning lab")
st.write(
    "Forward commitments create obligations for both parties, while contingent claims create rights whose payoff depends on a future state. "
    "The calculators below make the payoff, marking, settlement, and netting mechanics explicit."
)

forward_tab, settlement_tab, option_tab = st.tabs(["Forward commitments", "MTM and settlement", "Contingent claims"])

with forward_tab:
    st.subheader("Payoff at maturity")
    col1, col2, col3 = st.columns(3)
    spot_at_maturity = col1.number_input("Underlying price at maturity", value=110.0, min_value=0.0)
    delivery_price = col2.number_input("Delivery price", value=100.0, min_value=0.0)
    position = col3.selectbox("Forward position", ["long", "short"])
    payoff = payoff_at_maturity(spot_at_maturity, delivery_price, position)
    st.metric("Payoff at maturity", f"{payoff:,.2f}")
    st.latex(r"Payoff_{long}=S_T-K\qquad Payoff_{short}=K-S_T")
    st.write("A long forward benefits when the underlying finishes above the agreed delivery price. A short forward benefits when it finishes below that price. The payoff is linear and the initial value of a fairly priced forward is approximately zero.")

    prices = np.linspace(max(0.0, delivery_price * 0.5), delivery_price * 1.5, 101)
    profile = pd.DataFrame(
        {
            "Long forward": [long_forward_payoff(price, delivery_price) for price in prices],
            "Short forward": [short_forward_payoff(price, delivery_price) for price in prices],
        },
        index=prices,
    )
    profile.index.name = "Underlying price at maturity"
    st.line_chart(profile)
    st.caption("The payoff profile crosses zero at the delivery price and has equal and opposite long/short outcomes.")

with settlement_tab:
    st.subheader("Mark-to-market change")
    col1, col2, col3 = st.columns(3)
    previous_forward = col1.number_input("Previous forward price", value=100.0, min_value=0.0)
    current_forward = col2.number_input("Current forward price", value=103.0, min_value=0.0)
    mtm_position = col3.selectbox("MTM position", ["long", "short"])
    mtm = mark_to_market_change(previous_forward, current_forward, mtm_position)
    st.metric("Mark-to-market change per unit", f"{mtm:,.2f}")
    st.latex(r"\Delta MTM_{long}=F_t-F_{t-1}\qquad \Delta MTM_{short}=F_{t-1}-F_t")
    st.write("Mark-to-market measures the change in contract value since the last valuation. Futures commonly settle this change daily; OTC forwards may settle at maturity or under an agreed collateral arrangement.")

    st.subheader("Settlements and netting")
    settlement_col1, settlement_col2, settlement_col3 = st.columns(3)
    per_unit = settlement_col1.number_input("Per-unit settlement", value=3.0)
    contract_size = settlement_col2.number_input("Units per contract", value=100.0, min_value=0.0)
    contracts = settlement_col3.number_input("Number of contracts", value=2.0, min_value=0.0)
    settlement = settlement_amount(per_unit, contract_size, contracts)
    settlement_col = st.columns(2)
    settlement_col[0].metric("Gross settlement", f"{settlement:,.2f}")
    netting_text = st.text_input("Settlement amounts to net", "600, -150, 75")
    settlements = [float(value.strip()) for value in netting_text.split(",") if value.strip()]
    settlement_col[1].metric("Net settlement", f"{netting(settlements):,.2f}")
    st.latex(r"Settlement=Payoff_{per\ unit}\times Contract\ Size\times Number\ of\ Contracts")
    st.latex(r"Net\ Settlement=\sum_{i=1}^{n}Settlement_i")
    st.write("Settlement converts a per-unit derivative payoff into a cash amount. Netting offsets payable and receivable positions, reducing the number and size of cash transfers when contracts share a legal netting agreement.")

with option_tab:
    st.subheader("Call and put payoff profiles")
    col1, col2 = st.columns(2)
    option_strike = col1.number_input("Option strike price", value=100.0, min_value=0.0)
    expiry_price = col2.number_input("Underlying price at expiry", value=110.0, min_value=0.0)
    long_call = call_option_payoff(expiry_price, option_strike, "long")
    short_call = call_option_payoff(expiry_price, option_strike, "short")
    long_put = put_option_payoff(expiry_price, option_strike, "long")
    short_put = put_option_payoff(expiry_price, option_strike, "short")
    call_col, put_col = st.columns(2)
    call_col.metric("Long call payoff", f"{long_call:,.2f}")
    call_col.metric("Short call payoff", f"{short_call:,.2f}")
    put_col.metric("Long put payoff", f"{long_put:,.2f}")
    put_col.metric("Short put payoff", f"{short_put:,.2f}")
    st.latex(r"Payoff_{long\ call}=max(S_T-K,0)\qquad Payoff_{short\ call}=-max(S_T-K,0)")
    st.latex(r"Payoff_{long\ put}=max(K-S_T,0)\qquad Payoff_{short\ put}=-max(K-S_T,0)")
    st.write("A call gives the long holder the right to buy at the strike; a put gives the right to sell. Unlike a forward, the long option holder can choose not to exercise, so the payoff cannot be below zero before the premium is considered.")

    option_prices = np.linspace(max(0.0, option_strike * 0.5), option_strike * 1.5, 101)
    option_profile = pd.DataFrame(
        {
            "Long call": [call_option_payoff(price, option_strike, "long") for price in option_prices],
            "Long put": [put_option_payoff(price, option_strike, "long") for price in option_prices],
        },
        index=option_prices,
    )
    option_profile.index.name = "Underlying price at expiry"
    st.line_chart(option_profile)
    st.caption("The graph shows intrinsic payoff only; option premiums are excluded and would shift the long-holder profit profile downward.")

with st.expander("Practical interpretation"):
    st.markdown("**Forward commitments** are obligations with symmetric, linear payoffs. **Contingent claims** give one party a right, not an obligation, creating asymmetric payoff profiles. **Settlement and netting** determine how those economic outcomes become cash transfers.")
    st.markdown("These are payoff calculations rather than full derivative prices. Premiums, discounting, collateral, margin, credit support, and transaction costs may be needed for valuation and trading analysis.")
