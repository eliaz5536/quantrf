"""CFA-aligned quantitative methods calculations."""

from math import exp, log, sqrt

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm


def holding_period_return(beginning_value, ending_value, income=0.0):
    """Return including income received during the holding period."""
    if beginning_value == 0:
        raise ValueError("Beginning value must be non-zero")
    return (ending_value - beginning_value + income) / beginning_value


def beginning_price_change(beginning_price, ending_price):
    """Change in market value during the holding period."""
    return float(ending_price - beginning_price)


def beginning_distribution(distribution):
    """Cash distribution received while the investment is held."""
    return float(distribution)


def complete_investor_outcome(beginning_price, ending_price, distribution=0.0):
    """Total dollar outcome from price change plus cash distribution."""
    return float(beginning_price_change(beginning_price, ending_price) + beginning_distribution(distribution))


def distribution_price_interaction(pre_distribution_price, distribution):
    """Approximate ex-distribution price after a cash distribution."""
    return float(pre_distribution_price - distribution)


def risk_premium(expected_return, risk_free_rate):
    return float(expected_return - risk_free_rate)


def annualized_effective_rate(holding_period_return_value, days_held, days_per_year=365):
    if days_held <= 0 or days_per_year <= 0 or holding_period_return_value <= -1:
        raise ValueError("Days must be positive and holding-period return must be greater than -100%")
    return float((1 + holding_period_return_value) ** (days_per_year / days_held) - 1)


def periods_per_year(days_held, days_per_year=365):
    if days_held <= 0 or days_per_year <= 0:
        raise ValueError("Days must be positive")
    return float(days_per_year / days_held)


def effective_annual_rate(periodic_rate, periods):
    if periods <= 0 or periodic_rate <= -1:
        raise ValueError("Periods must be positive and periodic rate must be greater than -100%")
    return float((1 + periodic_rate) ** periods - 1)


def arithmetic_mean(returns):
    values = np.asarray(returns, dtype=float)
    if values.size == 0:
        raise ValueError("At least one return is required")
    return float(np.mean(values))


def geometric_mean_return(returns):
    values = np.asarray(returns, dtype=float)
    if values.size == 0 or np.any(values <= -1):
        raise ValueError("Returns must be greater than -100%")
    return float(np.prod(1 + values) ** (1 / values.size) - 1)


def harmonic_mean(values):
    values = np.asarray(values, dtype=float)
    if values.size == 0 or np.any(values <= 0):
        raise ValueError("Values must be positive")
    return float(values.size / np.sum(1 / values))


def trimmed_mean(values, trim_fraction=0.1):
    values = np.sort(np.asarray(values, dtype=float))
    if values.size == 0 or not 0 <= trim_fraction < 0.5:
        raise ValueError("Trim fraction must be between 0 and 0.5")
    trim_count = int(values.size * trim_fraction)
    kept = values[trim_count:values.size - trim_count or None]
    return float(np.mean(kept))


def winsorized_mean(values, trim_fraction=0.1):
    values = np.sort(np.asarray(values, dtype=float))
    if values.size == 0 or not 0 <= trim_fraction < 0.5:
        raise ValueError("Trim fraction must be between 0 and 0.5")
    trim_count = int(values.size * trim_fraction)
    if trim_count == 0:
        return float(np.mean(values))
    winsorized = values.copy()
    winsorized[:trim_count] = values[trim_count]
    winsorized[-trim_count:] = values[-trim_count - 1]
    return float(np.mean(winsorized))


def money_weighted_return(cash_flows, periods=None):
    """IRR of dated or equally spaced cash flows, with investor cash-flow signs."""
    flows = np.asarray(cash_flows, dtype=float)
    if flows.size < 2 or not (np.any(flows > 0) and np.any(flows < 0)):
        raise ValueError("Cash flows need at least one positive and one negative value")
    times = np.arange(flows.size, dtype=float) if periods is None else np.asarray(periods, dtype=float)
    if times.size != flows.size or np.any(np.diff(times) <= 0):
        raise ValueError("Periods must be increasing and match cash flows")

    def npv_at(rate):
        return float(np.sum(flows / (1 + rate) ** times))

    grid = np.unique(np.concatenate([np.linspace(-0.9999, 1, 1000), np.linspace(1.01, 100, 500)]))
    for lower, upper in zip(grid[:-1], grid[1:]):
        if npv_at(lower) * npv_at(upper) <= 0:
            return float(brentq(npv_at, lower, upper))
    raise ValueError("No IRR found in the supported rate range")


