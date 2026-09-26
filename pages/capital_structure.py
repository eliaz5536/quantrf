"""Interactive CFA Corporate Issuers capital structure page."""

import numpy as np
import pandas as pd
import streamlit as st

from quantitative_methods import (
    after_tax_cost_of_debt,
    capital_structure_wacc,
    capital_structure_weights,
    cost_of_equity_capm,
    cost_of_preferred_stock,
    financial_leverage,
    interest_coverage,
    levered_firm_value,
    operating_leverage,
    optimal_capital_structure,
    unlevered_firm_value,
    value_of_firm,
)


st.set_page_config(page_title="Capital Structure", layout="wide", page_icon="quantrf_logo_website.png")
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

st.title("Capital Structure")
st.caption("Corporate Issuers | CFA-aligned interactive learning lab")
st.write(
    "Capital structure is the mix of debt, common equity, and preferred stock used to finance a company. "
    "The practical objective is to balance the tax benefits of debt against financial distress, agency, and financial-risk costs."
)

mix_tab, leverage_tab, value_tab = st.tabs(["WACC and D*", "Leverage and coverage", "Firm value"])

with mix_tab:
    st.subheader("Capital weights and WACC")
    col1, col2, col3 = st.columns(3)
    debt_value = col1.number_input("Debt value", value=300.0, min_value=0.0)
    equity_value = col2.number_input("Common equity value", value=600.0, min_value=0.0)
    preferred_value = col3.number_input("Preferred stock value", value=100.0, min_value=0.0)
    debt_weight, equity_weight, preferred_weight = capital_structure_weights(debt_value, equity_value, preferred_value)
    cost_debt = st.number_input("Pre-tax cost of debt", value=0.06, format="%.4f")
    tax_rate = st.number_input("Corporate tax rate", value=0.25, min_value=0.0, max_value=1.0, format="%.4f")
    risk_free = st.number_input("Risk-free rate", value=0.04, format="%.4f")
    beta_value = st.number_input("Equity beta", value=1.10, format="%.4f")
    market_return = st.number_input("Expected market return", value=0.09, format="%.4f")
    preferred_dividend = st.number_input("Preferred annual dividend", value=7.0, min_value=0.0)
    preferred_price = st.number_input("Preferred stock price", value=100.0, min_value=0.01)
    cost_equity = cost_of_equity_capm(risk_free, beta_value, market_return)
    cost_preferred = cost_of_preferred_stock(preferred_dividend, preferred_price)
    wacc_value = capital_structure_wacc(
        debt_weight,
        equity_weight,
        preferred_weight,
        cost_debt,
        cost_equity,
        cost_preferred,
        tax_rate,
    )
    weight_col, cost_col, wacc_col = st.columns(3)
    weight_col.metric("Debt weight (wd)", f"{debt_weight:.2%}")
    weight_col.metric("Common equity weight (we)", f"{equity_weight:.2%}")
    weight_col.metric("Preferred stock weight (wp)", f"{preferred_weight:.2%}")
    cost_col.metric("After-tax cost of debt", f"{after_tax_cost_of_debt(cost_debt, tax_rate):.2%}")
    cost_col.metric("Cost of equity", f"{cost_equity:.2%}")
    cost_col.metric("Cost of preferred stock", f"{cost_preferred:.2%}")
    wacc_col.metric("WACC", f"{wacc_value:.2%}")
    st.latex(r"WACC=w_dk_d(1-T)+w_ek_e+w_pk_p")
    st.latex(r"k_e=R_f+\beta(R_M-R_f)\qquad k_p=\frac{D_p}{P_p}")
    st.write("WACC combines the required returns of each funding source using market-value weights. Debt receives a tax adjustment because interest is generally tax deductible; common equity is often estimated with CAPM, while preferred cost is its dividend yield.")

    st.subheader("D*: optimal capital structure")
    preferred_for_curve = st.slider("Preferred weight held constant for D* analysis", 0.0, 0.30, float(preferred_weight), 0.01)
    candidate_debt_weights = np.linspace(0.0, 1.0 - preferred_for_curve, 51)
    candidate_wacc = np.array(
        [
            capital_structure_wacc(
                debt_weight_value,
                1 - preferred_for_curve - debt_weight_value,
                preferred_for_curve,
                cost_debt,
                cost_equity,
                cost_preferred,
                tax_rate,
            )
            for debt_weight_value in candidate_debt_weights
        ]
    )
    optimal_debt, minimum_wacc = optimal_capital_structure(candidate_debt_weights, candidate_wacc)
    d_col, min_col = st.columns(2)
    d_col.metric("D* debt weight", f"{optimal_debt:.2%}")
    min_col.metric("Minimum WACC at D*", f"{minimum_wacc:.2%}")
    curve = pd.DataFrame({"WACC": candidate_wacc}, index=candidate_debt_weights)
    curve.index.name = "Debt weight"
    st.line_chart(curve)
    st.latex(r"D^*=\arg\min_{d\in[0,1]}WACC(d)")
    st.write("D* is the debt proportion that minimizes WACC under the supplied assumptions. In practice, the curve may eventually rise as distress, agency, refinancing, and rating costs offset the tax shield.")

