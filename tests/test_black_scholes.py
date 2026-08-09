######################################################
# ! REVIEW THE FOLLOWING FILE
######################################################

import numpy as np

if __package__ in {None, ""}:
    from black_scholes_app import bs_price, implied_volatility, figlewski_option_price, hull_white_option_price
else:
    from ..black_scholes_app import bs_price, implied_volatility, figlewski_option_price, hull_white_option_price


def test_bs_price_call_matches_expected_value():
    price = bs_price(100.0, 100.0, 1.0, 0.05, 0.2, option="call")
    assert np.isclose(price, 10.4506, atol=1e-4)


def test_bs_price_put_matches_expected_value():
    price = bs_price(100.0, 100.0, 1.0, 0.05, 0.2, option="put")
    assert np.isclose(price, 5.5735, atol=1e-4)


def test_implied_volatility_recovers_input_volatility():
    true_sigma = 0.2
    price = bs_price(100.0, 100.0, 1.0, 0.05, true_sigma, option="call")
    sigma = implied_volatility(price, 100.0, 100.0, 1.0, 0.05, option="call")
    assert np.isclose(sigma, true_sigma, atol=1e-4)


def test_figlewski_option_price_runs():
    call_price = figlewski_option_price(100.0, 100.0, 1.0, 0.05, 0.2, 100, option="call")
    put_price = figlewski_option_price(100.0, 100.0, 1.0, 0.05, 0.2, 100, option="put")
    assert call_price > 0.0
    assert put_price > 0.0


def test_hull_white_option_price_runs():
    call_price = hull_white_option_price(100.0, 100.0, 1.0, 0.05, 0.2, 100, option="call")
    put_price = hull_white_option_price(100.0, 100.0, 1.0, 0.05, 0.2, 100, option="put")
    assert call_price > 0.0
    assert put_price > 0.0