def time_weighted_return(period_returns):
    values = np.asarray(period_returns, dtype=float)
    if values.size == 0 or np.any(values <= -1):
        raise ValueError("Period returns must be greater than -100%")
    return float(np.prod(1 + values) - 1)


def annualized_return(total_return, years):
    if years <= 0 or total_return <= -1:
        raise ValueError("Total return must be greater than -100% and years positive")
    return float((1 + total_return) ** (1 / years) - 1)


def continuously_compounded_return(beginning_value, ending_value, years=1.0):
    if beginning_value <= 0 or ending_value <= 0 or years <= 0:
        raise ValueError("Values and years must be positive")
    return float(log(ending_value / beginning_value) / years)


def real_return(nominal_return, inflation_rate):
    if inflation_rate <= -1:
        raise ValueError("Inflation rate must be greater than -100%")
    return float((1 + nominal_return) / (1 + inflation_rate) - 1)


def leveraged_return(asset_return, leverage_ratio, borrowing_rate=0.0):
    """Return on equity for leverage ratio = total asset value / equity."""
    if leverage_ratio <= 0:
        raise ValueError("Leverage ratio must be positive")
    return float(leverage_ratio * asset_return - (leverage_ratio - 1) * borrowing_rate)


def leverage_ratio(total_assets, equity):
    if total_assets < 0 or equity <= 0:
        raise ValueError("Total assets must be non-negative and equity must be positive")
    return float(total_assets / equity)


def maximum_leverage_ratio(initial_margin_requirement):
    if not 0 < initial_margin_requirement <= 1:
        raise ValueError("Initial margin requirement must be between 0 and 100%")
    return float(1 / initial_margin_requirement)


def margin_call_price(number_of_shares, initial_share_price, initial_margin_requirement, maintenance_margin_requirement):
    if number_of_shares <= 0 or initial_share_price <= 0:
        raise ValueError("Number of shares and initial share price must be positive")
    if not 0 < initial_margin_requirement <= 1:
        raise ValueError("Initial margin requirement must be between 0 and 100%")
    if not 0 <= maintenance_margin_requirement < 1:
        raise ValueError("Maintenance margin requirement must be between 0% and 100%")
    loan = number_of_shares * initial_share_price * (1 - initial_margin_requirement)
    return float(loan / (number_of_shares * (1 - maintenance_margin_requirement)))


def price_return_index_value(component_prices, divisor=1.0):
    prices = np.asarray(component_prices, dtype=float)
    if prices.size == 0 or np.any(prices < 0) or divisor <= 0:
        raise ValueError("Prices must be non-negative and divisor must be positive")
    return float(np.sum(prices) / divisor)


def index_price_return(beginning_index_value, ending_index_value):
    if beginning_index_value <= 0:
        raise ValueError("Beginning index value must be positive")
    return float(ending_index_value / beginning_index_value - 1)


def index_total_return(beginning_index_value, ending_index_value, distributions=0.0):
    if beginning_index_value <= 0:
        raise ValueError("Beginning index value must be positive")
    return float((ending_index_value - beginning_index_value + distributions) / beginning_index_value)


def price_weighting(component_prices):
    prices = np.asarray(component_prices, dtype=float)
    if prices.size == 0 or np.any(prices < 0) or np.sum(prices) <= 0:
        raise ValueError("Prices must be non-negative with a positive sum")
    return prices / np.sum(prices)


def equal_weighting(number_of_securities):
    if number_of_securities <= 0:
        raise ValueError("Number of securities must be positive")
    return np.full(number_of_securities, 1 / number_of_securities, dtype=float)


def market_cap_weighting(market_capitalizations):
    market_caps = np.asarray(market_capitalizations, dtype=float)
    if market_caps.size == 0 or np.any(market_caps < 0) or np.sum(market_caps) <= 0:
        raise ValueError("Market capitalizations must be non-negative with a positive sum")
    return market_caps / np.sum(market_caps)


def float_adjusted_market_cap_weighting(market_capitalizations, float_factors):
    market_caps = np.asarray(market_capitalizations, dtype=float)
    floats = np.asarray(float_factors, dtype=float)
    if market_caps.size != floats.size or np.any(market_caps < 0) or np.any((floats < 0) | (floats > 1)):
        raise ValueError("Market caps and float factors must match, with float factors between 0 and 1")
    adjusted_caps = market_caps * floats
    if adjusted_caps.size == 0 or np.sum(adjusted_caps) <= 0:
        raise ValueError("Float-adjusted market caps must have a positive sum")
    return adjusted_caps / np.sum(adjusted_caps)


