from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import brentq

import scipy as sq
import seaborn as sns
from matplotlib import pyplot as plt
import streamlit as st
from datetime import datetime
import time

import time
import yfinance as yf
import pandas as pd

# Columns produced by the implied-volatility step (kept as a constant so an
# empty result still has the right schema for downstream code).
IV_COLUMNS = [
    "ContractSymbol", "StrikePrice", "TimeToExpiry", "ImpliedVolatility",
    "OptionType", "Expiration", "Volume", "OpenInterest", "SpreadPct",
]


@st.cache_data(show_spinner="Fetching spot price…", ttl=900)
def get_stock_data(ticker_symbol="SPY", period="5d"):
    """Fetch recent price history and derive the spot price.

    Cached per (ticker, period) for 15 min. A single ``history`` call covers
    both needs, so the old duplicate 1d request is gone. Raises ValueError on
    an unknown / empty ticker so callers can show a friendly message.
    """
    hist = yf.Ticker(ticker_symbol).history(period=period)
    if hist.empty or "Close" not in hist or hist["Close"].dropna().empty:
        raise ValueError(
            f"No price data available for '{ticker_symbol}'. "
            "Check the ticker symbol or try again later."
        )

    spot_prices = hist["Close"].dropna().to_frame()
    spot_price = float(spot_prices["Close"].iloc[-1])
    return spot_prices, spot_price

@st.cache_data(show_spinner="Fetching option chains…", ttl=900)
def get_options_data(ticker_symbol):
    """Download every call AND put option chain for a ticker, in parallel.

    Keyed by the ticker *string* (hashable) so the whole result is cached.
    Returns a single long DataFrame tagged with an ``optionType`` column
    ('C'/'P') plus the tuple of expiration dates. Chains are fetched
    concurrently, which cuts wall-clock time roughly in proportion to the
    worker count.
    """
    expirations = tuple(yf.Ticker(ticker_symbol).options)
    if not expirations:
        return pd.DataFrame(), expirations

    def fetch(date):
        try:
            # Fresh Ticker per thread avoids sharing a non-thread-safe session.
            chain = yf.Ticker(ticker_symbol).option_chain(date)
            calls = chain.calls.copy()
            calls["optionType"] = "C"
            puts = chain.puts.copy()
            puts["optionType"] = "P"
            both = pd.concat([calls, puts], ignore_index=True)
            both["expiration"] = date
            return both
        except Exception:
            return None

    max_workers = min(8, len(expirations))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        frames = [c for c in executor.map(fetch, expirations)
                  if c is not None and not c.empty]

    options_all = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return options_all, expirations

@st.cache_data(show_spinner=False)
def prepare_options(options_data, spot_price, min_time_to_expiry=0.07):
    """Blend to the out-of-the-money side, add TimeToExpiry / midPrice / liquidity.

    A real vol surface is built from OTM options on each side (OTM puts below
    spot, OTM calls above), because those are the liquid, informative quotes --
    ITM options carry wide spreads and stale last prices. For each strike we
    therefore keep the put when strike <= spot and the call when strike > spot,
    leaving exactly one contract per (expiration, strike).

    Strike-independent, so it runs once on the full chain (not per slider move).
    TimeToExpiry uses a single ``now`` mapped over unique dates -- deterministic
    and cheap. Liquidity columns are carried through so the app can filter them
    in memory without recomputing IV.
    """
    if options_data.empty:
        return options_data

    df = options_data.copy()

    now = datetime.now()
    tte_by_date = {
        date: calculate_time_to_expiration(date, now=now)
        for date in df["expiration"].unique()
    }
    df["TimeToExpiry"] = df["expiration"].map(tte_by_date)
    df = df[df["TimeToExpiry"] >= min_time_to_expiry].copy()

    # OTM blend: puts at/below spot, calls above spot.
    is_otm = np.where(df["optionType"].values == "P",
                      df["strike"].values <= spot_price,
                      df["strike"].values > spot_price)
    df = df[is_otm].copy()

    bid = df["bid"]
    ask = df["ask"]
    mid = 0.5 * (bid + ask)
    quoted = (bid > 0) & (ask > 0)
    # Use the bid/ask midpoint when both sides are quoted, else last traded price.
    df["midPrice"] = np.where(quoted, mid, df["lastPrice"])
    # Relative spread in %, only meaningful when both sides are quoted.
    df["SpreadPct"] = np.where(quoted & (mid > 0), 100.0 * (ask - bid) / mid, np.nan)
    df["Volume"] = df.get("volume", pd.Series(index=df.index, dtype=float)).fillna(0)
    df["OpenInterest"] = df.get("openInterest", pd.Series(index=df.index, dtype=float)).fillna(0)

    return df.reset_index(drop=True)

