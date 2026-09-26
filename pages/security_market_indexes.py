"""Interactive CFA Equity security market indexes page."""

import streamlit as st

from quantitative_methods import (
    equal_weighting,
    float_adjusted_market_cap_weighting,
    fundamental_weighting,
    index_price_return,
    index_total_return,
    market_cap_weighting,
    price_return_index_value,
    price_weighting,
)


def _numbers(text):
    return [float(value.strip()) for value in text.split(",") if value.strip()]


def _percentages(values):
    return [f"{value:.2%}" for value in values]


st.set_page_config(page_title="Security Market Indexes", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Security Market Indexes")
st.caption("Equity | CFA-aligned interactive learning lab")
st.write(
    "An equity index is a rules-based summary of a group of securities. "
    "Its return and behavior depend on whether constituents are weighted by price, equally, by market value, by float-adjusted market value, or by fundamentals."
)

returns_tab, weighting_tab = st.tabs(["Index value and returns", "Weighting methods"])

with returns_tab:
    st.subheader("Value of a price return index")
    col1, col2 = st.columns(2)
    beginning_prices = _numbers(col1.text_input("Beginning constituent prices", "100, 50, 25"))
    ending_prices = _numbers(col2.text_input("Ending constituent prices", "110, 48, 27"))
    divisor = st.number_input("Index divisor", value=1.0, min_value=0.0001, format="%.4f")
    if len(beginning_prices) == len(ending_prices) and beginning_prices:
        beginning_index = price_return_index_value(beginning_prices, divisor)
        ending_index = price_return_index_value(ending_prices, divisor)
        price_return = index_price_return(beginning_index, ending_index)
        distributions = st.number_input("Index-point distributions during period", value=2.0, min_value=0.0)
        total_return = index_total_return(beginning_index, ending_index, distributions)
        begin_col, end_col, price_col, total_col = st.columns(4)
        begin_col.metric("Beginning index value", f"{beginning_index:,.2f}")
        end_col.metric("Ending index value", f"{ending_index:,.2f}")
        price_col.metric("Price return", f"{price_return:.2%}")
        total_col.metric("Total return", f"{total_return:.2%}")
        st.latex(r"Index\ Value=\frac{\sum_i P_i}{Divisor}")
        st.latex(r"Price\ Return=\frac{I_1-I_0}{I_0}\qquad Total\ Return=\frac{I_1-I_0+D}{I_0}")
        st.write("A price return index captures only constituent price changes. A total return index adds dividends or other distributions, usually assuming they are reinvested. The divisor preserves index continuity after splits, additions, deletions, or other corporate actions.")
    else:
        st.warning("Enter beginning and ending price lists with the same number of securities.")

with weighting_tab:
    st.subheader("Compare index weighting schemes")
    prices = _numbers(st.text_input("Current constituent prices", "110, 48, 27"))
    shares = _numbers(st.text_input("Shares outstanding (millions)", "100, 250, 500"))
    float_factors = [value / 100 for value in _numbers(st.text_input("Float factors (%)", "80, 60, 90"))]
    fundamentals = _numbers(st.text_input("Fundamental measures", "120, 100, 80"))
    if prices and len({len(prices), len(shares), len(float_factors), len(fundamentals)}) == 1:
        market_caps = [price * share for price, share in zip(prices, shares)]
        weight_price = price_weighting(prices)
        weight_equal = equal_weighting(len(prices))
        weight_market_cap = market_cap_weighting(market_caps)
        weight_float = float_adjusted_market_cap_weighting(market_caps, float_factors)
        weight_fundamental = fundamental_weighting(fundamentals)
        st.dataframe(
            {
                "Security": [f"Security {index}" for index in range(1, len(prices) + 1)],
                "Price weighting": _percentages(weight_price),
                "Equal weighting": _percentages(weight_equal),
                "Market cap weighting": _percentages(weight_market_cap),
                "Float-adjusted market cap": _percentages(weight_float),
                "Fundamental weighting": _percentages(weight_fundamental),
            },
            hide_index=True,
            use_container_width=True,
        )
        st.latex(r"w_i^{price}=\frac{P_i}{\sum_jP_j}\qquad w_i^{equal}=\frac{1}{N}")
        st.latex(r"w_i^{cap}=\frac{P_iQ_i}{\sum_jP_jQ_j}\qquad w_i^{float}=\frac{P_iQ_i f_i}{\sum_jP_jQ_j f_j}")
        st.latex(r"w_i^{fundamental}=\frac{Fundamental_i}{\sum_jFundamental_j}")
        st.write("Price weighting gives expensive shares more influence regardless of company size. Equal weighting gives every security the same influence. Market-cap weighting reflects aggregate equity value; float adjustment removes closely held shares that are not readily available to public investors. Fundamental weighting uses measures such as earnings, sales, book value, or cash flow instead of market price.")
    else:
        st.warning("Enter equally sized, non-empty lists for prices, shares, float factors, and fundamentals.")

with st.expander("Practical interpretation"):
    st.markdown("Index construction determines what the index represents and how it rebalances. Price-weighted indexes can be moved by a high-priced constituent; capitalization-weighted indexes can become concentrated in the largest companies; equal and fundamental weighting introduce different rebalancing and implementation effects.")
    st.markdown("These examples use simplified constituent data. Real indexes also specify eligibility, corporate-action adjustments, rebalancing dates, investability screens, and treatment of distributions.")
