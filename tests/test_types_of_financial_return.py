import pytest

from quantitative_methods import (
    annualized_effective_rate,
    beginning_price_change,
    complete_investor_outcome,
    distribution_price_interaction,
    effective_annual_rate,
    periods_per_year,
    risk_premium,
)


def test_investor_outcome_combines_price_change_and_distribution():
    assert beginning_price_change(100, 108) == pytest.approx(8)
    assert complete_investor_outcome(100, 108, 2) == pytest.approx(10)
    assert complete_investor_outcome(100, 108, 2) / 100 == pytest.approx(0.10)


def test_distribution_reduces_ex_distribution_price():
    assert distribution_price_interaction(50, 1.25) == pytest.approx(48.75)


def test_risk_premium_and_annualization():
    assert risk_premium(0.09, 0.04) == pytest.approx(0.05)
    assert periods_per_year(90, 360) == pytest.approx(4)
    assert annualized_effective_rate(0.06, 90, 360) == pytest.approx(0.26247696)
    assert effective_annual_rate(0.015, 4) == pytest.approx((1.015**4) - 1)