def filter_iv_data(iv_data, min_strike_price, max_strike_price,
                   min_volume=0, min_open_interest=0, max_spread_pct=None):
    """Filter an IV table by strike window and liquidity (cheap, in-memory).

    Rows whose spread is unknown (last-price-only quotes) are kept regardless of
    ``max_spread_pct`` -- we simply can't assess their spread.
    """
    if iv_data.empty:
        return iv_data

    mask = (
        (iv_data["StrikePrice"] >= min_strike_price)
        & (iv_data["StrikePrice"] <= max_strike_price)
        & (iv_data["Volume"] >= min_volume)
        & (iv_data["OpenInterest"] >= min_open_interest)
    )
    if max_spread_pct is not None:
        mask &= iv_data["SpreadPct"].isna() | (iv_data["SpreadPct"] <= max_spread_pct)

    return iv_data[mask].reset_index(drop=True)

def get_option_chains_spot(ticker_symbol, retries=3, delay=2):
    # Fetch the ticker data
    ticker = yf.Ticker(ticker_symbol)
    for attempt in range(retries):
        try:
            # Get the historical spot price
            history = ticker.history(period="1d")

            # Check if the history DataFrame is empty
            if history.empty:
                raise ValueError(f"No historical data available for ticker {ticker_symbol}.")

            # Get the spot price from the history DataFrame
            spot_price = history["Close"].iloc[0]

            # Get expiration dates
            expiration_dates = ticker.options  # Expiration dates

            # Fetch call and put options for each expiration date
            calls_dict = {date: ticker.option_chain(date).calls for date in expiration_dates}
            puts_dict = {date: ticker.option_chain(date).puts for date in expiration_dates}

            # Add expiration column to each DataFrame in calls_dict and puts_dict
            for date, df in calls_dict.items():
                df['expiration'] = date

            for date, df in puts_dict.items():
                df['expiration'] = date

            # Concatenate all DataFrames from calls_dict and puts_dict
            calls_all = pd.concat(calls_dict.values(), ignore_index=True)
            puts_all = pd.concat(puts_dict.values(), ignore_index=True)

            # For calls_all DataFrame
            calls_all = calls_all[["strike", "lastPrice", "impliedVolatility", "expiration"]]
            calls_all["time_to_expiration"] = calls_all["expiration"].apply(calculate_time_to_expiration)
            calls_all = calls_all[calls_all["time_to_expiration"] > 0.0]
            calls_all = calls_all.reset_index(drop=True)

            # For puts_all DataFrame
            puts_all = puts_all[["strike", "lastPrice", "impliedVolatility", "expiration"]]
            puts_all["time_to_expiration"] = puts_all["expiration"].apply(calculate_time_to_expiration)
            puts_all = puts_all[puts_all["time_to_expiration"] > 0.0]
            puts_all = puts_all.reset_index(drop=True)

            # If successful, return the data
            return calls_all, puts_all, spot_price

        except (IndexError, ValueError) as e:
            # Print a warning and retry after a delay
            print(f"Attempt {attempt + 1} failed with error: {e} - Retrying after {delay} seconds...")
            time.sleep(delay)

    # If all retries fail, raise an error
    raise ValueError(f"Failed to get spot price and options data for ticker {ticker_symbol} after {retries} attempts.")

def Call_BS_Value(S, X, r, T, v, q):
    # Calculates the value of a call option (Black-Scholes formula for call options with dividends)
    # S is the share price at time T
    # X is the strike price
    # r is the risk-free interest rate
    # T is the time to maturity in years (days/365)
    # v is the volatility
    # q is the dividend yield

    if S <= 0 or X <= 0:
        return np.nan

    # If expired or basically expired: price is intrinsic
    if T <= 0:
        return max(S - X, 0.0)

    # If vol is basically zero: BS formula divides by ~0, so handle limit case
    if v <= 0:
        # In the zero-vol limit, the option is worth discounted intrinsic on the forward
        return max(S*np.exp(-q*T) - X*np.exp(-r*T), 0.0)

    d_1 = (np.log(S / X) + (r - q + v ** 2 * 0.5) * T) / (v * np.sqrt(T))
    d_2 = d_1 - v * np.sqrt(T)
    return S * np.exp(-q * T) * norm.cdf(d_1) - X * np.exp(-r * T) * norm.cdf(d_2)