def fundamental_weighting(fundamental_values):
    fundamentals = np.asarray(fundamental_values, dtype=float)
    if fundamentals.size == 0 or np.any(fundamentals < 0) or np.sum(fundamentals) <= 0:
        raise ValueError("Fundamental values must be non-negative with a positive sum")
    return fundamentals / np.sum(fundamentals)


def payoff_at_maturity(spot_at_maturity, delivery_price, position="long"):
    if position not in {"long", "short"}:
        raise ValueError("Position must be 'long' or 'short'")
    payoff = spot_at_maturity - delivery_price
    return float(payoff if position == "long" else -payoff)


def long_forward_payoff(spot_at_maturity, delivery_price):
    return payoff_at_maturity(spot_at_maturity, delivery_price, "long")


def short_forward_payoff(spot_at_maturity, delivery_price):
    return payoff_at_maturity(spot_at_maturity, delivery_price, "short")


def mark_to_market_change(previous_forward_price, current_forward_price, position="long"):
    if position not in {"long", "short"}:
        raise ValueError("Position must be 'long' or 'short'")
    change = current_forward_price - previous_forward_price
    return float(change if position == "long" else -change)


def settlement_amount(per_unit_payoff, contract_size=1.0, number_of_contracts=1):
    if contract_size < 0 or number_of_contracts < 0:
        raise ValueError("Contract size and number of contracts must be non-negative")
    return float(per_unit_payoff * contract_size * number_of_contracts)


def netting(settlements):
    values = np.asarray(settlements, dtype=float)
    if values.size == 0:
        raise ValueError("At least one settlement is required")
    return float(np.sum(values))


def call_option_payoff(spot_at_expiry, strike_price, position="long"):
    if position not in {"long", "short"}:
        raise ValueError("Position must be 'long' or 'short'")
    payoff = max(spot_at_expiry - strike_price, 0.0)
    return float(payoff if position == "long" else -payoff)


def put_option_payoff(spot_at_expiry, strike_price, position="long"):
    if position not in {"long", "short"}:
        raise ValueError("Position must be 'long' or 'short'")
    payoff = max(strike_price - spot_at_expiry, 0.0)
    return float(payoff if position == "long" else -payoff)


def present_value_strike(strike_price, risk_free_rate, years):
    if strike_price < 0 or years < 0 or 1 + risk_free_rate <= 0:
        raise ValueError("Strike must be non-negative, years non-negative, and rate greater than -100%")
    return float(strike_price / (1 + risk_free_rate) ** years)


def fiduciary_call_value(call_premium, strike_price, risk_free_rate, years):
    return float(call_premium + present_value_strike(strike_price, risk_free_rate, years))


def synthetic_protective_put_value(spot_price, put_premium):
    if spot_price < 0 or put_premium < 0:
        raise ValueError("Spot price and put premium must be non-negative")
    return float(spot_price + put_premium)


def call_option_premium_from_parity(spot_price, put_premium, strike_price, risk_free_rate, years, present_value_dividends=0.0):
    if spot_price < 0 or put_premium < 0 or present_value_dividends < 0:
        raise ValueError("Spot, put premium, and dividend value must be non-negative")
    return float(put_premium + spot_price - present_value_dividends - present_value_strike(strike_price, risk_free_rate, years))


def put_option_premium_from_parity(spot_price, call_premium, strike_price, risk_free_rate, years, present_value_dividends=0.0):
    if spot_price < 0 or call_premium < 0 or present_value_dividends < 0:
        raise ValueError("Spot, call premium, and dividend value must be non-negative")
    return float(call_premium + present_value_strike(strike_price, risk_free_rate, years) - spot_price + present_value_dividends)


def forward_option_put_call_difference(forward_price, strike_price, risk_free_rate, years):
    if forward_price < 0 or strike_price < 0:
        raise ValueError("Forward price and strike must be non-negative")
    return float((forward_price - strike_price) / (1 + risk_free_rate) ** years)


def shareholder_payoff(asset_value, debt_face_value):
    if asset_value < 0 or debt_face_value < 0:
        raise ValueError("Asset value and debt face value must be non-negative")
    return float(max(asset_value - debt_face_value, 0.0))


def debtholder_payoff(asset_value, debt_face_value):
    if asset_value < 0 or debt_face_value < 0:
        raise ValueError("Asset value and debt face value must be non-negative")
    return float(min(asset_value, debt_face_value))


def solvent(asset_value, debt_face_value):
    if asset_value < 0 or debt_face_value < 0:
        raise ValueError("Asset value and debt face value must be non-negative")
    return bool(asset_value >= debt_face_value)


