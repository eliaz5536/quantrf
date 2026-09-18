import streamlit as st


st.set_page_config(
    page_title="References",
    layout="wide",
    page_icon="quantrf_logo_website.png",
)

st.sidebar.title("Quant Research Framework")
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
    "Selected books for option pricing, volatility, Greeks, and practical options strategy."
)

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