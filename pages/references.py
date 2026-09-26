import streamlit as st

st.set_page_config(
    page_title="References",
    layout="wide",
    page_icon="quantrf_logo_website.png",
)

st.sidebar.image("images/sidebar_logo.png")
st.sidebar.page_link(page="pages/monte_carlo.py", label="Monte Carlo")
st.sidebar.page_link(page="main.py", label="Black-Scholes-Merton (1973)")
st.sidebar.page_link(page="pages/black.py", label="Black (1976)", disabled=True)
st.sidebar.page_link(page="pages/binomial_tree.py", label="Binomial Tree")
st.sidebar.page_link(page="pages/trinomial_tree.py", label="Trinomial Tree", disabled=True)
st.sidebar.page_link(page="pages/interest_rate_models.py", label="Interest Rate Models")
st.sidebar.page_link(page="pages/american_option_pricing.py", label="American Option Pricing")
st.sidebar.page_link(page="pages/credit_risk.py", label="Credit Risk")
st.sidebar.page_link(page="pages/risk_management.py", label="Risk Management")
st.sidebar.page_link(page="pages/volatility_models.py", label="Volatility Models")
st.sidebar.page_link(page="pages/cfa_curriculum.py", label="Rates and Returns")
st.sidebar.page_link(page="pages/time_value_of_money.py", label="Time Value of Money")
st.sidebar.page_link(page="pages/types_of_financial_return.py", label="Types of Financial Return")
st.sidebar.page_link(page="pages/portfolio_risk_return.py", label="Portfolio Risk and Return")
st.sidebar.page_link(page="pages/fixed_income_yield_spreads.py", label="Fixed Income Yield Spreads")
st.sidebar.page_link(page="pages/market_organization_structure.py", label="Market Organization and Structure")
st.sidebar.page_link(page="pages/security_market_indexes.py", label="Security Market Indexes")
st.sidebar.page_link(page="pages/forward_commitment_contingent_claims.py", label="Forward Commitments and Contingent Claims")
st.sidebar.page_link(page="pages/option_replication_put_call_parity.py", label="Option Replication Using Put-Call Parity")
st.sidebar.page_link(page="pages/capital_structure.py", label="Capital Structure")
st.sidebar.page_link(page="pages/alternative_investments.py", label="Alternative Investments")
st.sidebar.page_link(page="pages/alternative_investment_performance.py", label="Alternative Investment Performance")
st.sidebar.page_link(page="pages/references.py", label="References")

st.sidebar.markdown(
    """
    <div style='margin-bottom: 25px;'>
        <a href='https://www.linkedin.com/in/eliaz-simon/' target='_blank' style='text-decoration: none; display: flex; align-items: center; gap: 12px; margin-top: 8px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='32' height='32'/>
            <span style='color: #0A66C2; font-size: 18px; font-weight: bold;'>Eliaz Simon</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("References")
st.write(
    "Selected books for option pricing, volatility, Greeks, and practical options strategy. "
    "For interactive CFA-aligned equations and worked examples, open Rates and Returns."
)
st.page_link("pages/cfa_curriculum.py", label="Open Rates and Returns", icon="📈")

references = [
    {
        "cover": "images/option_volatility_&_pricing.jpg",
        "title": "Option Volatility and Pricing: Advanced Trading Strategies and Techniques",
        "author": "Sheldon Natenberg",
        "edition": "2nd Edition",
    },
    {
        "cover": "images/trading_option_greeks.jpeg",
        "title": "Trading Options Greeks: How Time, Volatility, and Other Pricing Factors Drive Profits",
        "author": "Dan Passarelli",
        "edition": "Bloomberg Financial",
    },
    {
        "cover": "images/options_as_a_strategic_investment.jpg",
        "title": "Options as a Strategic Investment",
        "author": "Lawrence G. McMillan",
        "edition": "5th Edition",
    },
]

for reference in references:
    cover_column, details_column = st.columns([1, 3], gap="large")
    with cover_column:
        st.image(reference["cover"], width=250)
    with details_column:
        st.subheader(reference["title"])
        st.write(f"**Author:** {reference['author']}")
        st.write(f"**Edition / series:** {reference['edition']}")
    st.divider()