def call_price_bounds(S, X, r, T, q):
    lower = max(S*np.exp(-q*T) - X*np.exp(-r*T), 0.0)
    upper = S*np.exp(-q*T)
    return lower, upper

def put_price_bounds(S, X, r, T, q):
    lower = max(X*np.exp(-r*T) - S*np.exp(-q*T), 0.0)
    upper = X*np.exp(-r*T)
    return lower, upper

def Call_IV(S, X, r, T, Call_Price, q, a=1e-6, b=5.0, xtol=1e-6):
    # Calculates the implied volatility for a call option with Brent's method
    # The first four parameters are explained in the Call_BS_Value function
    # Call_Price is the price of the call option
    # q is the dividend yield
    # Last three variables are needed for Brent's method
    if T <= 0 or S <= 0 or X <= 0:
        return np.nan

    low, high = call_price_bounds(S, X, r, T, q)
    if not (low <= Call_Price <= high):
        return np.nan

    def fcn(v):
        return Call_Price - Call_BS_Value(S, X, r, T, v, q)

    try:
        result = brentq(fcn, a=a, b=b, xtol=xtol)
        return np.nan if result <= xtol else result
    except ValueError:
        return np.nan

def Put_BS_Value(S, X, r, T, v, q):
    # Calculates the value of a put option (Black-Scholes formula for put options with dividends)
    # The parameters are explained in the Call_BS_Value function

    if S <= 0 or X <= 0:
        return np.nan
    if T <= 0:
        return max(X - S, 0.0)
    if v <= 0:
        return max(X*np.exp(-r*T) - S*np.exp(-q*T), 0.0)

    d_1 = (np.log(S / X) + (r - q + v ** 2 * 0.5) * T) / (v * np.sqrt(T))
    d_2 = d_1 - v * np.sqrt(T)
    return X * np.exp(-r * T) * norm.cdf(-d_2) - S * np.exp(-q * T) * norm.cdf(-d_1)

def Put_IV(S, X, r, T, Put_Price, q, a=1e-6, b=5.0, xtol=1e-6):
    # Calculates the implied volatility for a put option with Brent's method
    # The first four parameters are explained in the Call_BS_Value function
    # Put_Price is the price of the put option
    # q is the dividend yield
    # Last three variables are needed for Brent's method
    if T <= 0 or S <= 0 or X <= 0:
        return np.nan

    low, high = put_price_bounds(S, X, r, T, q)
    if not (low <= Put_Price <= high):
        return np.nan

    def fcn(v):
        return Put_Price - Put_BS_Value(S, X, r, T, v, q)

    try:
        result = brentq(fcn, a=a, b=b, xtol=xtol)
        return np.nan if result <= xtol else result
    except ValueError:
        return np.nan

def Calculate_IV_Call_Put(S, X, r, T, Option_Price, Put_or_Call, q):
    # This is a general function witch summarizes Call_IV and Put_IV (delivers the same results)
    # Can be used for a Lambda function within Pandas
    # The first four parameters are explained in the Call_BS_Value function
    # Put_or_Call:
    # 'C' returns the implied volatility of a call
    # 'P' returns the implied volatility of a put
    # Option_Price is the price of the option.
    # q is the dividend yield

    pc = str(Put_or_Call).upper()
    if pc == 'C':
        return Call_IV(S, X, r, T, Option_Price, q)
    if pc == 'P':
        return Put_IV(S, X, r, T, Option_Price, q)
    else:
        return np.nan

