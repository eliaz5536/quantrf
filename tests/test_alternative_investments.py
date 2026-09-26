import pytest

from quantitative_methods import (
    gp_catch_up_clause,
    gp_rate_of_return,
    lp_distribution,
    lp_preferred_return,
    private_equity_waterfall,
)


def test_lp_preferred_return_and_gp_catch_up():
    preferred = lp_preferred_return(1000, 0.08, 3)
    assert preferred == pytest.approx(259.712)
    assert gp_catch_up_clause(preferred, 0.20) == pytest.approx(64.928)


def test_waterfall_distributes_all_proceeds():
    waterfall = private_equity_waterfall(1400, 1000, 259.712, 0.20)
    total_distributed = waterfall["lp_total_distribution"] + waterfall["gp_total_distribution"]
    assert total_distributed == pytest.approx(1400)
    assert lp_distribution(1400, 1000, 259.712, 0.20) == pytest.approx(waterfall["lp_total_distribution"])
    assert waterfall["gp_catch_up"] == pytest.approx(64.928)


def test_gp_rate_of_return():
    assert gp_rate_of_return(80, 50, 3) == pytest.approx((80 / 50) ** (1 / 3) - 1)
