import pytest

from quantitative_methods import (
    gp_rate_of_return,
    leveraged_rate_of_return,
    money_weighted_return,
    multiple_of_invested_capital,
    return_to_investors,
)


def test_irr_and_moic_measure_different_performance_dimensions():
    assert money_weighted_return([-1000, 0, 0, 1400], [0, 1, 2, 3]) == pytest.approx((1.4 ** (1 / 3)) - 1)
    assert multiple_of_invested_capital(1400, 1000) == pytest.approx(1.4)
    assert return_to_investors(1400, 1000) == pytest.approx(0.4)


def test_leveraged_return():
    assert leveraged_rate_of_return(0.15, 2, 0.06) == pytest.approx(0.24)


def test_gp_return():
    assert gp_rate_of_return(80, 50, 3) == pytest.approx((80 / 50) ** (1 / 3) - 1)