@st.cache_data(show_spinner="Computing implied volatilities…")
def calculate_implied_volatility(prepared_options, spot_price, risk_free_rate, dividend_yield):
    """Solve Black-Scholes implied vol for every OTM option in the chain.

    Uses the put inverter for puts and the call inverter for calls. Depends only
    on (chain, spot, r, q) -- NOT on the strike / liquidity sliders -- so it is
    computed once per parameter set and cached; the app then filters the result
    in memory.
    """
    if prepared_options.empty:
        return pd.DataFrame(columns=IV_COLUMNS)

    S = float(spot_price)
    symbols = prepared_options["contractSymbol"].to_numpy()
    strikes = prepared_options["strike"].to_numpy(dtype=float)
    times = prepared_options["TimeToExpiry"].to_numpy(dtype=float)
    prices = prepared_options["midPrice"].to_numpy(dtype=float)
    kinds = prepared_options["optionType"].to_numpy()
    expirations = prepared_options["expiration"].to_numpy()
    volumes = prepared_options["Volume"].to_numpy(dtype=float)
    ois = prepared_options["OpenInterest"].to_numpy(dtype=float)
    spreads = prepared_options["SpreadPct"].to_numpy(dtype=float)

    rows = []
    for sym, strike, T, price, kind, exp, vol, oi, spr in zip(
        symbols, strikes, times, prices, kinds, expirations, volumes, ois, spreads
    ):
        if not (np.isfinite(price) and price > 0):
            continue
        if not (np.isfinite(T) and T > 0):
            continue
        iv = Calculate_IV_Call_Put(S, strike, risk_free_rate, T, price, kind, dividend_yield)
        if np.isfinite(iv):
            rows.append((sym, strike, T, iv, kind, exp, vol, oi, spr))

    return pd.DataFrame(rows, columns=IV_COLUMNS)

# Black-scholes-merton (1973)
def bs_price(S, K, T, r, sigma, option="call"):
    S_arr, K_arr, T_arr, r_arr, sigma_arr = np.broadcast_arrays(
        np.asarray(S, dtype=float),
        np.asarray(K, dtype=float),
        np.asarray(T, dtype=float),
        np.asarray(r, dtype=float),
        np.asarray(sigma, dtype=float),
    )

    sigma_arr = np.where(sigma_arr <= 1e-8, 1e-8, sigma_arr)
    T_arr = np.where(T_arr <= 1e-8, 1e-8, T_arr)

    d1 = (np.log(S_arr / K_arr) + (r_arr + 0.5 * sigma_arr**2) * T_arr) / (sigma_arr * np.sqrt(T_arr))
    d2 = d1 - sigma_arr * np.sqrt(T_arr)

    call = S_arr * norm.cdf(d1) - K_arr * np.exp(-r_arr * T_arr) * norm.cdf(d2)
    put = K_arr * np.exp(-r_arr * T_arr) * norm.cdf(-d2) - S_arr * norm.cdf(-d1)

    if option == "call":
        return call
    if option == "put":
        return put
    raise ValueError("option must be 'call' or 'put'")

def call_bs_value(S, X, r, T, v, q):
    # Calculates the value of a call option (Black-Scholes formula for call options with dividends)
    # S is the share price at time T
    # X is the strike price
    # r is the risk-free interest rate
    # T is the time to maturity in years (days/365)
    # v is the volatility
    # q is the dividend yield
    d_1 = (np.log(S / X) + (r - q + v ** 2 * 0.5) * T) / (v * np.sqrt(T))
    d_2 = d_1 - v * np.sqrt(T)
    return S * np.exp(-q * T) * norm.cdf(d_1) - X * np.exp(-r * T) * norm.cdf(d_2)

def put_bs_value(S, X, r, T, v, q):
    # Calculates the value of a put option (Black-Scholes formula for put options with dividends)
    # The parameters are explained in the Call_BS_Value function
    d_1 = (np.log(S / X) + (r - q + v ** 2 * 0.5) * T) / (v * np.sqrt(T))
    d_2 = d_1 - v * np.sqrt(T)
    return X * np.exp(-r * T) * norm.cdf(-d_2) - S * np.exp(-q * T) * norm.cdf(-d_1)


