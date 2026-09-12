import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import streamlit as st
import black_scholes_app as f
import svi

from scipy.interpolate import griddata

st.set_page_config(page_title="Black-Scholes-Merton (1973)", layout="wide")
st.sidebar.title("Quant Research Framework")
st.sidebar.page_link(page="", label="Monte Carlo")
st.sidebar.page_link(page="main.py", label="Black-Scholes-Merton (1973)")
st.sidebar.page_link(page="pages/black.py", label="Black (1976)")
st.sidebar.page_link(page="pages/binomial_tree.py", label="Binomial Tree")
st.sidebar.page_link(page="pages/trinomial_tree.py", label="Trinomial Tree")
st.sidebar.page_link(page="pages/interest_rate_models.py", label="Interest Rate Models")
st.sidebar.page_link(page="pages/american_option_pricing.py", label="American Option Pricing")
st.sidebar.markdown(
    """
    <div style='margin-bottom: 25px;'>
        <!-- <span style='font-weight: bold; font-size: 18px;'>Created by:</span><br> -->
        <a href='https://www.linkedin.com/in/eliaz-simon/' target='_blank' style='text-decoration: none; display: flex; align-items: center; gap: 12px; margin-top: 8px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='32' height='32'/>
            <span style='color: #0A66C2; font-size: 18px; font-weight: bold;'>Eliaz Simon</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

####################################################################################
# American Option Pricing
####################################################################################

# ! Review
# Bjerksund-Stensland (1993)
def bs1993_phi(S, K, T, gamma, H, x, r, b, sigma):
    # Equation 8
	Lambda = -r + gamma * b + 0.5 * gamma * (gamma - 1) * sigma ** 2

	# Equation 9
	kappa = (2 * b / (sigma ** 2)) + (2 * gamma - 1);

	# Equation 7 for the phi function
	d1 = -(((np.log(S/H) + (b+(gamma-0.5)*sigma*sigma)*T)) / (sigma * np.sqrt(T)));
	d2 = -((np.log(x**2/S/H) + (b+(gamma-0.5)*sigma*sigma)*T) / (sigma * np.sqrt(T)));

	# Return phi
	return np.exp(Lambda * T) * np.pow(S,gamma) * (np.cdf(d1) - np.pow(x / S, kappa) * np.cdf(d2));

# ! Review
# def bs1993_option_price(S, K, T, r, sigma, N):
def bs1993_option_price(S, K, T, r, b, sigma):
    if b >= r:
        print("Black Scholes") # Call Black-Scholes equation here and pass as 'call'
        return 0

    # Call price
    beta = ((0.5 - b/(2**sigma)) + (np.sqrt(b/2**sigma - 0.5)**2 + 2*r/sigma**2))

    hT = -(b*T + 2*sigma*np.sqrt(T)) * (2**K/((bInf - b0)*b0))
    bInf = (beta/beta-1)*K
    b0 = np.max(K,(r/r-b)*K)

    XT = b0 + (bInf - b0)  * (1 - np.exp(hT))

    if(S >= XT):
        call_price = S - K
    else:
        aX = (XT - K)*np.pow(XT, -b)
        t = 0.5 * (np.sqrt(5) - 1) * T
        hTt = -(b*(T-t) + 2* sigma * np.sqrt(T-t)) * K * K/b0/(bInf-b0)

        x = b0 + (bInf - b0) * (1 - np.exp(hTt))

        call_price = (aX * np.pow(S, b)) - aX * bs1993_phi(S, t, beta, XT, XT, r, b, sigma) + bs1993_phi(S, t, 1, XT, XT, r, b, sigma) - bs1993_phi(S, t, 1, x, XT, r, b, sigma) - K * bs1993_phi(S, t, 0, XT, XT, r, b, sigma) + K * bs1993_phi(S, t, 0, x, XT, r, b, sigma) + aX * bs1993_phi(S, t, beta, x, XT, r, b, sigma) - aX * bs1993_phi(S, T, beta, x, XT, x, t, r, b, sigma) + bs1993_phi(S, T, 1, x, XT, x, t, r, b, sigma) - bs1993_phi(S, T, 1, K, XT, x, t, r, b, sigma) - K * bs1993_phi(S, T, 0, x, XT, x, t, r, b, sigma) + K * bs1993_phi(S, T, 0, K, XT, x, t, r, b, sigma)

    # return call_price, put_price, stock, call_tree, put_tree
    # return call_price, put_price
    return call_price


# ! Review
def bs2002_phi(S, K, T, gamma, H, x, r, b, sigma):
    # Equation 8
	Lambda = -r + gamma * b + 0.5 * gamma * (gamma - 1) * sigma ** 2

	# Equation 9
	kappa = (2 * b / (sigma ** 2)) + (2 * gamma - 1);

	# Equation 7 for the phi function
	d1 = -(((np.log(S/H) + (b+(gamma-0.5)*sigma*sigma)*T)) / (sigma * np.sqrt(T)));
	d2 = -((np.log(x**2/S/H) + (b+(gamma-0.5)*sigma*sigma)*T) / (sigma * np.sqrt(T)));

	# Return phi
	return np.exp(Lambda * T) * np.pow(S,gamma) * (np.cdf(d1) - np.pow(x / S, kappa) * np.cdf(d2));

def bs2002_psi(S, T, gamma, H, X, x, t, r, b, sigma):
    d1 = -(np.log(S / x) + (b + (gamma - 0.5) * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = -(np.log(X ** 2 / S / x) + (b + (gamma - 0.5) * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d3 = -(np.log(S / x) - (b + (gamma - 0.5) * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d4 = -(np.log(X**2 / S / x) - (b + (gamma - 0.5) * sigma ** 2) * t) / (sigma * np.sqrt(t))

    D1 = -(np.log(S / H) + (b + (gamma - 0.5) * sigma ** 2) * T) / (sigma * np.sqrt(T))
    D2 = -(np.log(X ** 2 / S / H) + (b + (gamma - 0.5) * sigma ** 2) ** T) / (sigma * np.sqrt(T))
    D3 = -(np.log(x ** 2 / S / H) + (b + (gamma - 0.5) * sigma ** 2) * T) / (sigma * np.sqrt(T))
    D4 = -(np.log(S * x ** 2 / H / X / X) + (b + (gamma - 0.5) * sigma ** 2) * T) / (sigma * np.sqrt(T))

    rho = np.sqrt(t / T)

    Lambda = -r + gamma * b + 0.5 * gamma * (gamma - 1) * sigma ** 2
    kappa = 2 * b / sigma / sigma + (2 + gamma - 1)

    return np.exp(Lambda * T) * np.pow(S , gamma) * (
        np.cdf(d1, D1, rho) - np.cdf(d2, D2, rho) * np.pow(X / S, kappa) - np.cdf(d3, D3, -rho) * np.pow(x / S, kappa) + np.cdf(d4, D4, -rho) * np.pow(x / X, kappa)
    )

# Bjerksund-Stensland (2002)
def bs2002_option_price(S, K, T, r, b, sigma):
    if b >= r:
        print("Black Scholes") # Call Black-Scholes equation here and pass as 'call'
        return 0

    # Call price
    beta = ((0.5 - b/(2**sigma)) + (np.sqrt(b/2**sigma - 0.5)**2 + 2*r/sigma**2))

    hT = -(b*T + 2*sigma*np.sqrt(T)) * (2**K/((bInf - b0)*b0))
    bInf = (beta/beta-1)*K
    b0 = np.max(K,(r/r-b)*K)

    XT = b0 + (bInf - b0)  * (1 - np.exp(hT))

    if(S >= XT):
        call_price = S - K
    else:
        aX = (XT - K)*np.pow(XT, -b)
        t = 0.5 * (np.sqrt(5) - 1) * T
        hTt = -(b*(T-t) + 2* sigma * np.sqrt(T-t)) * K * K/b0/(bInf-b0)

        x = b0 + (bInf - b0) * (1 - np.exp(hTt))

        call_price = (aX * np.pow(S, b)) 
        - aX * bs1993_phi(S, t, beta, XT, XT, r, b, sigma) 
        + bs1993_phi(S, t, 1, XT, XT, r, b, sigma) 
        - bs1993_phi(S, t, 1, x, XT, r, b, sigma) 
        - K * bs1993_phi(S, t, 0, XT, XT, r, b, sigma) 
        + K * bs1993_phi(S, t, 0, x, XT, r, b, sigma) 
        + aX * bs1993_phi(S, t, beta, x, XT, r, b, sigma) 
        - aX * bs1993_phi(S, T, beta, x, XT, x, t, r, b, sigma) 
        + bs1993_phi(S, T, 1, x, XT, x, t, r, b, sigma) 
        - bs1993_phi(S, T, 1, K, XT, x, t, r, b, sigma) 
        - K * bs1993_phi(S, T, 0, x, XT, x, t, r, b, sigma) 
        + K * bs1993_phi(S, T, 0, K, XT, x, t, r, b, sigma)

    return call_price

#! REVIEW AND LINK with STREAMLIT WHICH SHOULD USE ONLY S&P500 INDEX
# Brenner and Galai (1989) (VIX)
def bg_option_price(S, K, T, r, sigma, N):
    # import yields
    yields = pd.read_csv("", converters={"Date": lambda x: dt.datetime.strptime(x, "%Y%m%d")})
    yields = yields.set_index(["Date", "Days"])

    # import options
    # - function to parse dates of 20090101 format
    raw_options = pd.read_csv("", converters={"Expiration": lambda x: dt.datetime.strptime(x, "%Y%m%d")})
    # - function to convert days to internal timedelta format
    raw_options["Date"] = raw_options["Expiration"] - raw_options["Days"].map(lambda x: dt.timedelta(days=int(x)))
    # - convert integer strikes to float! Otherwise it may lead to accumulation of errors.
    raw_options["Strike"] = raw_options["Strike"].astype(float)

    # Do some cleaning and indexing
    # - Since VIX is computed for hte date of option quotations, we do not really need Expiration
    options = raw_options.set_index(["Date", "Days", "Strike"]).drop("Expiration", axis=1)
    # - Do some renaming and separate calls from puts
    calls = options[["Call Bid", "Call Ask"]].rename(columns={"Call Bid": "Bid", "Call Ask": "Ask"})
    puts = options[["Put Bid", "Put Ask"]].rename(columns={"Put Bid": "Bid", "Put Ask": "Ask"})
    # - add a column indicating the type of the option
    calls["CP"], puts["CP"] = "C", "P"
    # - Merge calls and puts
    options = pd.concat ([calls, puts])
    # - Reindex and sort
    options = options.reset_index().set_index(["Date", "Days", "CP", "Strike"]).sort_index()
    # options.head()

    # Compute bid/ask average
    # This step is used further to filter out in-the-mone yoptions
    options["Premium"] = (options["Bid"] + options["Ask"]) / 2
    options2 = options[options["Bid"] > 0]["Premium"].unstack("CP")
    # options2.dropna().head()

    # Determine minimum difference
    # - find the absolute difference
    options2["CPdiff"] = (options2["C"] - options2["P"]).abs()
    # - mark the minimum for each date / term
    options2["min"] = options2["CPdiff"].groupby(level=["Date", "Days"]).transform(lambda x : x == x.min())
    # options2.dropna().head()

    # Compute forward price
    # - leave only at-the-money options
    df = options2[options2["min"] == 1].reset_index()
    # - merge with risk-free rate
    df = pd.merge(df, yields.reset_index(), how="left")
    # - compute the implied forward
    df["Forward"] = df["CPdiff"] * np.exp(df["Rate"] * df["Days"] / 36500)
    df["Forward"] += df["Strike"]
    forward = df.set_index (["Date", "Days"])[["Forward"]]
    # forward.head()


    # Compute at-the-money strike
    # - Merge options with implied forward price
    left = options2.reset_index().set_index(["Date", "Days"])
    df = pd.merge(left, forward, left_index=True, right_index=True)
    # - compute at the money-strike
    mid_strike = df[df["Strike"] < df["Forward"]]["Strike"].groupby(level={"Date", "Days"}).max()
    mid_strike = pd.DataFrame({"Mid Strike": mid_strike})
    # mid_strike.head()


    # Separate out-of-the-money calls and puts
    # - Go back to original data and reindex it
    left = options.reset_index().set_index(["Date", "Days"]).drop("Premium", axis=1)
    # - merge with at-the-money strike
    df = pd.merge(left, mid_strike, left_index=True, right_index=True)
    # - separate out-of-the-money calls and puts
    P = (df["Strike"] <= df["Mid Strike"]) & (df["CP"] == "P")
    C = (df["Strike"] >= df["Mid Strike"]) & (df["CP"] == "C")
    puts, calls = df[P], df[C]
    # puts.tail()
    # calls.head()


    # Remove all quotes after two consecutive zero bids
    # - Indicator of zero bid
    calls = calls.assign(zero_bid=lambda df: (df["Bid"] == 0).astype(int))
    # - accumulate number of ero bids starting at-the-money
    calls["zero_bid_accum"] = calls.groupby(level=["Date", "Days"])["zero_bid"].cumsum()
    # - sort puts in reverse order inside date/term
    puts = puts.groupby(level=["Date", "Days"]).apply(lambda x: x.sort_values(["Strike"], ascending=False))
    # # - indicator of zero bid 
    puts = puts.assign(zero_bid=lambda df: (df["Bid"] == 0).astype(int))
    # # - accumulate number of zero bids starting at-the-money
    puts["zero_bid_accum"] = puts.groupby(level=["Date", "Days"])["zero_bid"].cumsum()
    # 
    # calls[(calls["Strike"] >= 1210) & (calls["Strike"] <= 1240)].head()


    # - merge puts and cals
    option3 = pd.concat([calls, puts]).reset_index()
    # - throw away bad stuff
    options3 = options3[(options3["zero_bid_accum"] < 2) & (options3["Bid"] > 0)]
    # - compute option premium as bid/ask average
    options3["Premium"] = (options3["Bid"] + options3["Ask"]) / 2
    options3 = options3.set_index(["Date", "Days", "CP", "Strike"])["Premium"].unstack("CP")
    # options3.dropna().head()



    # Compute out-of-the-money option price
    # - Merge with at-the-money strike price
    left = options3.reset_index().set_index(["Date", "Days"])     
    df = pd.merge(left, mid_strike, left_index=True, right_index=True)
    # - conditions to separate out-of-the-money puts and calls
    condition1 = df["Strike"] < df["Mid Strike"]
    condition2 = df["Strike"] > df["Mid Strike"]
    # - at-the-money we have two quotes, so take the average
    df["Premium"] = (df["P"] + df["C"]) / 2
    # - remove in-the-money options
    df.loc[condition1, "Premium"] = df.loc[condition1, "P"]
    df.loc[condition2, "Premium"] = df.loc[condition2, "C"]
    options4 = df[["Strike", "Mid Strike", "Premium"]].copy()
    # options4[(options4["Strike"] => 910) & (options4["Strike"] <= 930)].head()


    # Compute difference between adjoining strikes
    def compute_adjoining_strikes_diff(group):
        new = group.copy()
        new.iloc[1:-1] = np.array((group.values[2:] - group.values[:-2]) / 2)
        new.iloc[0] = group.values[1] - group.values[0]
        new.iloc[-1] = group.values[-1] - group.values[-2]
        return new

    options4["dK"] = options4.groupby(["Date", "Days"])["Strike"].transform(compute_adjoining_strikes_diff)
    # options4.head()


    
    # Compute contribution of each strike
    # - merge with risk-free rate
    contrib = pd.merge(options4, yields, left_index=True, right_index=True).reset_index()
    contrib["sigma2"] = contrib["dK"] / contrib["Strike"] ** 2
    contrib["sigma2"] *= contrib["Premium"] * np.exp(contrib["Rate"] * contrib["Days"] / 36500)
    # contrib.head()


    # Compute each period index
    # - Sum up contributions from all strikes
    sigma2 = contrib.groupby(["Date", "Days"])[["sigma2"]].sum() * 2
    # - merge at-the-money strike and implied forward
    sigma2["Mid Strike"] = mid_strike
    sigma2["Forward"] = forward
    # - compute variance for each term
    sigma2["sigma2"] -= (sigma2["Forward"] / sigma2["Mid Strike"] - 1) ** 2
    sigma2["sigma2"] /= sigma2.index.get_level_values(1).astype(float) / 365
    sigma2 = sigma2[["sigma2"]]
    # sigma2.head()


    # Compute interpolated index
    # - this function determines near- and next-term if there are several maturities in the data
    def f(group):
        days = np.array(group["Days"])
        sigma2 = np.array(group["sigma2"])

        if days.min() <= 30:
            T1 = days[days <= 30].max()
        else:
            T1 = days.min()

        T2 = days[days > T1].min()

        sigma_T1 = sigma2[days == T1][0]
        sigma_T2 = sigma2[days == T2][0]

        return pd.DataFrame([{"T1": T1, "T2": T2, "sigma2_T1": sigma_T1, "sigma2_T2": sigma_T2}])

    two_sigmas = sigma2.reset_index().groupby("Date").apply(f, include_groups=False).groupby(level="Date").first()
    # two_sigmas.head()


    # Interpolate the VIX
    df = two_sigmas.copy()

    for t in ["T1", "T2"]:
        # - convert to fractions of the year
        df["days_" + t] = df[t].astype(float) / 365
        # - convert to minutes
        df[t] = (df[t] - 1) * 1440.0 + 510 + 930

    df["sigma2_T1"] = df["sigma2_T1"] * df["days_T1"] * (df["T2"] - 30.0 * 1440.0)
    df["sigma2_T1"] = df["sigma2_T2"] * df["days_T2"] * (30.0 * 1440.0 - df["T1"])
    df["VIX"] = ((df["sigma2_T1"] + df["sigma2_T2"]) / (df["T2"] - df["T1"]) * 365.0 / 30.0) ** 0.5 * 100
    VIX = df[["VIX"]]
    # VIX.head()

    # return call_price, put_price, stock, call_tree, put_tree, 
    return vixDay

#! IMPLEMENT GARCH
# GARCH 
def garch_option_price(S, K, T, r, sigma, N):



    return call_price, put_price, stock, call_tree, put_tree


##! REVIEW FUNCTIONS FOR Ju-Zhong (1999)
def findS(Sx, K, r, q, v, T, phi):
    d1, Ve, h, beta, alpha, Lambda = []

    if (Sx <= 0):
        return 1.0e100
    else:
        d1 = (np.log(Sx / K) + (r + q + v**2 / 2) * T) / v / np.sqrt(T)

    Ve = BS.BSPrice(Sx, K, r, q, v, T, phi)
    h = 1 - np.exp(-r * T)
    beta = 2 * (r - q) / v / v
    alpha = 2 * r / v / v

    if ((r == 0.0) & (phi == 1)):
        Lambda = ((1 - beta) + np.sqrt((beta - 1) * (beta - 1) + 8 / v / v / T)) / 2
    else:
        Lambda = ((1 - beta) + phi * np.sqrt((beta - 1) * (beta - 1) + 4 * alpha/h)) / 2

    return np.pow((phi * np.exp(-q * T) * np.cdf(phi * d1) + Lambda * (phi * (Sx - K) - Ve)/Sx - phi), 2)

##! REVIEW First derivative for Ju-Zhong (1999)
def findSder1(Sx, K, r, q, v, T, phi, dS):
    return (findS(Sx + dS, K, r, q, v, T, phi) - findS(Sx - dS, K, r, q, v, T, phi)) / (2 * dS)

##! REVIEW Second derivative for Ju-Zhong (1999)
def findSder2(Sx, K, r, q, v, T, phi, dS):
    return (findS(Sx + dS, K, r, q, v, T, phi) - 2 * findS(Sx, K, r, q, v, T, phi) + findS(Sx - dS, K, r, q, v, T, phi)) / (dS * dS)

#! REVIEW Newton (For Ju-Zhong 1999)
def Newton(S0, K, r, q, v, T, phi, dS, MaxIter, tol):
    k = 0
    diff = 1.5 * tol
    start = K
    S1 = start - findSder1(start, K, r, q, v, T, phi, dS) / findSder2(start, K, r, q, v, T, phi, dS)

    while(K < MaxIter & diff > tol):
        S0 = S1
        S1 = S0 - findSder1(start, K, r, q, v, T, phi, dS) / findSder2(start, K, r, q, v, T, phi, dS)
        k += 1
        diff = np.abs(S0 - S1)

    return S1

##! REVIEW Ju-Zhong (1999)
def ju_zhong_option_price(S, K, r, q, v, T, phi, MaxIter, tol, dS):
    Sx = Newton(S, K, r, q, v, T, phi, dS, MaxIter, tol)

    Ve = BSPrice(Sx, K, r, q, v, T, phi)

    h = (1 - np.exp(-r * T))
    alpha = 2 * r / v / v
    beta = 2 * (r - q) / v / v
    hAh = phi * (Sx - K) - Ve
    d1 = (np.log(Sx / K) + (r - q + v * v / 2) * T) / v / np.sqrt(T)
    d2 = d1 - v * np.sqrt(T)

    Lambda, b, c, lambdap, dVdh = [],

    if r == 0.0 and phi == 1:
        Lambda = ((1 - beta) + np.sqrt((beta - 1) * (beta - 1) + 8 / v / v / T)) / 2
        b = -2 / (v * v * v * v) / (T * T) / ((beta - 1) * (beta - 1) + 8 / v / v / T)
        c = -1 / np.sqrt((beta - 1) * (beta - 1) + 8 / v / v / T) * (Sx * np.pdf(d1) * np.exp(-q * T) / hAh / v / np.sqrt(T) - 2 * q * Sx * np.cdf(d1) * np.exp(-q * T) + 2 / v / v / T - 4 / (v * v * v * v) / (T * T) / ((beta - 1) * (beta - 1) + 8 / v / v / T))
    else:
        Lambda = ((1 - beta) + phi * np.sqrt((beta - 1) * (beta - 1) + 4 * alpha / h)) / 2
        lambdap = -phi * alpha / (h * h) / np.sqrt((beta - 1) * (beta - 1) + 4 * alpha / h)
        dVdh = Sx * np.pdf(d1) * v * np.exp((r - q) * T) / 2 / r / np.sqrt(T) - phi * q * Sx * np.cdf(phi * d1) * np.exp((r - q) * T) / r + phi * K * np.cdf(phi * d2)
        b = (1 - h) * alpha * lambdap / 2 / (2 * Lambda + beta - 1)
        c = -(1 - h) * alpha / (2 * Lambda + beta - 1) * (1 / hAh * dVdh + 1 / h + lambdap / (2 * Lambda * beta - 1))

    X = b * (np.log(S / Sx)) * (np.log(S / Sx)) + c * np.log(S / Sx)

    VE = BSPrice(S, K, r, q, v, T, phi)

    if phi * (Sx - S) > 0:
        return VE + hAh * np.pow(S / Sx, Lambda) / (1 - X)
    else:
        return phi * (S - K)

