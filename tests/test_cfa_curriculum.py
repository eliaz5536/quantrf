import numpy as np
import pytest

from pages.cfa_curriculum import (
    black_scholes_value,
    bond_duration_convexity,
    bond_price,
    dupont_roe,
    gordon_growth_value,
    irr,
    npv,
    portfolio_metrics,
    wacc,
)


def test_quant_and_portfolio_metrics_are_consistent():
    returns = np.array([[.10, .04], [.06, .02], [.08, .03]])
    result = portfolio_metrics([.5, .5], returns, .01)
    assert result[0] == pytest.approx(.055)
    assert result[1] > 0
    assert result[2] > 0


def test_bond_price_and_sensitivity_metrics_are_finite():
    price = bond_price(1000, .05, .05, 5)
    duration, convexity = bond_duration_convexity(1000, .05, .05, 5)
    assert price == pytest.approx(1000)
    assert duration > 0
    assert convexity > 0


def test_valuation_identities_and_corporate_metrics():
    assert dupont_roe(.1, 1.5, 2) == pytest.approx(.3)
    assert gordon_growth_value(2, .10, .04) == pytest.approx(34.6666667)
    assert wacc(.10, .06 * (1 - .25), 700, 300) == pytest.approx(.0835)
    assert npv(.10, [-100, 60, 60]) > 0
    assert irr([-100, 60, 60]) == pytest.approx(.1306623863)


def test_put_call_parity_holds_for_black_scholes_values():
    call = black_scholes_value(100, 105, .04, .25, 1)
    put = black_scholes_value(100, 105, .04, .25, 1, option="Put")
    assert call - put == pytest.approx(100 - 105 * np.exp(-.04))