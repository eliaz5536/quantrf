"""Interactive CFA Equity market organization and structure page."""

import streamlit as st

from quantitative_methods import leverage_ratio, margin_call_price, maximum_leverage_ratio


st.set_page_config(page_title="Market Organization and Structure", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Market Organization and Structure")
st.caption("Equity | CFA-aligned interactive learning lab")
st.write(
    "Margin allows an investor to control a position with less than the full purchase price. "
    "Leverage magnifies both gains and losses, while margin requirements define how much equity must support the position."
)

leverage_tab, margin_tab = st.tabs(["Leverage", "Margin call"])

with leverage_tab:
    st.subheader("Leverage ratio")
    col1, col2 = st.columns(2)
    total_assets = col1.number_input("Total assets", value=150000.0, min_value=0.0, step=1000.0)
    equity = col2.number_input("Investor equity", value=75000.0, min_value=0.01, step=1000.0)
    ratio = leverage_ratio(total_assets, equity)
    st.metric("Leverage ratio", f"{ratio:.2f}x")
    st.latex(r"Leverage\ Ratio=\frac{Total\ Assets}{Equity}")
    st.write("A leverage ratio of 2.0x means each dollar of investor equity supports two dollars of assets, with the remainder financed by borrowing. Leverage increases exposure without increasing the initial equity contribution proportionally, but losses also flow through to equity faster.")

    st.subheader("Maximum leverage ratio")
    initial_margin = st.slider("Initial margin requirement", 0.01, 1.0, 0.50, 0.01)
    maximum_ratio = maximum_leverage_ratio(initial_margin)
    st.metric("Maximum leverage ratio", f"{maximum_ratio:.2f}x")
    st.latex(r"Maximum\ Leverage\ Ratio=\frac{1}{Initial\ Margin\ Requirement}")
    st.write("The initial margin requirement is the investor's equity share at purchase. A 50% initial margin permits a maximum 2.0x asset-to-equity leverage ratio before considering fees, interest, or price changes.")

with margin_tab:
    st.subheader("Margin call price")
    col1, col2, col3 = st.columns(3)
    shares = col1.number_input("Number of shares", value=100.0, min_value=0.01)
    purchase_price = col2.number_input("Initial share price", value=100.0, min_value=0.01)
    maintenance_margin = col3.slider("Maintenance margin requirement", 0.01, 0.99, 0.30, 0.01)
    call_price = margin_call_price(shares, purchase_price, initial_margin, maintenance_margin)
    st.metric("Margin call price", f"${call_price:,.2f}")
    st.latex(r"P_{call}=\frac{Loan}{N(1-MM)}=\frac{P_0(1-IM)}{1-MM}")
    st.write("For a long position, the margin call occurs when equity as a percentage of market value falls to the maintenance margin. The number of shares cancels algebraically, but it is shown to make the financed loan balance explicit.")

    loan = shares * purchase_price * (1 - initial_margin)
    current_value_at_call = shares * call_price
    equity_at_call = current_value_at_call - loan
    loan_col, value_col, equity_col = st.columns(3)
    loan_col.metric("Initial loan balance", f"${loan:,.2f}")
    value_col.metric("Position value at call", f"${current_value_at_call:,.2f}")
    equity_col.metric("Equity at call", f"${equity_at_call:,.2f}")
    st.latex(r"Equity=Market\ Value-Loan\ Balance\qquad \frac{Equity}{Market\ Value}=Maintenance\ Margin")
    st.write("If the share price falls below the calculated threshold, the broker may require additional funds or liquidate securities. Actual broker rules can include house requirements, interest, dividends, and intraday price changes.")

with st.expander("Practical interpretation"):
    st.markdown("**Leverage ratio** describes the size of assets controlled per dollar of equity. **Maximum leverage** is set by the initial margin rule. **Margin call price** is the price at which the maintenance-margin floor is breached.")
    st.markdown("These calculations are educational and assume a single long position with a constant loan balance. Short-sale margin and portfolio margin use different mechanics.")