def insolvent(asset_value, debt_face_value):
    return not solvent(asset_value, debt_face_value)


def bond_price(face_value, coupon_rate, yield_rate, years, frequency=2):
    periods = int(years * frequency)
    coupon = face_value * coupon_rate / frequency
    discount = 1 + yield_rate / frequency
    return float(sum(coupon / discount**period for period in range(1, periods + 1)) + face_value / discount**periods)


def bond_duration_convexity(face_value, coupon_rate, yield_rate, years, frequency=2):
    periods = int(years * frequency)
    coupon = face_value * coupon_rate / frequency
    discount = 1 + yield_rate / frequency
    cash_flows = np.array([coupon] * periods, dtype=float)
    cash_flows[-1] += face_value
    times = np.arange(1, periods + 1, dtype=float) / frequency
    present_values = cash_flows / discount ** np.arange(1, periods + 1)
    price = np.sum(present_values)
    duration = np.sum(times * present_values) / price
    convexity = np.sum(times * (times + 1 / frequency) * present_values) / (price * discount**2)
    return float(duration), float(convexity)


def future_value(present_value, rate, periods):
    return float(present_value * (1 + rate) ** periods)


def present_value(future_value_amount, rate, periods):
    if 1 + rate <= 0:
        raise ValueError("Rate must be greater than -100%")
    return float(future_value_amount / (1 + rate) ** periods)


def zero_coupon_bond_price(face_value, yield_rate, years, frequency=1):
    if frequency <= 0 or years < 0:
        raise ValueError("Frequency must be positive and years non-negative")
    return present_value(face_value, yield_rate / frequency, years * frequency)


def coupon_bond_price(face_value, coupon_rate, yield_rate, years, frequency=2):
    if frequency <= 0 or years <= 0:
        raise ValueError("Frequency and years must be positive")
    periods = int(years * frequency)
    coupon = face_value * coupon_rate / frequency
    discount = 1 + yield_rate / frequency
    return float(sum(coupon / discount**period for period in range(1, periods + 1)) + face_value / discount**periods)


def perpetual_bond_price(coupon_payment, required_return):
    if required_return <= 0:
        raise ValueError("Required return must be positive")
    return float(coupon_payment / required_return)


def ordinary_annuity_present_value(payment, rate, periods):
    if rate == 0:
        return float(payment * periods)
    return float(payment * (1 - (1 + rate) ** -periods) / rate)


def ordinary_annuity_future_value(payment, rate, periods):
    if rate == 0:
        return float(payment * periods)
    return float(payment * ((1 + rate) ** periods - 1) / rate)


def annuity_payment_from_present_value(present_value_amount, rate, periods):
    if periods <= 0:
        raise ValueError("Periods must be positive")
    if rate == 0:
        return float(present_value_amount / periods)
    return float(present_value_amount * rate / (1 - (1 + rate) ** -periods))


def annuity_payment_from_future_value(future_value_amount, rate, periods):
    if periods <= 0:
        raise ValueError("Periods must be positive")
    if rate == 0:
        return float(future_value_amount / periods)
    return float(future_value_amount * rate / ((1 + rate) ** periods - 1))


def mortgage_payment(principal, rate, periods):
    return annuity_payment_from_present_value(principal, rate, periods)


def constant_dividend_value(dividend, required_return):
    return perpetual_bond_price(dividend, required_return)


def constant_growth_dividend_value(next_dividend, required_return, growth_rate):
    if required_return <= growth_rate:
        raise ValueError("Required return must exceed growth rate")
    return float(next_dividend / (required_return - growth_rate))


def two_stage_dividend_value(current_dividend, first_growth_rate, stable_growth_rate, required_return, high_growth_years):
    if high_growth_years <= 0 or required_return <= stable_growth_rate:
        raise ValueError("High-growth years must be positive and required return must exceed stable growth")
    dividends = [current_dividend * (1 + first_growth_rate) ** year for year in range(1, high_growth_years + 1)]
    present_value_stage_one = sum(dividend / (1 + required_return) ** year for year, dividend in enumerate(dividends, 1))
    terminal_dividend = dividends[-1] * (1 + stable_growth_rate)
    terminal_value = terminal_dividend / (required_return - stable_growth_rate)
    present_value_stage_two = terminal_value / (1 + required_return) ** high_growth_years
    return float(present_value_stage_one + present_value_stage_two)


def implied_discount_bond_return(price, face_value, years):
    if price <= 0 or face_value <= 0 or years <= 0:
        raise ValueError("Price, face value, and years must be positive")
    return float((face_value / price) ** (1 / years) - 1)


