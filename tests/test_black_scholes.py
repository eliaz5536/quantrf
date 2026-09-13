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


def test_binomial_tree_functions_are_exposed_and_finite():
    from black_scholes_app import crr_option_price, jr_option_price, lr_option_price, tian_option_price

    for fn in (crr_option_price, jr_option_price, lr_option_price, tian_option_price):
        call_price, put_price, stock, call_tree, put_tree = fn(100.0, 100.0, 1.0, 0.05, 0.2, 10)
        assert np.isfinite(call_price)
        assert np.isfinite(put_price)
        assert np.isfinite(stock).all()
        assert np.isfinite(call_tree).all()
        assert np.isfinite(put_tree).all()


def test_interest_rate_model_functions_are_exposed_and_finite():
    from black_scholes_app import (
        cir_short_rate_path,
        cir_bond_price,
        cir_show_bond_prices,
        cir_yield_curve,
        vasicek_short_rate_path,
        vasicek_bond_price,
        vasicek_yield_curve,
    )

    t, rates = cir_short_rate_path(0.03, 0.80, 0.04, 0.02, 1.0, 10)
    assert np.isfinite(rates).all()

    bond_price = cir_bond_price(0.03, 0.80, 0.04, 0.02, 1.0)
    assert np.isfinite(bond_price)

    maturities = np.array([1.0, 2.0, 3.0])
    prices = cir_show_bond_prices(maturities, 0.03, 0.80, 0.04, 0.02)
    assert np.isfinite(prices).all()

    t, rates = vasicek_short_rate_path(0.03, 0.80, 0.04, 0.02, 1.0, 10)
    assert np.isfinite(rates).all()

    bond_price = vasicek_bond_price(0.03, 0.80, 0.04, 0.02, 1.0)
    assert np.isfinite(bond_price)

    prices = np.array([0.95, 0.90, 0.85])
    yields = vasicek_yield_curve(prices, maturities)
    assert np.isfinite(yields).all()


def test_american_approximation_functions_are_exposed_and_finite():
    from black_scholes_app import bs1993_option_price, bs2002_option_price

    call_1993 = bs1993_option_price(100.0, 100.0, 1.0, 0.05, 0.03, 0.20, option="call")
    put_1993 = bs1993_option_price(100.0, 100.0, 1.0, 0.05, 0.03, 0.20, option="put")
    assert np.isfinite(call_1993)
    assert np.isfinite(put_1993)

    call_2002 = bs2002_option_price(100.0, 100.0, 1.0, 0.05, 0.03, 0.20, option="call")
    put_2002 = bs2002_option_price(100.0, 100.0, 1.0, 0.05, 0.03, 0.20, option="put")
    assert np.isfinite(call_2002)
    assert np.isfinite(put_2002)