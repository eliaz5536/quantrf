import pytest

from quantitative_methods import (
    equal_weighting,
    float_adjusted_market_cap_weighting,
    fundamental_weighting,
    index_price_return,
    index_total_return,
    market_cap_weighting,
    price_return_index_value,
    price_weighting,
)


def test_index_values_and_returns():
    beginning = price_return_index_value([100, 50, 25])
    ending = price_return_index_value([110, 48, 27])
    assert beginning == pytest.approx(175)
    assert ending == pytest.approx(185)
    assert index_price_return(beginning, ending) == pytest.approx(10 / 175)
    assert index_total_return(beginning, ending, 2) == pytest.approx(12 / 175)


def test_index_weighting_methods_normalize():
    prices = [100, 50, 25]
    market_caps = [1000, 500, 250]
    assert sum(price_weighting(prices)) == pytest.approx(1)
    assert equal_weighting(3).tolist() == pytest.approx([1 / 3] * 3)
    assert market_cap_weighting(market_caps).tolist() == pytest.approx([1000 / 1750, 500 / 1750, 250 / 1750])
    assert sum(float_adjusted_market_cap_weighting(market_caps, [0.8, 0.6, 0.9])) == pytest.approx(1)
    assert sum(fundamental_weighting([120, 100, 80])) == pytest.approx(1)
