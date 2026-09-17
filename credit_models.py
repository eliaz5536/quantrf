"""Structural credit-risk models."""

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm


def merton_equity_value(asset_value, debt_face, maturity, rate, asset_volatility):
    """Merton equity value, treating equity as a call on firm assets."""
    _validate(asset_value, debt_face, maturity, asset_volatility)
    d1 = (np.log(asset_value / debt_face) + (rate + 0.5 * asset_volatility**2) * maturity) / (asset_volatility * np.sqrt(maturity))
    d2 = d1 - asset_volatility * np.sqrt(maturity)
    equity = asset_value * norm.cdf(d1) - debt_face * np.exp(-rate * maturity) * norm.cdf(d2)
    return float(equity)


def merton_debt_value(asset_value, debt_face, maturity, rate, asset_volatility):
    """Market value of risky debt implied by the Merton balance sheet."""
    return float(asset_value - merton_equity_value(asset_value, debt_face, maturity, rate, asset_volatility))


def distance_to_default(asset_value, debt_face, maturity, rate, asset_volatility):
    """Merton/KMV distance to default measured in asset-volatility units."""
    _validate(asset_value, debt_face, maturity, asset_volatility)
    return float((np.log(asset_value / debt_face) + (rate - 0.5 * asset_volatility**2) * maturity) / (asset_volatility * np.sqrt(maturity)))


def probability_of_default(asset_value, debt_face, maturity, rate, asset_volatility):
    """Risk-neutral default probability at maturity."""
    return float(norm.cdf(-distance_to_default(asset_value, debt_face, maturity, rate, asset_volatility)))


def solve_asset_value(equity_value, debt_face, maturity, rate, asset_volatility):
    """Infer firm asset value from observed equity using Merton's equation."""
    if equity_value <= 0 or debt_face <= 0:
        raise ValueError("equity_value and debt_face must be positive")
    lower = max(equity_value, debt_face * 1e-6)
    upper = max(debt_face * 2.0, equity_value * 5.0)
    while merton_equity_value(upper, debt_face, maturity, rate, asset_volatility) < equity_value:
        upper *= 2.0
    return float(brentq(lambda a: merton_equity_value(a, debt_face, maturity, rate, asset_volatility) - equity_value, lower, upper))


def _validate(asset_value, debt_face, maturity, asset_volatility):
    if min(asset_value, debt_face, maturity, asset_volatility) <= 0:
        raise ValueError("asset value, debt, maturity, and volatility must be positive")