def bs_greeks(S, K, T, r, sigma, q=0.0):
    S_arr, K_arr, T_arr, r_arr, sigma_arr, q_arr = np.broadcast_arrays(
        np.asarray(S, dtype=float),
        np.asarray(K, dtype=float),
        np.asarray(T, dtype=float),
        np.asarray(r, dtype=float),
        np.asarray(sigma, dtype=float),
        np.asarray(q, dtype=float),
    )

    sigma_arr = np.where(sigma_arr <= 1e-8, 1e-8, sigma_arr)
    T_arr = np.where(T_arr <= 1e-8, 1e-8, T_arr)

    d1 = (np.log(S_arr / K_arr) + (r_arr - q_arr + 0.5 * sigma_arr**2) * T_arr) / (sigma_arr * np.sqrt(T_arr))
    d2 = d1 - sigma_arr * np.sqrt(T_arr)

    # Delta (with continuous dividend yield q)
    delta_call = np.exp(-q_arr * T_arr) * norm.cdf(d1)
    delta_put = np.exp(-q_arr * T_arr) * (norm.cdf(d1) - 1.0)

    # Gamma and Vega (both include the exp(-qT) factor for underlying paying dividends)
    gamma = np.exp(-q_arr * T_arr) * norm.pdf(d1) / (S_arr * sigma_arr * np.sqrt(T_arr))
    vega = S_arr * np.exp(-q_arr * T_arr) * np.sqrt(T_arr) * norm.pdf(d1)

    # Theta (per year). Include dividend yield contributions for theta.
    theta_common = -(S_arr * np.exp(-q_arr * T_arr) * norm.pdf(d1) * sigma_arr) / (2.0 * np.sqrt(T_arr))
    theta_call = theta_common - r_arr * K_arr * np.exp(-r_arr * T_arr) * norm.cdf(d2) + q_arr * S_arr * np.exp(-q_arr * T_arr) * norm.cdf(d1)
    theta_put = theta_common + r_arr * K_arr * np.exp(-r_arr * T_arr) * norm.cdf(-d2) - q_arr * S_arr * np.exp(-q_arr * T_arr) * norm.cdf(-d1)

    # Rho (interest rate sensitivity)
    rho_call = K_arr * T_arr * np.exp(-r_arr * T_arr) * norm.cdf(d2)
    rho_put = -K_arr * T_arr * np.exp(-r_arr * T_arr) * norm.cdf(-d2)

    return {
        "delta_call": delta_call,
        "delta_put": delta_put,
        "gamma": gamma,
        "vega": vega,
        "theta_call": theta_call,
        "theta_put": theta_put,
        "rho_call": rho_call,
        "rho_put": rho_put,
    }



def calculate_greeks(S, K, r, T, sigma, dividend_yield=0.0):
    """
    Calculate the Greeks for a European option using the Black-Scholes model.

    Parameters:
    S (float): Current stock price
    K (float): Strike price
    r (float): Risk-free interest rate (as a decimal)
    T (float): Time to expiration in years
    sigma (float): Volatility of the underlying asset (as a decimal)
    dividend_yield (float): Dividend yield of the underlying asset (as a decimal)

    Returns:
    tuple: A tuple containing the Greeks in the following order:
        delta_call, delta_put, gamma, vega, theta_call, theta_put, rho_call, rho_put
    """
    # Pass dividend yield through to the underlying BS greeks implementation.
    greeks = bs_greeks(S, K, T, r, sigma, q=dividend_yield)
    return (
        greeks["delta_call"],
        greeks["delta_put"],
        greeks["gamma"],
        greeks["vega"],
        greeks["theta_call"],
        greeks["theta_put"],
        greeks["rho_call"],
        greeks["rho_put"],
    )


def calculate_time_to_expiration(expiration_date_str: str, now: datetime = None) -> float:
    """
    Calculate the time to expiration in years from today.

    Parameters:
    expiration_date_str (str): Expiration date in the format 'YYYY-MM-DD'

    Returns:
    float: Time to expiration in years
    """
    # Parse the expiration date string to a datetime object
    expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d")

    # Get today's date
    current_date = datetime.now()

    # Calculate the number of days to expiration
    days_to_expiration = (expiration_date - current_date).days

    # Convert days to years (use 365 for simplicity)
    T = days_to_expiration / 365.0

    return T


