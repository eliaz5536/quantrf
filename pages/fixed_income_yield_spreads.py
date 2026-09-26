"""Interactive CFA Fixed Income yield and spread measures page."""

import streamlit as st

from quantitative_methods import (
    annual_compounding,
    compounded_value,
    current_yield,
    g_spread,
    i_spread,
    monthly_compounding,
    option_adjusted_spread,
    periodicity_conversion,
    quarterly_compounding,
    semiannual_compounding,
    simple_yield,
    yield_to_call,
    yield_to_maturity,
    yield_to_worst,
    z_spread,
)


def _numbers(text, scale=1.0):
    return [float(value.strip()) * scale for value in text.split(",") if value.strip()]


st.set_page_config(page_title="Yield and Yield Spread Measures for Fixed-Rate Bonds", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Yield and Yield Spread Measures for Fixed-Rate Bonds")
st.caption("Fixed Income | CFA-aligned interactive learning lab")
st.write(
    "Bond yields depend on price, cash-flow timing, and compounding convention. "
    "Spread measures then separate the bond's compensation into benchmark, curve, credit, liquidity, and embedded-option effects."
)

periodicity_tab, yield_tab, spread_tab = st.tabs(["Periodicity and compounding", "Bond yield measures", "Yield spreads"])

with periodicity_tab:
    st.subheader("Annual, semiannual, quarterly, and monthly compounding")
    col1, col2, col3 = st.columns(3)
    principal = col1.number_input("Principal", value=1000.0, min_value=0.0)
    annual_rate = col2.number_input("Quoted annual rate", value=0.06, format="%.4f")
    years = col3.number_input("Years", value=3.0, min_value=0.0)
    annual_value = annual_compounding(principal, annual_rate, years)
    semiannual_value = semiannual_compounding(principal, annual_rate, years)
    quarterly_value = quarterly_compounding(principal, annual_rate, years)
    monthly_value = monthly_compounding(principal, annual_rate, years)
    annual_col, semi_col, quarter_col, month_col = st.columns(4)
    annual_col.metric("Annual", f"{annual_value:,.2f}")
    semi_col.metric("Semiannual", f"{semiannual_value:,.2f}")
    quarter_col.metric("Quarterly", f"{quarterly_value:,.2f}")
    month_col.metric("Monthly", f"{monthly_value:,.2f}")
    st.latex(r"FV=P\left(1+\frac{r_{nom}}{m}\right)^{mT}")
    st.write("The periodicity m is 1 for annual, 2 for semiannual, 4 for quarterly, and 12 for monthly compounding. More frequent compounding produces a higher effective return for the same quoted nominal rate.")

    st.subheader("Periodicity conversions")
    conversion_col1, conversion_col2, conversion_col3 = st.columns(3)
    from_periods = conversion_col1.selectbox("Convert from periods per year", [1, 2, 4, 12], index=1)
    to_periods = conversion_col2.selectbox("Convert to periods per year", [1, 2, 4, 12], index=3)
    converted_rate = periodicity_conversion(annual_rate, from_periods, to_periods)
    conversion_col3.metric("Equivalent nominal rate", f"{converted_rate:.4%}")
    st.latex(r"(1+r_m/m)^m=(1+r_n/n)^n")
    st.write("Periodicity conversion preserves the same effective annual value while changing the nominal quote. Always identify both the annual rate convention and the compounding frequency when comparing bonds.")

with yield_tab:
    st.subheader("Simple yield, current yield, and YTM")
    col1, col2, col3 = st.columns(3)
    face_value = col1.number_input("Face value", value=1000.0, min_value=0.01)
    coupon_rate = col2.number_input("Annual coupon rate", value=0.06, format="%.4f")
    bond_price = col3.number_input("Bond price", value=980.0, min_value=0.01)
    maturity = st.number_input("Years to maturity", value=5.0, min_value=0.01)
    frequency = st.selectbox("Coupon frequency", [1, 2, 4, 12], index=1)
    simple = simple_yield(face_value, coupon_rate, bond_price, maturity)
    current = current_yield(face_value, coupon_rate, bond_price)
    ytm = yield_to_maturity(bond_price, face_value, coupon_rate, maturity, frequency)
    simple_col, current_col, ytm_col = st.columns(3)
    simple_col.metric("Simple yield", f"{simple:.2%}")
    current_col.metric("Current yield", f"{current:.2%}")
    ytm_col.metric("Yield to maturity", f"{ytm:.2%}")
    st.latex(r"Simple\ Yield=\frac{C+(FV-P)/T}{P}\qquad Current\ Yield=\frac{C}{P}")
    st.latex(r"P=\sum_{t=1}^{N}\frac{C/m}{(1+YTM/m)^t}+\frac{FV}{(1+YTM/m)^N}")
    st.write("Simple yield approximates annualized return using coupon income and straight-line price change. Current yield uses only the annual coupon. YTM is the internal rate that discounts every promised cash flow and accounts for compounding and pull to par.")

    st.subheader("YTC and YTW for a callable bond")
    call_price = st.number_input("Call price", value=1020.0, min_value=0.01)
    years_to_call = st.number_input("Years to call", value=3.0, min_value=0.01)
    ytc = yield_to_call(bond_price, face_value, coupon_rate, call_price, years_to_call, frequency)
    ytw = yield_to_worst(bond_price, face_value, coupon_rate, maturity, [(call_price, years_to_call)], frequency)
    ytc_col, ytw_col = st.columns(2)
    ytc_col.metric("Yield to call", f"{ytc:.2%}")
    ytw_col.metric("Yield to worst", f"{ytw:.2%}")
    st.latex(r"YTC: P=\sum_{t=1}^{N_c}\frac{C/m}{(1+YTC/m)^t}+\frac{Call\ Price}{(1+YTC/m)^{N_c}}")
    st.write("YTC replaces maturity redemption with the call price and call date while retaining the original coupon. YTW is the lowest yield among the relevant redemption scenarios, so it is a conservative return measure for a callable bond.")

with spread_tab:
    st.subheader("G-spread and I-spread")
    col1, col2, col3 = st.columns(3)
    bond_yield = col1.number_input("Bond yield", value=0.065, format="%.4f")
    government_yield = col2.number_input("Government benchmark yield", value=0.045, format="%.4f")
    swap_rate = col3.number_input("Matched-maturity swap rate", value=0.050, format="%.4f")
    g_value = g_spread(bond_yield, government_yield)
    i_value = i_spread(bond_yield, swap_rate)
    g_col, i_col = st.columns(2)
    g_col.metric("G-spread", f"{g_value:.2%}")
    i_col.metric("I-spread", f"{i_value:.2%}")
    st.latex(r"G\text{-}spread=Y_{bond}-Y_{government}\qquad I\text{-}spread=Y_{bond}-Y_{swap}")
    st.write("The G-spread compares a bond yield with a government benchmark at a similar maturity. The I-spread compares it with the interpolated swap curve and is common in interest-rate and credit analysis.")

    st.subheader("Z-spread")
    z_price = st.number_input("Bond price for Z-spread", value=980.0, min_value=0.01)
    cash_flows_text = st.text_input("Bond cash flows by period", "30, 30, 30, 30, 1030")
    spot_rates_text = st.text_input("Spot rates by period", "0.045, 0.047, 0.049, 0.051, 0.053")
    periods_text = st.text_input("Periods in years", "1, 2, 3, 4, 5")
    cash_flows = _numbers(cash_flows_text)
    spot_rates = _numbers(spot_rates_text)
    periods_input = _numbers(periods_text)
    if len(cash_flows) == len(spot_rates) == len(periods_input) and cash_flows:
        z_value = z_spread(z_price, cash_flows, spot_rates, periods_input)
        st.metric("Z-spread", f"{z_value:.2%}")
        st.latex(r"P=\sum_{t=1}^{N}\frac{CF_t}{(1+s_t+Z)^t}")
        st.write("The Z-spread is the constant spread added to every spot rate that makes the discounted cash flows equal the observed bond price. It incorporates credit, liquidity, and other non-government compensation before separating embedded-option effects.")
    else:
        st.warning("Enter matching non-empty lists for cash flows, spot rates, and periods.")

    st.subheader("Option-adjusted spread")
    z_input = st.number_input("Z-spread estimate", value=0.02, format="%.4f")
    option_value = st.number_input("Embedded option value", value=12.0, min_value=0.0)
    effective_duration = st.number_input("Effective duration", value=4.5, min_value=0.01)
    oas = option_adjusted_spread(z_input, option_value, z_price, effective_duration)
    st.metric("Approximate OAS", f"{oas:.2%}")
    st.latex(r"OAS\approx Z\text{-}spread-\frac{Option\ Value}{Price\times Effective\ Duration}")
    st.write("OAS removes the estimated value of an embedded call or put from the Z-spread. The displayed calculation is a duration-based approximation; production OAS is normally obtained from a rate-tree or option-pricing model.")

with st.expander("Practical interpretation"):
    st.markdown("**Yield measures** describe a bond's return under a cash-flow scenario. **Spread measures** compare that return with a benchmark or curve to diagnose relative value and compensation for risk.")
    st.markdown("These are educational calculations aligned with standard CFA Fixed Income terminology. Day-count conventions, settlement dates, accrued interest, and curve construction can materially affect production bond analytics.")