def coupon_bond_yield(price, face_value, coupon_rate, years, frequency=2):
    if price <= 0 or frequency <= 0 or years <= 0:
        raise ValueError("Price, frequency, and years must be positive")
    periods = int(years * frequency)
    coupon = face_value * coupon_rate / frequency

    def price_at(yield_rate):
        discount = 1 + yield_rate / frequency
        return sum(coupon / discount**period for period in range(1, periods + 1)) + face_value / discount**periods

    return float(brentq(lambda yield_rate: price_at(yield_rate) - price, -0.9999, 100))


def compounded_value(principal, annual_rate, years, compounds_per_year):
    if principal < 0 or years < 0 or compounds_per_year <= 0:
        raise ValueError("Principal and years must be non-negative and frequency must be positive")
    return float(principal * (1 + annual_rate / compounds_per_year) ** (compounds_per_year * years))


def annual_compounding(principal, annual_rate, years=1.0):
    return compounded_value(principal, annual_rate, years, 1)


def semiannual_compounding(principal, annual_rate, years=1.0):
    return compounded_value(principal, annual_rate, years, 2)


def quarterly_compounding(principal, annual_rate, years=1.0):
    return compounded_value(principal, annual_rate, years, 4)


def monthly_compounding(principal, annual_rate, years=1.0):
    return compounded_value(principal, annual_rate, years, 12)


def periodicity_conversion(nominal_rate, from_periods, to_periods):
    """Convert nominal annual rates between compounding frequencies."""
    if from_periods <= 0 or to_periods <= 0 or nominal_rate / from_periods <= -1:
        raise ValueError("Frequencies must be positive and periodic rate must exceed -100%")
    effective_annual = (1 + nominal_rate / from_periods) ** from_periods - 1
    return float(to_periods * ((1 + effective_annual) ** (1 / to_periods) - 1))


def simple_yield(face_value, coupon_rate, price, years):
    if price <= 0 or years <= 0:
        raise ValueError("Price and years must be positive")
    annual_coupon = face_value * coupon_rate
    return float((annual_coupon + (face_value - price) / years) / price)


def current_yield(face_value, coupon_rate, price):
    if price <= 0:
        raise ValueError("Price must be positive")
    return float(face_value * coupon_rate / price)


def yield_to_maturity(price, face_value, coupon_rate, years, frequency=2):
    return coupon_bond_yield(price, face_value, coupon_rate, years, frequency)


def yield_to_call(price, face_value, coupon_rate, call_price, years_to_call, frequency=2):
    if price <= 0 or face_value <= 0 or call_price <= 0 or frequency <= 0 or years_to_call <= 0:
        raise ValueError("Prices, face value, frequency, and years must be positive")
    periods = int(years_to_call * frequency)
    coupon = face_value * coupon_rate / frequency

    def price_at(yield_rate):
        discount = 1 + yield_rate / frequency
        return sum(coupon / discount**period for period in range(1, periods + 1)) + call_price / discount**periods

    return float(brentq(lambda yield_rate: price_at(yield_rate) - price, -0.9999, 100))


def yield_to_worst(price, face_value, coupon_rate, years, call_options=None, frequency=2):
    yields = [yield_to_maturity(price, face_value, coupon_rate, years, frequency)]
    for call_price, years_to_call in call_options or []:
        yields.append(yield_to_call(price, face_value, coupon_rate, call_price, years_to_call, frequency))
    return float(min(yields))


def g_spread(bond_yield, government_yield):
    return float(bond_yield - government_yield)


def z_spread(price, cash_flows, spot_rates, periods):
    cash_flows = np.asarray(cash_flows, dtype=float)
    spot_rates = np.asarray(spot_rates, dtype=float)
    periods = np.asarray(periods, dtype=float)
    if not (cash_flows.size == spot_rates.size == periods.size) or cash_flows.size == 0:
        raise ValueError("Cash flows, spot rates, and periods must have the same non-zero length")
    if np.any(periods <= 0):
        raise ValueError("Periods must be positive")

    def spread_price(spread):
        return float(np.sum(cash_flows / (1 + spot_rates + spread) ** periods))

    return float(brentq(lambda spread: spread_price(spread) - price, -0.9999, 100))


def option_adjusted_spread(z_spread_value, option_value, price, effective_duration):
    """Approximate OAS by removing the option cost from the Z-spread."""
    if price <= 0 or effective_duration <= 0:
        raise ValueError("Price and effective duration must be positive")
    return float(z_spread_value - option_value / (price * effective_duration))


