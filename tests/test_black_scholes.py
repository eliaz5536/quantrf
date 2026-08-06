import numpy as np

if __package__ in {None, ""}:
    from black_scholes_app import bs_price, implied_volatility
else:
    from ..black_scholes_app import bs_price, implied_volatility


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
