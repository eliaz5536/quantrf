"""Interactive CFA Quantitative Methods time value of money page."""

import streamlit as st

from quantitative_methods import (
    annuity_payment_from_future_value,
    annuity_payment_from_present_value,
    cash_flow_additivity,
    constant_dividend_value,
    constant_growth_dividend_value,
    constant_growth_implied_return,
    coupon_bond_price,
    coupon_bond_yield,
    dividend_payout_ratio,
    future_value,
    implied_discount_bond_return,
    mortgage_payment,
    ordinary_annuity_future_value,
    ordinary_annuity_present_value,
    pe_ratio,
    perpetual_bond_price,
    present_value,
    two_stage_dividend_value,
    zero_coupon_bond_price,
)


def _numbers(text):
    return [float(value.strip()) for value in text.split(",") if value.strip()]


st.set_page_config(page_title="Time Value of Money in Finance", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Time Value of Money in Finance")
st.caption("Quantitative Methods | CFA-aligned interactive learning lab")
st.write(
    "A dollar received today can be invested, while a dollar received later carries uncertainty and opportunity cost. "
    "These calculators discount and compound cash flows so that investments, bonds, loans, and stocks can be compared on one valuation date."
)

core_tab, bond_tab, annuity_tab, equity_tab = st.tabs(
    ["Core TVM", "Bonds", "Annuities and mortgages", "Equity and ratios"]
)

with core_tab:
    st.subheader("Future value and present value")
    col1, col2, col3 = st.columns(3)
    present = col1.number_input("Present value", value=1000.0, min_value=0.0)
    rate = col2.number_input("Periodic interest rate", value=0.05, format="%.4f")
    periods = col3.number_input("Number of periods", value=5.0, min_value=0.0)
    future = future_value(present, rate, periods)
    future_input = st.number_input("Future value to discount", value=1276.28, min_value=0.0)
    pv = present_value(future_input, rate, periods)
    future_col, pv_col = st.columns(2)
    future_col.metric("Future value", f"{future:,.2f}")
    pv_col.metric("Present value", f"{pv:,.2f}")
    st.latex(r"FV=PV(1+r)^n\qquad PV=\frac{FV}{(1+r)^n}")
    st.info("Compounding answers what a current amount becomes. Discounting answers what a future amount is worth today. The same rate and period convention must be used for both.")

    st.subheader("Cash-flow additivity")
    flow_text = st.text_input("Cash flows by period", "100, 100, 1100")
    additivity_flows = _numbers(flow_text)
    if additivity_flows:
        combined_pv = cash_flow_additivity(additivity_flows, rate)
        individual_pv = sum(present_value(amount, rate, period) for period, amount in enumerate(additivity_flows))
        st.metric("Present value of the cash-flow stream", f"{combined_pv:,.2f}")
        st.write(f"Sum of individual present values: **{individual_pv:,.2f}**")
        st.latex(r"PV(CF_1+CF_2+\cdots)=PV(CF_1)+PV(CF_2)+\cdots")
        st.write("Cash-flow additivity makes project and security valuation modular: value each dated cash flow separately, then add the present values.")

with bond_tab:
    st.subheader("Discount and coupon bonds")
    col1, col2, col3 = st.columns(3)
    face = col1.number_input("Face value", value=1000.0, min_value=0.01)
    bond_yield = col2.number_input("Yield per year", value=0.05, format="%.4f")
    bond_years = col3.number_input("Years to maturity", value=5.0, min_value=0.01)
    frequency = st.selectbox("Coupon payments per year", [1, 2, 4, 12], index=1)
    coupon_rate = st.number_input("Coupon rate", value=0.06, format="%.4f")
    zero_price = zero_coupon_bond_price(face, bond_yield, bond_years, frequency=1)
    coupon_price = coupon_bond_price(face, coupon_rate, bond_yield, bond_years, frequency=frequency)
    zero_col, coupon_col = st.columns(2)
    zero_col.metric("Zero-coupon bond price", f"{zero_price:,.2f}")
    coupon_col.metric("Coupon bond price", f"{coupon_price:,.2f}")
    st.latex(r"P_{zero}=\frac{FV}{(1+y)^T}\qquad P_{coupon}=\sum_{t=1}^{N}\frac{C/m}{(1+y/m)^t}+\frac{FV}{(1+y/m)^N}")
    st.write("A zero-coupon bond has one payment, so its price is a single discounted cash flow. A coupon bond combines discounted coupons and principal; price moves inversely with yield.")

    st.subheader("Perpetual bond and implied returns")
    perpetuity_coupon = st.number_input("Perpetual annual coupon", value=60.0, min_value=0.0)
    perpetual_price = perpetual_bond_price(perpetuity_coupon, bond_yield)
    discount_price = st.number_input("Discount bond market price", value=800.0, min_value=0.01)
    discount_return = implied_discount_bond_return(discount_price, face, bond_years)
    perpetuity_col, discount_col = st.columns(2)
    perpetuity_col.metric("Perpetual bond price", f"{perpetual_price:,.2f}")
    discount_col.metric("Implied annualized return", f"{discount_return:.2%}")
    st.latex(r"P_{perpetual}=\frac{C}{y}\qquad y_{discount}=\left(\frac{FV}{P}\right)^{1/T}-1")
    st.write("A perpetuity has no maturity, so its value is the level payment divided by the required return. The discount-bond return converts price appreciation into an annualized yield.")

    st.subheader("Yield to maturity from a coupon bond price")
    market_price = st.number_input("Coupon bond market price", value=1040.0, min_value=0.01)
    ytm = coupon_bond_yield(market_price, face, coupon_rate, bond_years, frequency)
    st.metric("Solved yield to maturity", f"{ytm:.2%}")
    st.latex(r"P=\sum_{t=1}^{N}\frac{C/m}{(1+YTM/m)^t}+\frac{FV}{(1+YTM/m)^N}")
    st.write("YTM is the discount rate that equates the bond's observed price with the present value of every promised cash flow, assuming the bond is held to maturity and coupons are reinvested at that rate.")

with annuity_tab:
    st.subheader("Ordinary annuity and periodic payment")
    col1, col2, col3 = st.columns(3)
    payment = col1.number_input("Periodic payment", value=250.0, min_value=0.0)
    annuity_rate = col2.number_input("Periodic annuity rate", value=0.04, format="%.4f")
    annuity_periods = col3.number_input("Annuity periods", value=10.0, min_value=1.0)
    annuity_pv = ordinary_annuity_present_value(payment, annuity_rate, annuity_periods)
    annuity_fv = ordinary_annuity_future_value(payment, annuity_rate, annuity_periods)
    pv_col, fv_col = st.columns(2)
    pv_col.metric("PV of ordinary annuity", f"{annuity_pv:,.2f}")
    fv_col.metric("FV of ordinary annuity", f"{annuity_fv:,.2f}")
    st.latex(r"PV_{annuity}=PMT\left[\frac{1-(1+r)^{-n}}{r}\right]\qquad FV_{annuity}=PMT\left[\frac{(1+r)^n-1}{r}\right]")
    st.write("An ordinary annuity pays at the end of each period. Its PV supports valuation of leases and loans; its FV supports savings and retirement accumulation plans.")

    target_pv = st.number_input("Present value to amortize", value=10000.0, min_value=0.0)
    target_fv = st.number_input("Future savings target", value=15000.0, min_value=0.0)
    pv_payment = annuity_payment_from_present_value(target_pv, annuity_rate, annuity_periods)
    fv_payment = annuity_payment_from_future_value(target_fv, annuity_rate, annuity_periods)
    payment_col, savings_col = st.columns(2)
    payment_col.metric("Periodic payment for present value", f"{pv_payment:,.2f}")
    savings_col.metric("Periodic payment for future target", f"{fv_payment:,.2f}")
    st.latex(r"PMT_{PV}=\frac{PV\,r}{1-(1+r)^{-n}}\qquad PMT_{FV}=\frac{FV\,r}{(1+r)^n-1}")
    st.write("These inverse annuity formulas solve for the recurring deposit or repayment required to reach a target value.")

    st.subheader("Fully amortizing mortgage")
    mortgage_principal = st.number_input("Mortgage principal", value=300000.0, min_value=0.01)
    mortgage_rate = st.number_input("Mortgage periodic rate", value=0.005, format="%.5f")
    mortgage_periods = st.number_input("Mortgage payment periods", value=360.0, min_value=1.0)
    mortgage_pmt = mortgage_payment(mortgage_principal, mortgage_rate, mortgage_periods)
    st.metric("Periodic mortgage payment", f"{mortgage_pmt:,.2f}")
    st.latex(r"PMT=PV\frac{r(1+r)^n}{(1+r)^n-1}")
    st.write("A fully amortizing mortgage sets the payment so the loan balance reaches zero after the final period. Use the periodic rate and number of payments, not annual figures mixed with monthly periods.")

with equity_tab:
    st.subheader("Dividend valuation")
    col1, col2, col3 = st.columns(3)
    dividend = col1.number_input("Current annual dividend", value=2.0, min_value=0.0)
    required_return = col2.number_input("Required return", value=0.10, format="%.4f")
    growth_rate = col3.number_input("Constant dividend growth", value=0.04, format="%.4f")
    constant_value = constant_dividend_value(dividend, required_return)
    growth_value = constant_growth_dividend_value(dividend * (1 + growth_rate), required_return, growth_rate)
    constant_col, growth_col = st.columns(2)
    constant_col.metric("Constant dividend value", f"{constant_value:,.2f}")
    growth_col.metric("Constant-growth stock value", f"{growth_value:,.2f}")
    st.latex(r"P_0=\frac{D}{r}\qquad P_0=\frac{D_1}{r-g}")
    st.write("The constant dividend model values a level perpetuity. The constant-growth model, also called the Gordon growth model, values dividends growing forever at a stable rate below the required return.")

    high_growth = st.number_input("Initial high-growth rate", value=0.12, format="%.4f")
    stable_growth = st.number_input("Stable growth rate", value=0.04, format="%.4f")
    high_growth_years = st.number_input("High-growth stage years", value=5.0, min_value=1.0)
    two_stage_value = two_stage_dividend_value(dividend, high_growth, stable_growth, required_return, int(high_growth_years))
    st.metric("Two-stage dividend discount value", f"{two_stage_value:,.2f}")
    st.latex(r"P_0=\underbrace{\sum_{t=1}^{N}\frac{D_0(1+g_1)^t}{(1+r)^t}}_{PV\ of\ stage\ 1}+\underbrace{\frac{D_0(1+g_1)^N(1+g_2)}{(r-g_2)(1+r)^N}}_{PV\ of\ stage\ 2\ and\ terminal\ value}")
    st.write("The two-stage model discounts the initial period of higher growth one dividend at a time. It then calculates a terminal value using stable growth and discounts that terminal value back to today.")

    st.subheader("Implied return and valuation ratios")
    stock_price = st.number_input("Stock price", value=40.0, min_value=0.01)
    next_dividend = dividend * (1 + growth_rate)
    implied_return = constant_growth_implied_return(stock_price, next_dividend, growth_rate)
    eps = st.number_input("Earnings per share", value=4.0, format="%.4f")
    forward_eps = st.number_input("Forward earnings per share", value=4.4, format="%.4f")
    net_income = st.number_input("Net income", value=100.0, min_value=0.01)
    dividends_total = st.number_input("Total dividends", value=35.0, min_value=0.0)
    return_col, pe_col, forward_col, payout_col = st.columns(4)
    return_col.metric("Implied return", f"{implied_return:.2%}")
    pe_col.metric("P/E ratio", f"{pe_ratio(stock_price, eps):.2f}x")
    forward_col.metric("Forward P/E ratio", f"{stock_price / forward_eps:.2f}x")
    payout_col.metric("Dividend payout ratio", f"{dividend_payout_ratio(dividends_total, net_income):.2%}")
    st.latex(r"r=\frac{D_1}{P_0}+g\qquad P/E=\frac{P_0}{EPS_0}\qquad Forward\ P/E=\frac{P_0}{EPS_1}\qquad Payout=\frac{D}{NI}")
    st.write("Implied return decomposes expected return into dividend yield and growth. P/E compares price with current earnings, forward P/E uses expected earnings, and payout ratio shows how much profit is distributed rather than retained.")