def calculate_option_values(min_spot, max_spot, min_vol, max_vol, strike_price, risk_free_rate, time_to_maturity, dividend_yield, purchase_price):
    spot_interval = np.round(np.linspace(min_spot, max_spot, 11), 2)
    vol_interval = np.round(np.linspace(min_vol, max_vol, 11), 2)

    call_values = np.zeros((len(vol_interval), len(spot_interval)))
    put_values = np.zeros((len(vol_interval), len(spot_interval)))

    call_pnl = np.zeros((len(vol_interval), len(spot_interval)))
    put_pnl = np.zeros((len(vol_interval), len(spot_interval)))

    for i, spot in enumerate(spot_interval):
        for j, vol in enumerate(vol_interval):
            call_values[j, i] = call_bs_value(spot, strike_price, risk_free_rate, time_to_maturity, vol, dividend_yield)
            put_values[j, i] = put_bs_value(spot, strike_price, risk_free_rate, time_to_maturity, vol, dividend_yield)

            call_pnl[j, i] = call_values[j, i] - purchase_price
            put_pnl[j, i] = put_values[j, i] - purchase_price

    call_df = pd.DataFrame(call_values, index=vol_interval, columns=spot_interval)
    put_df = pd.DataFrame(put_values, index=vol_interval, columns=spot_interval)

    call_pnl_df = pd.DataFrame(call_pnl, index=vol_interval, columns=spot_interval)
    put_pnl_df = pd.DataFrame(put_pnl, index=vol_interval, columns=spot_interval)

    call_df = call_df.round(2)
    put_df = put_df.round(2)

    call_pnl_df = call_pnl_df.round(2)
    put_pnl_df = put_pnl_df.round(2)

    return call_df, put_df, call_pnl_df, put_pnl_df

def calculate_market_prices(min_spot, max_spot, call_datapoints, put_datapoints, risk_free_rate, dividend_yield):
    spot_interval = np.round(np.linspace(min_spot, max_spot, 11), 2)

    call_vol_interval = call_datapoints["impliedVolatility"].round(2)
    put_vol_interval = put_datapoints["impliedVolatility"].round(2)

    call_values = np.zeros((len(call_vol_interval), len(spot_interval)))
    put_values = np.zeros((len(put_vol_interval), len(spot_interval)))

    for i, spot in enumerate(spot_interval):
        for row in call_datapoints.itertuples():
            call_values[row.Index, i] = call_bs_value(S=spot, X=row.strike, r=risk_free_rate, T=row.time_to_expiration,
                                                      v=row.impliedVolatility, q=dividend_yield) - row.lastPrice

    for i, spot in enumerate(spot_interval):
        for row in put_datapoints.itertuples():
            put_values[row.Index, i] = put_bs_value(S=spot, X=row.strike, r=risk_free_rate, T=row.time_to_expiration,
                                                    v=row.impliedVolatility, q=dividend_yield) - row.lastPrice

    call_df = pd.DataFrame(call_values, index=call_vol_interval, columns=spot_interval)
    put_df = pd.DataFrame(put_values, index=put_vol_interval, columns=spot_interval)

    return call_df, put_df



def implied_volatility(market_price, S, K, T, r, option="call", tol=1e-9, max_iter=100):
    if T <= 0:
        raise ValueError("Time to expiry must be positive")

    lower_bound = 1e-6
    upper_bound = 5.0

    if option == "call":
        lower_price = max(0.0, S - K * np.exp(-r * T))
    elif option == "put":
        lower_price = max(0.0, K * np.exp(-r * T) - S)
    else:
        raise ValueError("option must be 'call' or 'put'")

    upper_price = max(S, K)
    if market_price < lower_price or market_price > upper_price:
        raise ValueError("market price is outside the feasible price range")

    for _ in range(max_iter):
        mid = 0.5 * (lower_bound + upper_bound)
        price = bs_price(S, K, T, r, mid, option=option)
        if price > market_price:
            upper_bound = mid
        else:
            lower_bound = mid
        if abs(upper_bound - lower_bound) < tol:
            break

    return 0.5 * (lower_bound + upper_bound)


def build_fallback_price_history(ticker, periods=252):
    dates = pd.date_range("2023-01-01", periods=periods, freq="D")
    close = np.exp(np.cumsum(np.random.normal(0.001, 0.02, periods)))
    price_history = pd.DataFrame({"close": close}, index=dates)
    price_history.index.name = "date"
    return price_history


def load_price_history(ticker, start_date="2023-01-01", end_date="2024-01-01"):
    try:
        import yfinance as yf
    except Exception:
        yf = None

    if yf is None:
        return build_fallback_price_history(ticker)

    try:
        raw = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)
    except Exception:
        return build_fallback_price_history(ticker)

    if raw is None or raw.empty:
        return build_fallback_price_history(ticker)

    close_series = raw.get("Close") if isinstance(raw, pd.DataFrame) else None
    if close_series is None:
        close_series = raw.iloc[:, 0] if hasattr(raw, "iloc") else raw

    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]

    if not isinstance(close_series, pd.Series):
        close_series = pd.Series(close_series, name="close")

    price_history = close_series.dropna().to_frame(name="close")
    price_history.index.name = "date"
    return price_history


