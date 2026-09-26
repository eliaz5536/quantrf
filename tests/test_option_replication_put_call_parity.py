import pytest

from quantitative_methods import (
    call_option_premium_from_parity,
    debtholder_payoff,
    fiduciary_call_value,
    forward_option_put_call_difference,
    insolvent,
    present_value_strike,
    put_option_premium_from_parity,
    shareholder_payoff,
    solvent,
    synthetic_protective_put_value,
)


def test_fiduciary_call_equals_synthetic_protective_put():
    spot = 100
    strike = 100
    rate = 0.05
    years = 1
    put = 7
    call = call_option_premium_from_parity(spot, put, strike, rate, years)
    assert fiduciary_call_value(call, strike, rate, years) == pytest.approx(
        synthetic_protective_put_value(spot, put)
    )
    assert put_option_premium_from_parity(spot, call, strike, rate, years) == pytest.approx(put)
    assert present_value_strike(strike, rate, years) == pytest.approx(100 / 1.05)


def test_forward_option_parity():
    assert forward_option_put_call_difference(102, 100, 0.05, 1) == pytest.approx(2 / 1.05)


def test_solvency_and_corporate_security_payoffs():
    assert solvent(120, 100)
    assert not insolvent(120, 100)
    assert insolvent(80, 100)
    assert not solvent(80, 100)
    assert debtholder_payoff(80, 100) == pytest.approx(80)
    assert shareholder_payoff(80, 100) == pytest.approx(0)
    assert debtholder_payoff(120, 100) == pytest.approx(100)
    assert shareholder_payoff(120, 100) == pytest.approx(20)
