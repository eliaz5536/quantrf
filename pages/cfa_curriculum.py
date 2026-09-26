"""Interactive CFA Quantitative Methods learning page."""

import streamlit as st

from quantitative_methods import (
    annualized_return,
    arithmetic_mean,
    black_scholes_value,
    bond_duration_convexity,
    bond_price,
    continuously_compounded_return,
    dupont_roe,
    geometric_mean_return,
    gordon_growth_value,
    harmonic_mean,
    holding_period_return,
    irr,
    leveraged_return,
    money_weighted_return,
    npv,
    portfolio_metrics,
    real_return,
    time_weighted_return,
    trimmed_mean,
    wacc,
    winsorized_mean,
)


def _numbers(text):
    return [float(value.strip()) for value in text.split(",") if value.strip()]


st.set_page_config(page_title="Rates and Returns", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Rates and Returns")
st.caption("Quantitative Methods | CFA-aligned interactive learning lab")
st.write(
    "Returns translate price changes, income, cash-flow timing, inflation, and financing into comparable performance measures. "
    "Use the calculators below to see how each measure answers a different investment question."
)

st.subheader("Core return measures")
return_tab, average_tab, cash_flow_tab, adjustments_tab = st.tabs(
    ["Holding period", "Averages", "Cash-flow timing", "Adjustments"]
)

with return_tab:
    col1, col2, col3 = st.columns(3)
    beginning = col1.number_input("Beginning value", value=100.0, min_value=0.01)
    ending = col2.number_input("Ending value", value=112.0, min_value=0.0)
    income = col3.number_input("Income received", value=2.0)
    result = holding_period_return(beginning, ending, income)
    st.metric("Holding Period Return", f"{result:.2%}")
    st.latex(r"HPR=\frac{V_1-V_0+I}{V_0}")
    st.info("HPR is the investor's total gain over one holding period, including dividends or coupons. It is useful for comparing a specific trade or investment period.")

with average_tab:
    returns_text = st.text_input("Periodic returns (%)", "10, -5, 8, 12, 4")
    trim = st.slider("Trim / winsorize fraction", 0.0, 0.4, 0.1, 0.05)
    returns = [value / 100 for value in _numbers(returns_text)]
    if returns:
        values = [arithmetic_mean(returns), geometric_mean_return(returns)]
        mean_col, geo_col, harm_col = st.columns(3)
        mean_col.metric("Arithmetic mean", f"{values[0]:.2%}")
        geo_col.metric("Geometric mean", f"{values[1]:.2%}")
        if all(value > 0 for value in returns):
            harm_col.metric("Harmonic mean", f"{harmonic_mean(returns):.2%}")
        st.write(f"Trimmed mean: **{trimmed_mean(returns, trim):.2%}**  |  Winsorized mean: **{winsorized_mean(returns, trim):.2%}**")
    st.latex(r"\bar R=\frac{1}{n}\sum_{i=1}^nR_i\qquad G=\left(\prod_{i=1}^n(1+R_i)\right)^{1/n}-1")
    st.write("Arithmetic mean is useful for one-period expectations. Geometric mean captures compounded realized growth. Harmonic, trimmed, and winsorized means reduce the influence of scale or extreme observations when the data supports them.")

with cash_flow_tab:
    flow_text = st.text_input("Investor cash flows (negative = investment)", "-100, 20, 30, 80")
    flows = _numbers(flow_text)
    periods_text = st.text_input("Periods for cash flows", "0, 1, 2, 3")
    periods = _numbers(periods_text)
    period_returns_text = st.text_input("Subperiod returns (%) for TWR", "5, -2, 8")
    period_returns = [value / 100 for value in _numbers(period_returns_text)]
    try:
        mwrr = money_weighted_return(flows, periods)
        twrr = time_weighted_return(period_returns)
        mw_col, tw_col = st.columns(2)
        mw_col.metric("Money-weighted rate of return", f"{mwrr:.2%}")
        tw_col.metric("Time-weighted rate of return", f"{twrr:.2%}")
    except ValueError as error:
        st.warning(str(error))
    st.latex(r"0=\sum_{t=0}^{T}\frac{CF_t}{(1+MWRR)^{t}}\qquad TWR=\prod_{t=1}^{T}(1+R_t)-1")
    st.write("MWRR is the investor's IRR and reflects the size and timing of deposits and withdrawals. TWR links subperiod returns and is designed to evaluate manager performance independently of external cash flows.")

with adjustments_tab:
    col1, col2 = st.columns(2)
    total_return = col1.number_input("Total holding-period return", value=0.25, format="%.4f")
    years = col2.number_input("Years held", value=3.0, min_value=0.01)
    annual = annualized_return(total_return, years)
    beginning_adjusted = col1.number_input("Beginning value for continuous return", value=100.0, min_value=0.01)
    ending_adjusted = col2.number_input("Ending value for continuous return", value=125.0, min_value=0.01)
    st.metric("Annualized return", f"{annual:.2%}")
    st.metric("Continuously compounded annual return", f"{continuously_compounded_return(beginning_adjusted, ending_adjusted, years):.2%}")
    st.latex(r"R_{annualized}=(1+R_{total})^{1/T}-1\qquad r_c=\frac{\ln(V_T/V_0)}{T}")
    st.write("Annualization makes returns comparable across holding periods. Continuous compounding is convenient in pricing, risk, and log-return models because returns add across time.")

st.subheader("Inflation and financing")
col1, col2, col3 = st.columns(3)
nominal = col1.number_input("Nominal return", value=0.08, format="%.4f")
inflation = col2.number_input("Inflation rate", value=0.03, format="%.4f")
asset = col3.number_input("Asset return", value=0.10, format="%.4f")
leverage = st.slider("Leverage ratio (assets / equity)", 1.0, 5.0, 2.0, 0.25)
borrowing = st.number_input("Borrowing rate", value=0.05, format="%.4f")
real = real_return(nominal, inflation)
levered = leveraged_return(asset, leverage, borrowing)
real_col, lev_col = st.columns(2)
real_col.metric("Real return", f"{real:.2%}")
lev_col.metric("Leveraged return on equity", f"{levered:.2%}")
st.latex(r"R_{real}=\frac{1+R_{nominal}}{1+\pi}-1\qquad R_L=L R_A-(L-1)R_D")
st.write("Real return measures purchasing-power growth after inflation. Leveraged return shows how borrowing magnifies gains and losses after financing costs; it is central to capital structure and risk analysis.")

with st.expander("Formula reference"):
    st.markdown("**Practical rule:** use HPR for one investment, geometric mean for realized multi-period growth, MWRR when cash-flow timing belongs to the investor, and TWR when evaluating an investment manager.")
    st.markdown("These formulas are educational implementations aligned with standard CFA Quantitative Methods terminology; fees, taxes, and day-count conventions may require additional inputs in production analysis.")
