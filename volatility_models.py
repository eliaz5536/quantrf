"""Dependency-light GARCH volatility estimation."""

import numpy as np
from scipy.optimize import minimize


def fit_garch11(returns, mean_return=0.0):
    """Fit GARCH(1,1): h_t = omega + alpha eps_{t-1}^2 + beta h_{t-1}."""
    values = np.asarray(returns, dtype=float).ravel()
    if values.size < 20 or not np.isfinite(values).all():
        raise ValueError("at least 20 finite returns are required")
    centered = values - mean_return
    variance = max(float(np.var(centered)), 1e-12)

    def unpack(params):
        omega = np.exp(params[0])
        weights = np.exp(params[1:])
        alpha, beta = weights / (1.0 + weights.sum())
        return omega, alpha, beta

    def objective(params):
        omega, alpha, beta = unpack(params)
        conditional = np.empty(values.size)
        conditional[0] = variance
        for index in range(1, values.size):
            conditional[index] = omega + alpha * centered[index - 1] ** 2 + beta * conditional[index - 1]
        return 0.5 * np.sum(np.log(conditional) + centered**2 / conditional)

    initial = np.log([variance * 0.05, 0.08, 0.88])
    result = minimize(objective, initial, method="BFGS")
    omega, alpha, beta = unpack(result.x)
    conditional = _conditional_variance(centered, omega, alpha, beta, variance)
    return {
        "omega": float(omega), "alpha": float(alpha), "beta": float(beta),
        "conditional_variance": conditional, "conditional_volatility": np.sqrt(conditional),
        "success": bool(result.success), "log_likelihood": float(-result.fun),
    }


def forecast_garch11(fit, horizon=1):
    """Forecast conditional variance for future periods."""
    if horizon < 1:
        raise ValueError("horizon must be at least 1")
    omega, alpha, beta = fit["omega"], fit["alpha"], fit["beta"]
    last_variance = float(fit["conditional_variance"][-1])
    last_shock = float(fit.get("last_residual", 0.0))
    forecasts = np.empty(int(horizon))
    forecasts[0] = omega + alpha * last_shock**2 + beta * last_variance
    for index in range(1, int(horizon)):
        forecasts[index] = omega + (alpha + beta) * forecasts[index - 1]
    return forecasts


def _conditional_variance(centered, omega, alpha, beta, initial):
    conditional = np.empty(centered.size)
    conditional[0] = initial
    for index in range(1, centered.size):
        conditional[index] = omega + alpha * centered[index - 1] ** 2 + beta * conditional[index - 1]
    return conditional
