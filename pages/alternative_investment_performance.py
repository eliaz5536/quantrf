"""Interactive CFA Alternative Investments performance page."""

import streamlit as st

from quantitative_methods import (
    gp_rate_of_return,
    leveraged_rate_of_return,
    money_weighted_return,
    multiple_of_invested_capital,
    return_to_investors,
)


def _numbers(text):
    return [float(value.strip()) for value in text.split(",") if value.strip()]


st.set_page_config(page_title="Alternative Investment Performance and Returns", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Alternative Investment Performance and Returns")
st.caption("Alternative Investments | CFA-aligned interactive learning lab")
st.write(
    "Alternative-investment performance should be evaluated using both cash-flow timing and total value multiples. "
    "IRR captures timing, MOIC captures total capital returned, and leverage and carried interest explain how sponsor and investor outcomes differ."
)

performance_tab, leverage_tab, sponsor_tab = st.tabs(["IRR and MOIC", "Leveraged return", "GP and investor return"])

with performance_tab:
    st.subheader("Internal rate of return")
    cash_flow_text = st.text_input("Investment cash flows by period (negative = contribution)", "-1000, 0, 0, 1400")
    period_text = st.text_input("Cash-flow periods", "0, 1, 2, 3")
    cash_flows = _numbers(cash_flow_text)
    periods = _numbers(period_text)
    try:
        irr_value = money_weighted_return(cash_flows, periods)
        invested = abs(sum(value for value in cash_flows if value < 0))
        distributions = sum(value for value in cash_flows if value > 0)
        moic = multiple_of_invested_capital(distributions, invested)
        investor_return = return_to_investors(distributions, invested)
        irr_col, moic_col, return_col = st.columns(3)
        irr_col.metric("Internal rate of return", f"{irr_value:.2%}")
        moic_col.metric("MOIC", f"{moic:.2f}x")
        return_col.metric("Return to investors", f"{investor_return:.2%}")
        st.latex(r"0=\sum_{t=0}^{T}\frac{CF_t}{(1+IRR)^t}")
        st.latex(r"MOIC=\frac{Total\ Distributions}{Invested\ Capital}\qquad Return\ to\ Investors=MOIC-1")
        st.write("IRR is the discount rate that sets the net present value of the investment cash flows to zero, so it reflects the timing of contributions and distributions. MOIC ignores timing and reports how many times invested capital was returned.")
    except ValueError as error:
        st.warning(str(error))

with leverage_tab:
    st.subheader("Leveraged rate of return")
    col1, col2, col3 = st.columns(3)
    asset_return = col1.number_input("Underlying asset return", value=0.15, format="%.4f")
    leverage = col2.number_input("Leverage ratio", value=2.0, min_value=0.01, format="%.4f")
    borrowing_rate = col3.number_input("Borrowing rate", value=0.06, format="%.4f")
    leveraged_return_value = leveraged_rate_of_return(asset_return, leverage, borrowing_rate)
    st.metric("Leveraged rate of return", f"{leveraged_return_value:.2%}")
    st.latex(r"r_L=Lr_A-(L-1)r_D")
    st.write("The leveraged return on equity magnifies the asset return when the asset earns more than the borrowing cost, but leverage also magnifies losses. This is why an attractive unleveraged investment can become risky when financed aggressively.")

with sponsor_tab:
    st.subheader("GP return")
    col1, col2, col3 = st.columns(3)
    gp_proceeds = col1.number_input("GP proceeds", value=80.0, min_value=0.0)
    gp_contribution = col2.number_input("GP contribution", value=50.0, min_value=0.01)
    investment_years = col3.number_input("Investment years", value=3.0, min_value=0.01)
    gp_return = gp_rate_of_return(gp_proceeds, gp_contribution, investment_years)
    st.metric("GP annualized rate of return", f"{gp_return:.2%}")
    st.latex(r"r_{GP}=\left(\frac{GP\ Proceeds}{GP\ Contribution}\right)^{1/T}-1")
    st.write("GP return reflects both the GP's invested capital and performance-based proceeds such as carried interest. A GP can show a high return on a relatively small commitment even when LPs provide most of the fund capital.")

    investor_distributions = st.number_input("Investor distributions", value=1400.0, min_value=0.0)
    investor_contribution = st.number_input("Investor invested capital", value=1000.0, min_value=0.01)
    investor_moic = multiple_of_invested_capital(investor_distributions, investor_contribution)
    investor_total_return = return_to_investors(investor_distributions, investor_contribution)
    investor_moic_col, investor_return_col = st.columns(2)
    investor_moic_col.metric("Investor MOIC", f"{investor_moic:.2f}x")
    investor_return_col.metric("Investor total return", f"{investor_total_return:.2%}")
    st.write("Return to investors measures the gain relative to capital invested after considering the distributions they actually receive. Compare it with IRR when the timing of those distributions matters.")

with st.expander("Practical interpretation"):
    st.markdown("**IRR** is timing-sensitive. **MOIC** is a simple value multiple. **Leveraged return** isolates the effect of financing. **GP return** reflects sponsor economics, while **return to investors** reflects the cash actually delivered to capital providers.")
    st.markdown("These are educational calculations. Real funds may require fee deductions, interim cash flows, clawbacks, subscription lines, preferred returns, carried-interest waterfalls, and cash-flow-specific IRR conventions.")