def i_spread(bond_yield, swap_rate):
    return float(bond_yield - swap_rate)


def constant_growth_implied_return(price, next_dividend, growth_rate):
    if price <= 0:
        raise ValueError("Price must be positive")
    return float(next_dividend / price + growth_rate)


def pe_ratio(price, earnings_per_share):
    if earnings_per_share == 0:
        raise ValueError("Earnings per share must be non-zero")
    return float(price / earnings_per_share)


def forward_pe_ratio(price, forward_earnings_per_share):
    if forward_earnings_per_share == 0:
        raise ValueError("Forward earnings per share must be non-zero")
    return float(price / forward_earnings_per_share)


def dividend_payout_ratio(dividends, net_income):
    if net_income == 0:
        raise ValueError("Net income must be non-zero")
    return float(dividends / net_income)


def cash_flow_additivity(cash_flows, rate):
    flows = np.asarray(cash_flows, dtype=float)
    present_values = np.array([present_value(cash_flow, rate, period) for period, cash_flow in enumerate(flows)])
    return float(np.sum(present_values))


def portfolio_metrics(weights, returns, risk_free_rate=0.0):
    weights = np.asarray(weights, dtype=float)
    observations = np.asarray(returns, dtype=float)
    portfolio_returns = observations @ weights
    mean_return = float(np.mean(portfolio_returns))
    volatility = float(np.std(portfolio_returns, ddof=1))
    sharpe = (mean_return - risk_free_rate) / volatility if volatility else 0.0
    return mean_return, volatility, sharpe


def portfolio_return(weights, expected_returns):
    weights = np.asarray(weights, dtype=float)
    expected_returns = np.asarray(expected_returns, dtype=float)
    if weights.size != expected_returns.size:
        raise ValueError("Weights and expected returns must have the same length")
    return float(weights @ expected_returns)


def average_squared_deviation(values, mean_value=None):
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        raise ValueError("At least one observation is required")
    center = np.mean(values) if mean_value is None else mean_value
    return float(np.mean((values - center) ** 2))


def covariance(first_returns, second_returns):
    first = np.asarray(first_returns, dtype=float)
    second = np.asarray(second_returns, dtype=float)
    if first.size != second.size or first.size < 2:
        raise ValueError("Return series must have the same length and at least two observations")
    return float(np.cov(first, second, ddof=1)[0, 1])


def correlation_coefficient(first_returns, second_returns):
    first = np.asarray(first_returns, dtype=float)
    second = np.asarray(second_returns, dtype=float)
    if np.std(first, ddof=1) == 0 or np.std(second, ddof=1) == 0:
        raise ValueError("Correlation requires non-zero variation in both series")
    return float(np.corrcoef(first, second)[0, 1])


def portfolio_variance(weights, covariance_matrix):
    weights = np.asarray(weights, dtype=float)
    matrix = np.asarray(covariance_matrix, dtype=float)
    if matrix.shape != (weights.size, weights.size):
        raise ValueError("Covariance matrix dimensions must match weights")
    return float(weights @ matrix @ weights)


def two_asset_portfolio_variance(weight_one, weight_two, variance_one, variance_two, covariance_between):
    return float(
        weight_one**2 * variance_one
        + weight_two**2 * variance_two
        + 2 * weight_one * weight_two * covariance_between
    )


def portfolio_standard_deviation(variance):
    if variance < 0:
        raise ValueError("Variance cannot be negative")
    return float(np.sqrt(variance))


