"""Market-risk measures with a positive-loss VaR convention."""

import numpy as np
from scipy.stats import norm


def historical_var(returns, confidence=0.95, portfolio_value=1.0):
    """Historical VaR: positive loss exceeded with probability 1-confidence."""
    losses = _losses(returns, portfolio_value)
    _validate_confidence(confidence)
    return float(np.quantile(losses, confidence, method="linear"))


def historical_cvar(returns, confidence=0.95, portfolio_value=1.0):
    """Historical CVaR/expected shortfall, conditional on losses beyond VaR."""
    losses = _losses(returns, portfolio_value)
    var = historical_var(returns, confidence, portfolio_value)
    tail = losses[losses >= var]
    return float(tail.mean())


def parametric_var(mean_return, volatility, confidence=0.95, portfolio_value=1.0):
    """Normal parametric VaR for simple returns."""
    if volatility < 0 or portfolio_value < 0:
        raise ValueError("volatility and portfolio_value must be non-negative")
    _validate_confidence(confidence)
    return float(portfolio_value * (-mean_return + volatility * norm.ppf(confidence)))


def parametric_cvar(mean_return, volatility, confidence=0.95, portfolio_value=1.0):
    """Normal parametric CVaR for simple returns."""
    if volatility < 0 or portfolio_value < 0:
        raise ValueError("volatility and portfolio_value must be non-negative")
    _validate_confidence(confidence)
    z = norm.ppf(confidence)
    return float(portfolio_value * (-mean_return + volatility * norm.pdf(z) / (1.0 - confidence)))


def _losses(returns, portfolio_value):
    if portfolio_value < 0:
        raise ValueError("portfolio_value must be non-negative")
    values = np.asarray(returns, dtype=float).ravel()
    if values.size == 0 or not np.isfinite(values).all():
        raise ValueError("returns must contain finite observations")
    return -portfolio_value * values


def _validate_confidence(confidence):
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")
