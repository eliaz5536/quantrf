import numpy as np
import pytest

from quantitative_methods import (
    beta,
    capital_market_line_return,
    capital_market_line_risk,
    correlation_coefficient,
    covariance,
    global_minimum_variance_portfolio,
    jensens_alpha,
    msquared_ratio,
    portfolio_return,
    portfolio_standard_deviation,
    portfolio_variance,
    security_market_line_return,
    sharpe_ratio,
    treynor_ratio,
    two_asset_portfolio_variance,
)


def test_portfolio_return_and_two_asset_risk():
    assert portfolio_return([0.4, 0.6], [0.08, 0.12]) == pytest.approx(0.104)
    variance = two_asset_portfolio_variance(0.4, 0.6, 0.04, 0.09, 0.01)
    assert variance == pytest.approx(0.0436)
    assert portfolio_standard_deviation(variance) == pytest.approx(np.sqrt(0.0436))


def test_covariance_correlation_and_global_minimum_variance():
    first = np.array([0.01, 0.02, 0.03, 0.04])
    second = np.array([0.02, 0.01, 0.04, 0.03])
    assert covariance(first, second) == pytest.approx(0.0001)
    assert correlation_coefficient(first, second) == pytest.approx(0.6)
    matrix = np.array([[0.04, 0.01], [0.01, 0.09]])
    weights, variance, risk = global_minimum_variance_portfolio(matrix)
    assert weights.sum() == pytest.approx(1)
    assert variance == pytest.approx(weights @ matrix @ weights)
    assert risk == pytest.approx(np.sqrt(variance))


def test_cal_sml_and_performance_measures():
    assert capital_market_line_return(0.03, 0.09, 0.15, 0.10) == pytest.approx(0.07)
    assert capital_market_line_risk(0.03, 0.09, 0.15, 0.07) == pytest.approx(0.10)
    assert beta([0.06, 0.09, 0.0, 0.11], [0.05, 0.07, 0.01, 0.09]) > 0
    assert security_market_line_return(0.03, 1.2, 0.09) == pytest.approx(0.102)
    assert sharpe_ratio(0.10, 0.03, 0.20) == pytest.approx(0.35)
    assert treynor_ratio(0.10, 0.03, 1.4) == pytest.approx(0.05)
    assert msquared_ratio(0.10, 0.03, 0.20, 0.15) == pytest.approx(0.0825)
    assert jensens_alpha(0.11, 0.03, 1.1, 0.09) == pytest.approx(0.014)
