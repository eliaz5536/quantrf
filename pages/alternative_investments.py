"""Interactive CFA Alternative Investments GP/LP waterfall page."""

import pandas as pd
import streamlit as st

from quantitative_methods import (
    gp_catch_up_clause,
    gp_rate_of_return,
    lp_distribution,
    lp_preferred_return,
    private_equity_waterfall,
)


st.set_page_config(page_title="Alternative Investments, Features, Methods and Structures", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Alternative Investments, Features, Methods and Structures")
st.caption("Alternative Investments | CFA-aligned interactive learning lab")
st.write(
    "Private-equity and alternative-investment waterfalls determine how proceeds move between limited partners (LPs) and general partners (GPs). "
    "This calculator shows the distribution tiers and how carried interest affects the GP's return."
)

st.subheader("GP/LP waterfall inputs")
col1, col2, col3 = st.columns(3)
lp_contribution = col1.number_input("LP contribution", value=1000.0, min_value=0.0)
total_distributable = col2.number_input("Total distributable proceeds", value=1400.0, min_value=0.0)
gp_contribution = col3.number_input("GP contribution", value=50.0, min_value=0.01)
col4, col5, col6 = st.columns(3)
preferred_rate = col4.number_input("LP preferred return rate", value=0.08, min_value=0.0, format="%.4f")
years = col5.number_input("Investment years", value=3.0, min_value=0.01)
carried_interest = col6.number_input("GP carried interest", value=0.20, min_value=0.0, max_value=0.99, format="%.4f")

preferred_return = lp_preferred_return(lp_contribution, preferred_rate, years)
catch_up = gp_catch_up_clause(preferred_return, carried_interest)
waterfall = private_equity_waterfall(total_distributable, lp_contribution, preferred_return, carried_interest)
gp_return = gp_rate_of_return(waterfall["gp_total_distribution"], gp_contribution, years)

st.subheader("Distribution waterfall")
capital_col, pref_col, catch_col, residual_col = st.columns(4)
capital_col.metric("1. LP capital returned", f"${waterfall['lp_capital_return']:,.2f}")
pref_col.metric("2. LP preferred return", f"${waterfall['lp_preferred_return']:,.2f}")
catch_col.metric("3. GP catch-up", f"${waterfall['gp_catch_up']:,.2f}")
residual_col.metric("4. Residual proceeds", f"${waterfall['lp_residual'] + waterfall['gp_residual']:,.2f}")

st.dataframe(
    pd.DataFrame(
        {
            "Recipient": ["LP", "GP"],
            "Total distribution": [waterfall["lp_total_distribution"], waterfall["gp_total_distribution"]],
            "Share of proceeds": [
                waterfall["lp_total_distribution"] / total_distributable if total_distributable else 0.0,
                waterfall["gp_total_distribution"] / total_distributable if total_distributable else 0.0,
            ],
        }
    ).style.format({"Total distribution": "${:,.2f}", "Share of proceeds": "{:.2%}"}),
    hide_index=True,
)

st.latex(r"LP\ Preferred\ Return=LP\ Contribution[(1+h)^T-1]")
st.latex(r"GP\ Catch\text{-}up=\frac{Carry}{1-Carry}\times LP\ Preferred\ Return")
st.latex(r"Residual\ Split: LP=(1-Carry)\times Residual,\quad GP=Carry\times Residual")
st.write("The waterfall first returns LP capital, then pays the LP hurdle or preferred return. The GP catch-up gives the GP distributions until the agreed carried-interest economics are reached; remaining proceeds are split according to the carry rate.")

st.subheader("Key GP and LP metrics")
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("LP total distribution", f"${waterfall['lp_total_distribution']:,.2f}")
metric_col2.metric("GP total distribution", f"${waterfall['gp_total_distribution']:,.2f}")
metric_col3.metric("GP annualized rate of return", f"{gp_return:.2%}")
st.latex(r"GP\ Rate\ of\ Return=\left(\frac{GP\ Proceeds}{GP\ Contribution}\right)^{1/T}-1")
st.write("The GP's return can be much higher than the LP's percentage return when the GP contributes relatively little capital but earns carried interest. This is why the waterfall and the GP commitment must be analyzed together.")

with st.expander("Practical interpretation"):
    st.markdown("**LP:** supplies most of the capital and generally receives capital back plus a preferred return before residual sharing. **GP:** manages the investment, may contribute capital, and earns carried interest after the catch-up tier.")
    st.markdown("This is a simplified educational waterfall. Real agreements may include management fees, return-of-capital definitions, European or American waterfalls, clawbacks, deal-by-deal carry, and hurdle compounding conventions.")