def build_market_inputs(price_history, ticker):
    if price_history is None or price_history.empty:
        price_history = build_fallback_price_history(ticker)

    returns = np.log(price_history["close"] / price_history["close"].shift(1)).dropna()
    annualized_vol = float(returns.std() * np.sqrt(252)) if len(returns) > 1 else 0.2
    spot = float(price_history["close"].iloc[-1])
    strike = round(spot * 1.02, 2)
    expiry = 0.25
    rate = 0.045

    return {
        "ticker": ticker,
        "spot": spot,
        "strike": strike,
        "expiry": expiry,
        "rate": rate,
        "volatility": annualized_vol,
    }


## Black-Scholes-Merton heatmap
def market_heatmaps(call_df, put_df):
    fig, axs = plt.subplots(1, 2, figsize=(20, 10))

    # Plot Call Prices Heatmap
    sns.heatmap(call_df, ax=axs[0], cmap='RdBu', annot=True, cbar=True, fmt=".2f")
    axs[0].set_title('Call Mis-pricing')
    axs[0].set_xlabel('Spot Price')
    axs[0].set_ylabel('Volatility')

    # Plot Put Prices Heatmap
    sns.heatmap(put_df, ax=axs[1], cmap='RdBu', annot=True, cbar=True, fmt=".2f")
    axs[1].set_title('Put Mispricing')
    axs[1].set_xlabel('Spot Price')
    axs[1].set_ylabel('Volatility')

    handles = [
        plt.Line2D([0], [0], color='blue', label='Undervalued (Theoretical > Market)'),
        plt.Line2D([0], [0], color='white', label='Fairly Priced'),
        plt.Line2D([0], [0], color='red', label='Overvalued (Theoretical < Market)')
    ]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3,
               fontsize=22, markerscale=4, frameon=True)

    plt.tight_layout()
    st.pyplot(fig)


def plot_heatmaps(mode, call_df, put_df, call_pnl_df, put_pnl_df):
# def plot_heatmaps(mode, call_df, put_df):
    call_df = call_df.round(2)
    put_df = put_df.round(2)

    fig, axs = plt.subplots(1, 2, figsize=(20, 10))

    if mode == 'Pricing':
        # Plot Call and Put Prices
        sns.heatmap(call_df, ax=axs[0], cmap='viridis', annot=True, cbar=True, fmt=".2f")
        axs[0].set_facecolor('#f5f5f5')
        axs[0].set_title('CALL prices Heatmap')
        axs[0].set_xlabel('Spot Price')
        axs[0].set_ylabel('Volatility')

        sns.heatmap(put_df, ax=axs[1], cmap='viridis', annot=True, cbar=True, fmt=".2f")
        axs[1].set_facecolor('#f5f5f5')
        axs[1].set_title('PUT prices Heatmap')
        axs[1].set_xlabel('Spot Price')
        axs[1].set_ylabel('Volatility')

        # Add Legend for Pricing Mode
        handles = [
            plt.Line2D([0], [0], color='purple', label='Low Prices'),
            plt.Line2D([0], [0], color='green', label='Moderate Prices'),
            plt.Line2D([0], [0], color='yellow', label='High Prices')
        ]
        fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3,
                            fontsize=22, markerscale=4, frameon=True)

    elif mode == 'P&L':
        # Plot Call and Put PnLs
        sns.heatmap(call_pnl_df, ax=axs[0], cmap='RdYlGn', annot=True, cbar=True, fmt=".2f")
        axs[0].set_title('CALL P&Ls')
        axs[0].set_xlabel('Spot Price')
        axs[0].set_ylabel('Volatility')

        sns.heatmap(put_pnl_df, ax=axs[1], cmap='RdYlGn', annot=True, cbar=True, fmt=".2f")
        axs[1].set_title('PUT P&Ls')
        axs[1].set_xlabel('Spot Price')
        axs[1].set_ylabel('Volatility')

        handles = [
            plt.Line2D([0], [0], color='darkred', label='Negative P&L'),
            plt.Line2D([0], [0], color='yellow', label='Breakeven'),
            plt.Line2D([0], [0], color='darkgreen', label='Positive P&L')
        ]
        fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3,
                            fontsize=22, markerscale=4, frameon=True)
    plt.tight_layout()
    st.pyplot(fig)