def global_minimum_variance_portfolio(covariance_matrix):
    matrix = np.asarray(covariance_matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Covariance matrix must be square")
    ones = np.ones(matrix.shape[0])
    inverse_times_ones = np.linalg.solve(matrix, ones)
    weights = inverse_times_ones / (ones @ inverse_times_ones)
    variance = portfolio_variance(weights, matrix)
    return weights, variance, portfolio_standard_deviation(variance)


def capital_market_line_return(risk_free_rate, market_return, market_standard_deviation, portfolio_standard_deviation_value):
    if market_standard_deviation <= 0:
        raise ValueError("Market standard deviation must be positive")
    return float(risk_free_rate + (market_return - risk_free_rate) * portfolio_standard_deviation_value / market_standard_deviation)


def capital_market_line_risk(risk_free_rate, market_return, market_standard_deviation, portfolio_return_value):
    market_premium = market_return - risk_free_rate
    if market_premium == 0:
        raise ValueError("Market return must differ from the risk-free rate")
    return float((portfolio_return_value - risk_free_rate) * market_standard_deviation / market_premium)


def beta(asset_returns, market_returns):
    market_variance = average_squared_deviation(market_returns)
    if market_variance == 0:
        raise ValueError("Market returns must have non-zero variance")
    return float(covariance(asset_returns, market_returns) / market_variance)


def security_market_line_return(risk_free_rate, beta_value, market_return):
    return float(risk_free_rate + beta_value * (market_return - risk_free_rate))


def sharpe_ratio(portfolio_return_value, risk_free_rate, portfolio_standard_deviation_value):
    if portfolio_standard_deviation_value <= 0:
        raise ValueError("Portfolio standard deviation must be positive")
    return float((portfolio_return_value - risk_free_rate) / portfolio_standard_deviation_value)


def treynor_ratio(portfolio_return_value, risk_free_rate, beta_value):
    if beta_value == 0:
        raise ValueError("Beta must be non-zero")
    return float((portfolio_return_value - risk_free_rate) / beta_value)


def msquared_ratio(portfolio_return_value, risk_free_rate, portfolio_standard_deviation_value, market_standard_deviation):
    return float(risk_free_rate + sharpe_ratio(portfolio_return_value, risk_free_rate, portfolio_standard_deviation_value) * market_standard_deviation)


def jensens_alpha(portfolio_return_value, risk_free_rate, beta_value, market_return):
    return float(portfolio_return_value - security_market_line_return(risk_free_rate, beta_value, market_return))


def dupont_roe(net_margin, asset_turnover, equity_multiplier):
    return float(net_margin * asset_turnover * equity_multiplier)


def gordon_growth_value(dividend, required_return, growth_rate):
    if required_return <= growth_rate:
        raise ValueError("Required return must exceed growth rate")
    return float(dividend * (1 + growth_rate) / (required_return - growth_rate))


def wacc(cost_of_equity, after_tax_cost_of_debt, equity_value, debt_value):
    total = equity_value + debt_value
    return float(cost_of_equity * equity_value / total + after_tax_cost_of_debt * debt_value / total)


def capital_structure_weights(debt_value, equity_value, preferred_value=0.0):
    total = debt_value + equity_value + preferred_value
    if total <= 0 or min(debt_value, equity_value, preferred_value) < 0:
        raise ValueError("Capital values must be non-negative and total capital positive")
    return float(debt_value / total), float(equity_value / total), float(preferred_value / total)


def after_tax_cost_of_debt(cost_of_debt, tax_rate):
    if not 0 <= tax_rate <= 1:
        raise ValueError("Tax rate must be between 0 and 100%")
    return float(cost_of_debt * (1 - tax_rate))


def capital_structure_wacc(debt_weight, equity_weight, preferred_weight, cost_of_debt, cost_of_equity, cost_of_preferred, tax_rate):
    if min(debt_weight, equity_weight, preferred_weight) < 0 or not np.isclose(debt_weight + equity_weight + preferred_weight, 1):
        raise ValueError("Capital weights must be non-negative and sum to one")
    return float(
        debt_weight * after_tax_cost_of_debt(cost_of_debt, tax_rate)
        + equity_weight * cost_of_equity
        + preferred_weight * cost_of_preferred
    )


def optimal_capital_structure(debt_weights, wacc_values):
    debt_weights = np.asarray(debt_weights, dtype=float)
    wacc_values = np.asarray(wacc_values, dtype=float)
    if debt_weights.size == 0 or debt_weights.size != wacc_values.size:
        raise ValueError("Debt weights and WACC values must have the same non-zero length")
    index = int(np.argmin(wacc_values))
    return float(debt_weights[index]), float(wacc_values[index])


def cost_of_equity_capm(risk_free_rate, beta_value, market_return):
    return float(risk_free_rate + beta_value * (market_return - risk_free_rate))


def cost_of_preferred_stock(preferred_dividend, preferred_price):
    if preferred_dividend < 0 or preferred_price <= 0:
        raise ValueError("Preferred dividend must be non-negative and price positive")
    return float(preferred_dividend / preferred_price)


def interest_coverage(ebit, interest_expense):
    if interest_expense <= 0:
        raise ValueError("Interest expense must be positive")
    return float(ebit / interest_expense)


def financial_leverage(ebit, interest_expense):
    if ebit <= interest_expense:
        raise ValueError("EBIT must exceed interest expense")
    return float(ebit / (ebit - interest_expense))


def operating_leverage(contribution_margin, ebit):
    if ebit <= 0:
        raise ValueError("EBIT must be positive")
    return float(contribution_margin / ebit)


def value_of_firm(debt_value, equity_value):
    if min(debt_value, equity_value) < 0:
        raise ValueError("Debt and equity values must be non-negative")
    return float(debt_value + equity_value)


def unlevered_firm_value(nopat, unlevered_cost_of_capital):
    if nopat < 0 or unlevered_cost_of_capital <= 0:
        raise ValueError("NOPAT must be non-negative and cost of capital positive")
    return float(nopat / unlevered_cost_of_capital)


def levered_firm_value(unlevered_value, present_value_tax_shield):
    if unlevered_value < 0 or present_value_tax_shield < 0:
        raise ValueError("Firm value and tax shield must be non-negative")
    return float(unlevered_value + present_value_tax_shield)


def lp_preferred_return(lp_contribution, preferred_rate, years=1.0):
    if lp_contribution < 0 or preferred_rate < 0 or years < 0:
        raise ValueError("Contribution, preferred rate, and years must be non-negative")
    return float(lp_contribution * ((1 + preferred_rate) ** years - 1))


def gp_catch_up_clause(lp_preferred_return_value, carried_interest_rate):
    if lp_preferred_return_value < 0 or not 0 <= carried_interest_rate < 1:
        raise ValueError("Preferred return must be non-negative and carried interest below 100%")
    return float(lp_preferred_return_value * carried_interest_rate / (1 - carried_interest_rate))


def private_equity_waterfall(total_distributable, lp_contribution, lp_preferred_return_value, carried_interest_rate):
    if min(total_distributable, lp_contribution, lp_preferred_return_value) < 0 or not 0 <= carried_interest_rate < 1:
        raise ValueError("Amounts must be non-negative and carried interest below 100%")
    capital_return = min(total_distributable, lp_contribution)
    remaining = total_distributable - capital_return
    preferred_paid = min(remaining, lp_preferred_return_value)
    remaining -= preferred_paid
    target_catch_up = gp_catch_up_clause(lp_preferred_return_value, carried_interest_rate)
    catch_up_paid = min(remaining, target_catch_up)
    remaining -= catch_up_paid
    lp_residual = remaining * (1 - carried_interest_rate)
    gp_residual = remaining * carried_interest_rate
    return {
        "lp_capital_return": float(capital_return),
        "lp_preferred_return": float(preferred_paid),
        "gp_catch_up": float(catch_up_paid),
        "lp_residual": float(lp_residual),
        "gp_residual": float(gp_residual),
        "lp_total_distribution": float(capital_return + preferred_paid + lp_residual),
        "gp_total_distribution": float(catch_up_paid + gp_residual),
    }


def lp_distribution(total_distributable, lp_contribution, lp_preferred_return_value, carried_interest_rate):
    return private_equity_waterfall(
        total_distributable, lp_contribution, lp_preferred_return_value, carried_interest_rate
    )["lp_total_distribution"]


def gp_rate_of_return(gp_proceeds, gp_contribution, years=1.0):
    if gp_proceeds < 0 or gp_contribution <= 0 or years <= 0:
        raise ValueError("GP proceeds must be non-negative, contribution positive, and years positive")
    return float((gp_proceeds / gp_contribution) ** (1 / years) - 1)


def multiple_of_invested_capital(total_distributions, invested_capital):
    if total_distributions < 0 or invested_capital <= 0:
        raise ValueError("Distributions must be non-negative and invested capital positive")
    return float(total_distributions / invested_capital)


def return_to_investors(total_distributions, invested_capital):
    return multiple_of_invested_capital(total_distributions, invested_capital) - 1


def leveraged_rate_of_return(asset_return, leverage_ratio_value, borrowing_rate=0.0):
    return leveraged_return(asset_return, leverage_ratio_value, borrowing_rate)


def npv(rate, cash_flows):
    return float(sum(cash_flow / (1 + rate) ** period for period, cash_flow in enumerate(cash_flows)))


def irr(cash_flows):
    return money_weighted_return(cash_flows)


def black_scholes_value(spot, strike, rate, volatility, years, option="Call"):
    if min(spot, strike, volatility, years) <= 0:
        raise ValueError("Spot, strike, volatility, and years must be positive")
    d1 = (log(spot / strike) + (rate + volatility**2 / 2) * years) / (volatility * sqrt(years))
    d2 = d1 - volatility * sqrt(years)
    call = spot * norm.cdf(d1) - strike * exp(-rate * years) * norm.cdf(d2)
    return float(call if option.lower() == "call" else call - spot + strike * exp(-rate * years))