with leverage_tab:
    st.subheader("Interest coverage and financial leverage")
    col1, col2, col3 = st.columns(3)
    ebit = col1.number_input("EBIT", value=120.0, min_value=0.01)
    interest = col2.number_input("Interest expense", value=20.0, min_value=0.01)
    contribution_margin = col3.number_input("Contribution margin", value=180.0, min_value=0.01)
    coverage = interest_coverage(ebit, interest)
    financial = financial_leverage(ebit, interest)
    operating = operating_leverage(contribution_margin, ebit)
    coverage_col, financial_col, operating_col = st.columns(3)
    coverage_col.metric("Interest coverage", f"{coverage:.2f}x")
    financial_col.metric("Financial leverage", f"{financial:.2f}x")
    operating_col.metric("Operating leverage", f"{operating:.2f}x")
    st.latex(r"Interest\ Coverage=\frac{EBIT}{Interest}\qquad DFL=\frac{EBIT}{EBIT-Interest}")
    st.latex(r"DOL=\frac{Contribution\ Margin}{EBIT}")
    st.write("Interest coverage measures the buffer available to pay interest. Financial leverage measures how debt magnifies changes in pre-tax operating income into changes in earnings. Operating leverage measures sensitivity created by fixed operating costs; together they describe business and financing risk.")

with value_tab:
    st.subheader("Value of the firm")
    col1, col2 = st.columns(2)
    firm_debt = col1.number_input("Market value of debt", value=300.0, min_value=0.0)
    firm_equity = col2.number_input("Market value of equity", value=700.0, min_value=0.0)
    firm_value = value_of_firm(firm_debt, firm_equity)
    st.metric("Value of the firm", f"{firm_value:,.2f}")
    st.latex(r"V=D+E")
    st.write("The market-value identity says total firm value equals the market value of debt plus the market value of equity. Using market values keeps the capital mix tied to current investor claims rather than historical book values.")

    st.subheader("Unlevered and levered firm value")
    nopat = st.number_input("Unlevered NOPAT", value=100.0, min_value=0.0)
    unlevered_cost = st.number_input("Unlevered cost of capital", value=0.10, min_value=0.0001, format="%.4f")
    tax_shield = st.number_input("Present value of interest tax shield", value=75.0, min_value=0.0)
    unlevered = unlevered_firm_value(nopat, unlevered_cost)
    levered = levered_firm_value(unlevered, tax_shield)
    unlevered_col, shield_col, levered_col = st.columns(3)
    unlevered_col.metric("VU: unlevered firm value", f"{unlevered:,.2f}")
    shield_col.metric("PV of tax shield", f"{tax_shield:,.2f}")
    levered_col.metric("VL: levered firm value", f"{levered:,.2f}")
    st.latex(r"V_U=\frac{NOPAT}{k_U}\qquad V_L=V_U+PV(Tax\ Shield)")
    st.write("VU is the value of the business if financed entirely with equity. VL adds the value created by debt financing under the simplified tax-shield framework; real-world distress and agency costs can reduce that benefit.")

with st.expander("Practical interpretation"):
    st.markdown("**D*** is a decision point, not a universal debt percentage. The optimal mix depends on tax policy, earnings stability, asset collateral, financing access, credit ratings, distress costs, and management objectives.")
    st.markdown("These are educational CFA-aligned calculations. Production capital-structure analysis should use market values, forward-looking cash flows, realistic tax shields, refinancing assumptions, and scenario analysis.")
