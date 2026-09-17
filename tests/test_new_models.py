import numpy as np

from american_models import brenner_galai_option_price, ju_zhong_option_price
from credit_models import distance_to_default, merton_equity_value, probability_of_default, solve_asset_value
from risk_models import historical_cvar, historical_var, parametric_cvar, parametric_var
from volatility_models import fit_garch11, forecast_garch11


def test_american_models_are_finite_and_respect_intrinsic_value():
    for model in (ju_zhong_option_price, brenner_galai_option_price):
        call = model(110, 100, 1, .05, .03, .2, option="call", steps=100)
        put = model(90, 100, 1, .05, .03, .2, option="put", steps=100)
        assert call >= 10
        assert put >= 10 * np.exp(-.05)


def test_merton_credit_metrics_have_expected_ranges_and_inversion():
    equity = merton_equity_value(150, 100, 1, .05, .25)
    inferred = solve_asset_value(equity, 100, 1, .05, .25)
    assert np.isclose(inferred, 150, rtol=1e-5)
    assert distance_to_default(150, 100, 1, .05, .25) > 0
    assert 0 <= probability_of_default(150, 100, 1, .05, .25) <= 1


def test_var_and_cvar_are_positive_loss_measures():
    returns = np.array([-.10, -.05, -.01, .01, .02, .03])
    assert historical_var(returns, .8, 100) > 0
    assert historical_cvar(returns, .8, 100) >= historical_var(returns, .8, 100)
    assert parametric_cvar(.001, .02, .95, 100) >= parametric_var(.001, .02, .95, 100)


def test_garch_fit_and_forecast_are_finite():
    returns = np.random.default_rng(7).normal(0, .01, 100)
    fit = fit_garch11(returns)
    assert fit["omega"] > 0
    assert fit["alpha"] >= 0
    assert fit["beta"] >= 0
    assert np.isfinite(fit["conditional_volatility"]).all()
    assert np.isfinite(forecast_garch11(fit, 5)).all()