## Black 76

def black76_price_from_forward(F, K, T, sigma, df=1.0, option="call"):
    """Black (1976) price given forward price F and discount factor df.

    F, K, T, sigma, df are broadcastable to arrays.
    """
    F_arr, K_arr, T_arr, sigma_arr, df_arr = np.broadcast_arrays(
        np.asarray(F, dtype=float),
        np.asarray(K, dtype=float),
        np.asarray(T, dtype=float),
        np.asarray(sigma, dtype=float),
        np.asarray(df, dtype=float),
    )

    sigma_arr = np.where(sigma_arr <= 1e-8, 1e-8, sigma_arr)
    T_arr = np.where(T_arr <= 1e-8, 1e-8, T_arr)

    d1 = (np.log(F_arr / K_arr) + 0.5 * sigma_arr**2 * T_arr) / (sigma_arr * np.sqrt(T_arr))
    d2 = d1 - sigma_arr * np.sqrt(T_arr)

    call = df_arr * (F_arr * norm.cdf(d1) - K_arr * norm.cdf(d2))
    put = df_arr * (K_arr * norm.cdf(-d2) - F_arr * norm.cdf(-d1))

    if option == "call":
        return call
    if option == "put":
        return put
    raise ValueError("option must be 'call' or 'put'")


def black76_price_from_spot(S, K, T, r, sigma, option="call", dividend_yield=0.0):
    """Convenience wrapper: compute forward F from spot S and rates, then price using Black76."""
    # make arrays for broadcasting
    S_arr, K_arr, T_arr, r_arr, sigma_arr = np.broadcast_arrays(
        np.asarray(S, dtype=float),
        np.asarray(K, dtype=float),
        np.asarray(T, dtype=float),
        np.asarray(r, dtype=float),
        np.asarray(sigma, dtype=float),
    )

    F = S_arr * np.exp((r_arr - dividend_yield) * T_arr)
    df = np.exp(-r_arr * T_arr)
    return black76_price_from_forward(F, K_arr, T_arr, sigma_arr, df=df, option=option)


def black76_implied_vol(market_price, F, K, T, df=1.0, option="call", tol=1e-9, max_iter=100):
    """Invert Black (1976) price to find implied volatility using Brent's method.

    Supports scalar or broadcastable array inputs. When inputs are arrays, returns
    a numpy array of implied volatilities with the broadcasted shape.
    """
    # Broadcast inputs
    mp_arr, F_arr, K_arr, T_arr, df_arr = np.broadcast_arrays(
        np.asarray(market_price, dtype=float),
        np.asarray(F, dtype=float),
        np.asarray(K, dtype=float),
        np.asarray(T, dtype=float),
        np.asarray(df, dtype=float),
    )

    if np.any(T_arr <= 0):
        raise ValueError("Time to expiry must be positive")

    # Prepare output array
    out = np.full(mp_arr.shape, np.nan, dtype=float)

    # volatility bracket
    a, b = 1e-6, 5.0

    # iterate elementwise
    it = np.nditer(mp_arr, flags=["multi_index"])
    while not it.finished:
        idx = it.multi_index
        mp = float(mp_arr[idx])
        f = float(F_arr[idx])
        k = float(K_arr[idx])
        t = float(T_arr[idx])
        dff = float(df_arr[idx])

        def price_for_sigma(s):
            return float(black76_price_from_forward(f, k, t, s, df=dff, option=option) - mp)

        try:
            root = brentq(price_for_sigma, a, b, maxiter=max_iter, xtol=tol)
            out[idx] = float(root)
        except Exception:
            out[idx] = np.nan

        it.iternext()

    # Return scalar if inputs were scalar
    if out.shape == ():
        return float(out)
    return out


def black76_implied_vol_from_spot(market_price, S, K, T, r, option="call", dividend_yield=0.0, tol=1e-9, max_iter=100):
    F = S * np.exp((r - dividend_yield) * T)
    df = np.exp(-r * T)
    return black76_implied_vol(market_price, F, K, T, df=df, option=option, tol=tol, max_iter=max_iter)