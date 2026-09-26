import pytest

from quantitative_methods import leverage_ratio, margin_call_price, maximum_leverage_ratio


def test_leverage_ratio_and_maximum_leverage():
    assert leverage_ratio(150000, 75000) == pytest.approx(2.0)
    assert maximum_leverage_ratio(0.50) == pytest.approx(2.0)


def test_margin_call_price_for_long_position():
    assert margin_call_price(100, 100, 0.50, 0.30) == pytest.approx(71.4285714)
