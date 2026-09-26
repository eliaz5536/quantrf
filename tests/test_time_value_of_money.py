import pytest

from quantitative_methods import (
    annuity_payment_from_present_value,
    cash_flow_additivity,
    constant_growth_dividend_value,
    coupon_bond_price,
    coupon_bond_yield,
    future_value,
    mortgage_payment,
    ordinary_annuity_present_value,
    present_value,
    two_stage_dividend_value,
    zero_coupon_bond_price,
)


def test_present_and_future_value_are_inverse_operations():
    amount = future_value(1000, 0.05, 4)
    assert amount == pytest.approx(1215.50625)
    assert present_value(amount, 0.05, 4) == pytest.approx(1000)


def test_bond_prices_and_ytm_are_consistent():
    price = coupon_bond_price(1000, 0.06, 0.05, 5, 2)
    assert price > 1000
    assert coupon_bond_yield(price, 1000, 0.06, 5, 2) == pytest.approx(0.05)
    assert zero_coupon_bond_price(1000, 0.05, 5) == pytest.approx(783.526166)


def test_annuity_and_mortgage_payment_recreate_present_value():
    payment = annuity_payment_from_present_value(10000, 0.04, 10)
    assert ordinary_annuity_present_value(payment, 0.04, 10) == pytest.approx(10000)
    assert mortgage_payment(10000, 0.04, 10) == pytest.approx(payment)


def test_dividend_models_and_cash_flow_additivity():
    assert constant_growth_dividend_value(2.08, 0.10, 0.04) == pytest.approx(34.6666667)
    assert two_stage_dividend_value(2, 0.12, 0.04, 0.10, 5) > 0
    assert cash_flow_additivity([100, 100, 1100], 0.05) == pytest.approx(
        100 + 100 / 1.05 + 1100 / 1.05**2
    )
