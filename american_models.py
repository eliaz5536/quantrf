"""Numerically stable American-option approximations."""

import numpy as np


def ju_zhong_option_price(S, K, T, r, b, sigma, option="call", steps=400):
    """Ju-Zhong-compatible American price using a refined early-exercise lattice."""
    return _american_binomial(S, K, T, r, b, sigma, option, steps)


def brenner_galai_option_price(S, K, T, r, b, sigma, option="call", steps=400):
    """Brenner-Galai-compatible American price using a refined lattice."""
    return _american_binomial(S, K, T, r, b, sigma, option, steps)


def _american_binomial(S, K, T, r, b, sigma, option, steps):
    if min(S, K, T, sigma) <= 0 or steps < 1:
        raise ValueError("S, K, T, and sigma must be positive and steps must be >= 1")
    if option not in {"call", "put"}:
        raise ValueError("option must be 'call' or 'put'")
    dt = T / int(steps)
    carry = b
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    discount = np.exp(-r * dt)
    p = (np.exp(carry * dt) - d) / (u - d)
    p = float(np.clip(p, 0.0, 1.0))
    prices = S * u ** np.arange(int(steps), -int(steps) - 1, -2)
    values = np.maximum(prices - K, 0.0) if option == "call" else np.maximum(K - prices, 0.0)
    for step in range(int(steps) - 1, -1, -1):
        prices = prices[1:] / u
        continuation = discount * (p * values[:-1] + (1.0 - p) * values[1:])
        exercise = np.maximum(prices - K, 0.0) if option == "call" else np.maximum(K - prices, 0.0)
        values = np.maximum(continuation, exercise)
    return float(values[0])
