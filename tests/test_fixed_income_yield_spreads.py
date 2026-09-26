import pytest

from quantitative_methods import (
    annual_compounding,
    current_yield,
    g_spread,
    i_spread,
    monthly_compounding,
    option_adjusted_spread,
    periodicity_conversion,
    semiannual_compounding,
    simple_yield,
    yield_to_call,
    yield_to_maturity,
    yield_to_worst,
    z_spread,
)


def test_compounding_and_periodicity_conversion():
    annual = annual_compounding(1000, 0.06, 2)
    assert semiannual_compounding(1000, 0.06, 2) > annual
    monthly = monthly_compounding(1000, 0.06, 2)
    converted = periodicity_conversion(0.06, 2, 12)
    assert semiannual_compounding(1000, 0.06, 2) == pytest.approx(1000 * (1 + converted / 12) ** 24)


def test_simple_current_ytm_and_callable_yields():
    assert simple_yield(1000, 0.06, 980, 5) == pytest.approx((60 + 4) / 980)
    assert current_yield(1000, 0.06, 980) == pytest.approx(60 / 980)
    price = 980
    ytm = yield_to_maturity(price, 1000, 0.06, 5, 2)
    ytc = yield_to_call(price, 1000, 0.06, 1020, 3, 2)
    assert ytm > 0.06
    assert ytc > ytm
    assert yield_to_worst(price, 1000, 0.06, 5, [(1020, 3)], 2) == pytest.approx(ytm)


def test_spread_measures():
    assert g_spread(0.065, 0.045) == pytest.approx(0.02)
    assert i_spread(0.065, 0.05) == pytest.approx(0.015)
    cash_flows = [30, 30, 30, 1030]
    spot_rates = [0.04, 0.042, 0.044, 0.046]
    periods = [1, 2, 3, 4]
    price = sum(cash_flow / (1 + rate + 0.01) ** period for cash_flow, rate, period in zip(cash_flows, spot_rates, periods))
    assert z_spread(price, cash_flows, spot_rates, periods) == pytest.approx(0.01)
    assert option_adjusted_spread(0.02, 10, 1000, 5) == pytest.approx(0.018)
