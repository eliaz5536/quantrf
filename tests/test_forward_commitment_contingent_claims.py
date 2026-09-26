import pytest

from quantitative_methods import (
    call_option_payoff,
    long_forward_payoff,
    mark_to_market_change,
    netting,
    put_option_payoff,
    settlement_amount,
    short_forward_payoff,
)


def test_forward_payoffs_are_linear_and_opposite():
    assert long_forward_payoff(110, 100) == pytest.approx(10)
    assert short_forward_payoff(110, 100) == pytest.approx(-10)


def test_mark_to_market_settlement_and_netting():
    assert mark_to_market_change(100, 103, "long") == pytest.approx(3)
    assert mark_to_market_change(100, 103, "short") == pytest.approx(-3)
    assert settlement_amount(3, 100, 2) == pytest.approx(600)
    assert netting([600, -150, 75]) == pytest.approx(525)


def test_call_and_put_payoffs():
    assert call_option_payoff(110, 100, "long") == pytest.approx(10)
    assert call_option_payoff(90, 100, "long") == pytest.approx(0)
    assert put_option_payoff(90, 100, "long") == pytest.approx(10)
    assert put_option_payoff(110, 100, "short") == pytest.approx(0)
