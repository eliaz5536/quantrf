import pytest

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


def test_capital_weights_and_wacc_components():
    weights = capital_structure_weights(300, 600, 100)
    assert weights == pytest.approx((0.3, 0.6, 0.1))
    assert after_tax_cost_of_debt(0.06, 0.25) == pytest.approx(0.045)
    assert cost_of_equity_capm(0.04, 1.1, 0.09) == pytest.approx(0.095)
    assert cost_of_preferred_stock(7, 100) == pytest.approx(0.07)
    assert capital_structure_wacc(0.3, 0.6, 0.1, 0.06, 0.095, 0.07, 0.25) == pytest.approx(0.0775)


def test_optimal_capital_structure_and_operating_metrics():
    assert optimal_capital_structure([0.0, 0.3, 0.6], [0.10, 0.08, 0.09]) == pytest.approx((0.3, 0.08))
    assert interest_coverage(120, 20) == pytest.approx(6)
    assert financial_leverage(120, 20) == pytest.approx(1.2)
    assert operating_leverage(180, 120) == pytest.approx(1.5)


def test_firm_value_relationships():
    assert value_of_firm(300, 700) == pytest.approx(1000)
    assert unlevered_firm_value(100, 0.10) == pytest.approx(1000)
    assert levered_firm_value(1000, 75) == pytest.approx(1075)
