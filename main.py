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
st.sidebar.page_link(page="main.py", label="Black-Scholes-Merton (1973)")
st.sidebar.page_link(page="pages/black.py", label="Black (1976)", disabled=True)
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

program_mode = st.sidebar.radio(
    'Select Program Mode:',
    ('Black-Scholes Pricer', 'Historical Ticker Data Pricer')
)

if program_mode == "Black-Scholes Pricer":
    st.title("Black-Scholes Option Pricing")
    # st.markdown("<h1 style='text-align: center;'>Black Scholes Option Pricing</h1>", unsafe_allow_html=True)
    st.sidebar.header('Black-Scholes Pricer Variables')

    current_price = st.sidebar.number_input('Spot Price($)', value=100.00, format="%.2f")
    strike_price = st.sidebar.number_input('Strike Price($)', value=80.00, format="%.2f")
    volatility = st.sidebar.number_input('Volatility (σ)', value=0.20, format="%.2f")
    time_to_maturity = st.sidebar.number_input('Time to Maturity (in Years, days/365)', value=1.00, format="%.2f")
    risk_free_rate = st.sidebar.number_input('Risk-Free Rate', min_value=0.0, max_value=1.0, value=0.03, format="%.4f")
    dividend_yield = st.sidebar.number_input('Dividend Yield', min_value=0.0, max_value=1.0, value=0.0, format="%.4f")

    # Greeks - Calculate the Greeks using the provided inputs
    delta_call, delta_put, gamma, vega, theta_call, theta_put, rho_call, rho_put = f.calculate_greeks(
        current_price, strike_price, risk_free_rate, time_to_maturity, volatility, dividend_yield=dividend_yield
    )
    
    # Mode selection
    mode = st.sidebar.radio(
        'Select Mode:',
        ('Pricing', 'P&L')
    )

    # Conditionally display "Purchase Price" input or explanation text
    if mode == 'P&L':
        purchase_price = st.sidebar.number_input('Purchase Price', value=5.00, format="%.2f")
    else:
        purchase_price = 0
        st.sidebar.markdown("<i>Note: Switch to 'P&L' mode to set Purchase Price.</i>", unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Heatmap Inputs")

    # Set a default range within the dynamic range
    vol_min = 0.20
    vol_max = 0.50

    # Create the slider for strike price range percentages dynamically
    volatility_range_percentage = st.sidebar.slider(
        'Volatility Range',
        min_value=0.01,  # Minimum percentage allowed
        max_value=1.0,  # Maximum percentage allowed
        value=(vol_min, vol_max)  # Default range
    )

    vol_min_selected, vol_max_selected = volatility_range_percentage

    spot_min = st.sidebar.number_input('Min Spot Price($)', value=0.5 * current_price, format="%.2f")
    spot_max = st.sidebar.number_input('Max Spot Price($)', value=1.5 * current_price, format="%.2f")

    # Display Black Scholes Variables in a wide format using Streamlit columns
    colA, colB, colC, colD, colE, colF = st.columns([1, 1, 1, 1, 1, 1])

    with colA:
        st.markdown(f"**Spot Price:** ${current_price:.2f}")
    with colB:
        st.markdown(f"**Strike Price:** ${strike_price:.2f}")
    with colC:
        st.markdown(f"**Volatility:** {volatility:.3f}")
    with colD:
        st.markdown(f"**Time to Maturity (Years):** {time_to_maturity:.2f}")
    with colE:
        st.markdown(f"**Risk-Free Rate:** {risk_free_rate:.4f}")
    with colF:
        st.markdown(f"**Dividend Yield:** {dividend_yield:.4f}")


    st.space()

    # Greeks Sensitive Analysis
    st.header("Greeks Visualization and Sensitivity Analysis")

    # Greeks - Calculate the Greeks using the provided inputs
    delta_call, delta_put, gamma, vega, theta_call, theta_put, rho_call, rho_put = f.calculate_greeks(
        current_price, strike_price, risk_free_rate, time_to_maturity, volatility, dividend_yield=dividend_yield
    )

    # Display Black Scholes Variables in a wide format using Streamlit columns
    colG, colH, colI, colJ, colK, colL, colM, colN = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    with colG:
        st.markdown(f"**Delta Call:** {delta_call:.4f}")
    with colH:
        st.markdown(f"**Delta Put:** {delta_put:.4f}")
    with colI:
        st.markdown(f"**Gamma:** {gamma:.4f}")
    with colJ:
        st.markdown(f"**Vega:** {vega:.4f}")
    with colK:
        st.markdown(f"**Theta Call:** {theta_call:.4f}")
    with colL:
        st.markdown(f"**Theta Put:** {theta_put:.4f}")
    with colM:
        st.markdown(f"**Rho Call:** {rho_call:.4f}")
    with colN:
        st.markdown(f"**Rho Put:** {rho_put:.4f}")

    st.space()

    # Parameter to visualize against
    param_to_visualize = st.selectbox(
        "Select Parameter to Visualize Against", 
        ["Stock Price", "Strike Price", "Time to Expiration", "Interest Rate", "Volatility", "Dividend Yield"]
    )

    # ------ PARAMETER RANGES ------
    if param_to_visualize == "Stock Price":
        param_range = np.linspace(50, 150, 100)
        x_label = "Stock Price ($)"
    elif param_to_visualize == "Strike Price":
        param_range = np.linspace(50, 150, 100)
        x_label = "Strike Price ($)"
    elif param_to_visualize == "Time to Expiration":
        param_range = np.linspace(1, 365, 100)
        x_label = "Time to Expiration (Days)"
    elif param_to_visualize == "Interest Rate":
        param_range = np.linspace(0, 10, 100)
        x_label = "Interest Rate (%)"
    elif param_to_visualize == "Volatility":
        param_range = np.linspace(5, 100, 100)
        x_label = "Volatility (%)"
    elif param_to_visualize == "Dividend Yield":
        param_range = np.linspace(0, 10, 100)
        x_label = "Dividend Yield (%)"

    call_price_values = []
    put_price_values = []
    delta_call_values = []
    delta_put_values = []
    gamma_values = []
    vega_values = []
    theta_call_values = []
    theta_put_values = []
    rho_call_values = []
    rho_put_values = []

    for param_value in param_range:
        if param_to_visualize == "Stock Price":
            S = param_value
            K = strike_price
            T = time_to_maturity
            r = risk_free_rate
            sigma = volatility
            q = dividend_yield
        elif param_to_visualize == "Strike Price":
            S = current_price
            K = param_value
            T = time_to_maturity
            r = risk_free_rate
            sigma = volatility
            q = dividend_yield
        elif param_to_visualize == "Time to Expiration":
            if param_value < 0.001:
                continue
            S = current_price
            K = strike_price
            T = param_value / 365
            r = risk_free_rate
            sigma = volatility
            q = dividend_yield
        elif param_to_visualize == "Interest Rate":
            S = current_price
            K = strike_price
            T = time_to_maturity
            r = param_value / 100
            sigma = volatility
            q = dividend_yield
        elif param_to_visualize == "Volatility":
            if param_value < 0.001:
                continue
            S = current_price
            K = strike_price
            T = time_to_maturity
            r = risk_free_rate
            sigma = param_value / 100
            q = dividend_yield
        elif param_to_visualize == "Dividend Yield":
            S = current_price
            K = strike_price
            T = time_to_maturity
            r = risk_free_rate
            sigma = volatility
            q = param_value / 100

        delta_call_val, delta_put_val, gamma_val, vega_val, theta_call_val, theta_put_val, rho_call_val, rho_put_val = f.calculate_greeks(
            S, K, r, T, sigma, dividend_yield=q
        )
        call_price_val = f.call_bs_value(S, K, r, T, sigma, q=q)
        put_price_val = f.put_bs_value(S, K, r, T, sigma, q=q)

        call_price_values.append(call_price_val)
        put_price_values.append(put_price_val)
        delta_call_values.append(delta_call_val)
        delta_put_values.append(delta_put_val)
        gamma_values.append(gamma_val)
        vega_values.append(vega_val)
        theta_call_values.append(theta_call_val)
        theta_put_values.append(theta_put_val)
        rho_call_values.append(rho_call_val)
        rho_put_values.append(rho_put_val)

    st.subheader(f"Effect of {param_to_visualize} on Option Prices and Greeks")

    if param_to_visualize == "Stock Price":
        current_value = current_price
    elif param_to_visualize == "Strike Price":
        current_value = strike_price
    elif param_to_visualize == "Time to Expiration":
        current_value = time_to_maturity * 365
    elif param_to_visualize == "Interest Rate":
        current_value = risk_free_rate * 100
    elif param_to_visualize == "Volatility":
        current_value = volatility * 100
    elif param_to_visualize == "Dividend Yield":
        current_value = dividend_yield * 100

    x_display = param_range

    plot_definitions = [
        {
            "title": "Option Prices",
            "series": [call_price_values, put_price_values],
            "labels": ["Call Price", "Put Price"],
            "ylabel": "Price ($)",
        },
        {
            "title": "Delta",
            "series": [delta_call_values, delta_put_values],
            "labels": ["Delta Call", "Delta Put"],
            "ylabel": "Delta",
        },
        {
            "title": "Gamma",
            "series": [gamma_values],
            "labels": ["Gamma"],
            "ylabel": "Gamma",
        },
        {
            "title": "Vega",
            "series": [vega_values],
            "labels": ["Vega"],
            "ylabel": "Vega ($/1% vol)",
        },
        {
            "title": "Theta",
            "series": [theta_call_values, theta_put_values],
            "labels": ["Theta Call", "Theta Put"],
            "ylabel": "Theta ($/day)",
        },
        {
            "title": "Rho",
            "series": [rho_call_values, rho_put_values],
            "labels": ["Rho Call", "Rho Put"],
            "ylabel": "Rho ($/1% rate)",
        },
    ]

    for i in range(0, len(plot_definitions), 3):
        cols = st.columns(3)
        for j, plot_def in enumerate(plot_definitions[i:i+3]):
            with cols[j]:
                fig, ax = plt.subplots(figsize=(4, 3))
                for series, label in zip(plot_def["series"], plot_def["labels"]):
                    ax.plot(x_display, series, label=label)
                ax.set_xlabel(x_label)
                ax.set_ylabel(plot_def["ylabel"])
                ax.set_title(plot_def["title"])
                ax.grid(True)
                ax.axvline(x=current_value, color="r", linestyle="--", alpha=0.5)
                ax.legend(fontsize="small")
                plt.tight_layout()
                st.pyplot(fig)
 
    st.space()

    st.header("Heatmap of Option Prices and P&L")

    # Call and Put prices for given inputs
    call_price = f.call_bs_value(current_price, strike_price, risk_free_rate, time_to_maturity, volatility,
                                 q=dividend_yield)
    put_price = f.put_bs_value(current_price, strike_price, risk_free_rate, time_to_maturity, volatility,
                               q=dividend_yield)

    # Create two columns to display Call and Put prices
    col1, col2 = st.columns(2)

    # Display Call Price in the first column
    with col1:
        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; padding: 10px; background-color: #e0f7fa; border-radius: 10px; font-size: 18px;'>
                <h3 style='color: #00796b; margin: 0;'>Call Price: ${:.2f}</h3>
            </div>
        """.format(call_price), unsafe_allow_html=True)

    # Display Put Price in the second column
    with col2:
        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; padding: 10px; background-color: #ffe0b2; border-radius: 10px; font-size: 18px;'>
                <h3 style='color: #e65100; margin: 0;'>Put Price: ${:.2f}</h3>
            </div>
        """.format(put_price), unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    call_df, put_df, call_pnl_df, put_pnl_df = f.calculate_option_values(spot_min, spot_max, vol_min_selected,
                                                                         vol_max_selected, strike_price, risk_free_rate,
                                                                         time_to_maturity,
                                                                         dividend_yield=dividend_yield,
                                                                         purchase_price=purchase_price)
    
    heatmap = f.plot_heatmaps(mode=mode, call_df=call_df, put_df=put_df, call_pnl_df=call_pnl_df, put_pnl_df=put_pnl_df)


    # ---------------
    # ---------------
elif program_mode == "Historical Ticker Data Pricer":
    # Header
    st.title("Black-Scholes Option Pricing with Historical Ticker Data")

    #st.markdown("<h1 style='text-align: center;'>Mispricing Heatmap: Theoretical Price Minus Market Price</h1>", unsafe_allow_html=True)
    # Sidebar Inputs for Historical Ticker Data Pricer
    st.sidebar.header('Historical Ticker Data Variables')

    # User Inputs
    ticker_symbol = st.sidebar.text_input('Ticker Symbol', value='AAPL').strip().upper()
    risk_free_rate = st.sidebar.number_input('Risk-Free Rate', min_value=0.0, max_value=1.0, value=0.03, format="%.4f")
    dividend_yield = st.sidebar.number_input('Dividend Yield', min_value=0.0, max_value=1.0, value=0.0, format="%.4f")

    if not ticker_symbol:
        st.info("Enter a ticker symbol in the sidebar to begin.")
        st.stop()

    @st.cache_data(show_spinner="Fitting SVI slices…")
    def cached_svi_fits(iv_df, spot, r, q):
        """Cache the per-expiry SVI fits (independent of strike/liquidity sliders)."""
        return svi.fit_all_slices(iv_df, spot, r, q)

    # Get the Calls and Puts
    calls_all, puts_all, spot_price = f.get_option_chains_spot(ticker_symbol=ticker_symbol)

    calls_all["expiration"] = pd.to_datetime(calls_all["expiration"])
    puts_all["expiration"] = pd.to_datetime(puts_all["expiration"])

    common_years = pd.Series(list(set(calls_all['expiration'].dt.year) & set(puts_all['expiration'].dt.year)))

    # Date selection inputs
    st.sidebar.subheader('Option Maturity Date')
    selected_year = st.sidebar.selectbox('Year', options=common_years)

    filtered_calls_year = calls_all[calls_all['expiration'].dt.year == selected_year]
    filtered_puts_year = puts_all[puts_all['expiration'].dt.year == selected_year]

    common_months = pd.Series(list(set(filtered_calls_year['expiration'].dt.month) & set(filtered_puts_year['expiration'].dt.month)))
    selected_month = st.sidebar.selectbox('Month', options=common_months)

    filtered_calls_month = filtered_calls_year[filtered_calls_year['expiration'].dt.month == selected_month]
    filtered_puts_month = filtered_puts_year[filtered_puts_year['expiration'].dt.month == selected_month]

    common_days = pd.Series(list(set(filtered_calls_month['expiration'].dt.day) & set(filtered_puts_month['expiration'].dt.day)))
    selected_day = st.sidebar.selectbox('Day', options=common_days) 

    # Format the date to use in teh dataframes
    formatted_date = f"{selected_year}-{int(selected_month):02}-{int(selected_day):02}"
    date_for_call = calls_all[calls_all['expiration'] == formatted_date]
    date_for_put = puts_all[puts_all['expiration'] == formatted_date]

    # Time to maturity in float
    time_to_maturity = date_for_call["time_to_expiration"].iloc[0]

    # Create the datapoints
    call_n = len(date_for_call)
    put_n = len(date_for_put)

    call_indices = np.linspace(0, call_n - 1, 11, dtype=int)
    put_indices = np.linspace(0, put_n - 1, 11, dtype=int)

    call_datapoints = date_for_call.iloc[call_indices]
    put_datapoints = date_for_put.iloc[put_indices]

    call_datapoints = call_datapoints.reset_index(drop=True)
    put_datapoints = put_datapoints.reset_index(drop=True)

    # Spot price slider based on ticker data
    min_spot, max_spot = spot_price_slider = st.sidebar.slider(
        'Spot Price Range',
        min_value=0.1 * spot_price,
        max_value=2.0 * spot_price,
        value=(0.5 * spot_price, 1.5 * spot_price),
        format="%.2f"
    )

    # Display Variables in a wide format using Streamlit columns
    colA, colB, colC, colD, colE, colF = st.columns([1, 1, 1, 1, 1, 1])

    with colA:
        st.markdown(f"**Spot Price:** ${spot_price:.2f}")
    with colB:
        st.markdown(f"**Ticker:** ${ticker_symbol}")
    with colC:
        st.markdown(f"**Selected Maturity Date:** {selected_year}-{selected_month:02d}-{selected_day:02d}")
    with colD:
        st.markdown(f"**Risk-Free Rate:** {risk_free_rate:.4f}")
    with colE:
        st.markdown(f"**Dividend Yield:** {dividend_yield:.4f}")
    with colF:
        st.markdown(f"**Spot Price Range:** ${spot_price_slider[0]:.2f} - ${spot_price_slider[1]:.2f}")



    # Determine a representative strike and implied volatility from the selected expiry
    all_strikes = pd.concat([call_datapoints["strike"], put_datapoints["strike"]], ignore_index=True)
    if not all_strikes.empty:
        nearest_strike = float(all_strikes.iloc[(np.abs(all_strikes - spot_price)).argmin()])
        strike_price_hist = nearest_strike

        call_iv_series = call_datapoints.loc[call_datapoints["strike"] == nearest_strike, "impliedVolatility"]
        put_iv_series = put_datapoints.loc[put_datapoints["strike"] == nearest_strike, "impliedVolatility"]

        if not call_iv_series.empty and not put_iv_series.empty:
            volatility_hist = float(np.nanmean([call_iv_series.iloc[0], put_iv_series.iloc[0]]))
        elif not call_iv_series.empty:
            volatility_hist = float(call_iv_series.iloc[0])
        elif not put_iv_series.empty:
            volatility_hist = float(put_iv_series.iloc[0])
        else:
            volatility_hist = 0.20
    else:
        strike_price_hist = spot_price
        volatility_hist = 0.20

    # Protect against missing IVs
    if not np.isfinite(volatility_hist) or volatility_hist <= 0:
        volatility_hist = 0.20

    # Greeks - Calculate the Greeks using the selected option's strike and averaged IV
    delta_call, delta_put, gamma, vega, theta_call, theta_put, rho_call, rho_put = f.calculate_greeks(
        spot_price, strike_price_hist, risk_free_rate, time_to_maturity, volatility_hist, dividend_yield=dividend_yield
    )

    st.header("Greeks Sensitivity Analysis")

    st.caption(f"Greeks computed for strike ${strike_price_hist:.2f} with implied vol {volatility_hist:.3%}")
    
    # Display Black Scholes Variables in a wide format using Streamlit columns
    colG, colH, colI, colJ, colK, colL, colM, colN = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    with colG:
        st.markdown(f"**Delta Call:** {delta_call:.4f}")
    with colH:
        st.markdown(f"**Delta Put:** {delta_put:.4f}")
    with colI:
        st.markdown(f"**Gamma:** {gamma:.4f}")
    with colJ:
        st.markdown(f"**Vega:** {vega:.4f}")
    with colK:
        st.markdown(f"**Theta Call:** {theta_call:.4f}")
    with colL:
        st.markdown(f"**Theta Put:** {theta_put:.4f}")
    with colM:
        st.markdown(f"**Rho Call:** {rho_call:.4f}")
    with colN:
        st.markdown(f"**Rho Put:** {rho_put:.4f}")

    st.space()

    st.header("Mispricing Heatmap: Theoretical Price Minus Market Price")

    # Theoretical minus Market prices data
    call_df, put_df = f.calculate_market_prices(min_spot, max_spot, call_datapoints, put_datapoints, risk_free_rate,
                                                                                dividend_yield)
    heatmap = f.market_heatmaps(call_df, put_df)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Implied Volatility Surface Inputs")

    y_axis = st.sidebar.selectbox("Y-Axis (raw surface)", ["Strike Price", "Moneyness"])
    method = st.sidebar.radio("Surface method", ["Raw (interpolated)", "SVI fit"])

    # st.markdown("<h1 style='text-align: center;'>Implied Volatility Surface</h1>", unsafe_allow_html=True)
    st.header("Implied Volatility Surface")

   # --- Data (cached; only refetched when the ticker changes) ---------------
    try:
        spot_prices, spot_price = f.get_stock_data(ticker_symbol)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    options_data, expiration_dates = f.get_options_data(ticker_symbol)
    if options_data.empty:
        st.error("No options data returned for this ticker (or Yahoo blocked the request). Try another ticker.")
        st.stop()

    # OTM blend + strike-independent prep (cached).
    prepared = f.prepare_options(options_data, spot_price)
    if prepared.empty:
        st.error("No options left after dropping very short-dated expiries. Try another ticker.")
        st.stop()

    # Implied vol for the WHOLE (blended) chain — cached per ticker/r/q.
    imp_vol_all = f.calculate_implied_volatility(
        prepared, spot_price, risk_free_rate, dividend_yield
    )
    if imp_vol_all.empty:
        st.error("IV computation returned no valid points (bad quotes / illiquid options). Try another ticker.")
        st.stop() 



    # --- Filters (cheap: only re-filter an in-memory table) -------------------
    st.sidebar.subheader("Strike range")
    strike_pct = st.sidebar.slider(
        "Strike Price Range (as % of Spot Price)",
        min_value=20, max_value=200, value=(70, 130),
    )
    min_strike_price = spot_price * (strike_pct[0] / 100)
    max_strike_price = spot_price * (strike_pct[1] / 100)

    st.sidebar.subheader("Liquidity filters")
    min_volume = st.sidebar.number_input("Min volume", min_value=0, value=0, step=1)
    min_open_interest = st.sidebar.number_input("Min open interest", min_value=0, value=0, step=1)
    max_spread_pct = st.sidebar.slider("Max bid-ask spread (%)", min_value=1, max_value=100, value=100)

    imp_vol_data = f.filter_iv_data(
        imp_vol_all, min_strike_price, max_strike_price,
        min_volume=min_volume, min_open_interest=min_open_interest,
        max_spread_pct=max_spread_pct,
    )
    if imp_vol_data.empty:
        st.error("No options matched your strike/liquidity filters. Loosen them in the sidebar.")
        st.stop()

    n_calls = int((imp_vol_data["OptionType"] == "C").sum())
    n_puts = int((imp_vol_data["OptionType"] == "P").sum())
    st.caption(
        f"**{ticker_symbol}**  ·  spot ${spot_price:,.2f}  ·  {len(imp_vol_data):,} IV points "
        f"({n_puts:,} puts / {n_calls:,} calls) across {imp_vol_data['TimeToExpiry'].nunique()} expiries"
    )

    surface_tab, smile_tab, data_tab = st.tabs(["3D Surface", "Smile / Skew", "Data & Export"])

    # =========================================================================
    # 3D SURFACE
    # =========================================================================
    with surface_tab:
        if method == "SVI fit":
            fits = cached_svi_fits(imp_vol_all, spot_price, risk_free_rate, dividend_yield)
            built = svi.build_svi_surface(fits)
            if built is None:
                st.warning("Not enough expiries with a good SVI fit. Falling back to the raw surface.")
                method = "Raw (interpolated)"
            else:
                Ts, k_grid, Z = built
                fig = go.Figure(data=[go.Surface(x=Ts, y=k_grid, z=Z, colorscale="Viridis")])
                fig.update_layout(
                    title=f"SVI Implied Volatility Surface of {ticker_symbol}",
                    scene=dict(
                        xaxis_title="Time to Expiration (years)",
                        yaxis_title="Log-moneyness ln(K/F)",
                        zaxis_title="Implied Volatility (%)",
                    ),
                    height=800,
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption(
                    f"SVI fit on {len(fits)} expiries · median slice RMSE (total variance): "
                    f"{np.median([d['rmse'] for d in fits.values()]):.2e}"
                )

        if method == "Raw (interpolated)":
            X = imp_vol_data["TimeToExpiry"].values
            Z = imp_vol_data["ImpliedVolatility"].values * 100

            if y_axis == "Moneyness":
                T = imp_vol_data["TimeToExpiry"].values
                F = np.maximum(spot_price * np.exp((risk_free_rate - dividend_yield) * T), 1e-12)
                Y = np.log(imp_vol_data["StrikePrice"].values / F)
                y_label = "Log-moneyness ln(K/F)"
            else:
                Y = imp_vol_data["StrikePrice"].values
                y_label = "Strike Price ($)"

            if len(np.unique(X)) < 2 or len(np.unique(Y)) < 2:
                st.error("Not enough variation in expiry/strike to build a surface. Widen the filters.")
                st.stop()

            xi = np.linspace(X.min(), X.max(), 30)
            yi = np.linspace(Y.min(), Y.max(), 30)
            xi, yi = np.meshgrid(xi, yi)
            zi = griddata((X, Y), Z, (xi, yi), method="linear")
            zi_nearest = griddata((X, Y), Z, (xi, yi), method="nearest")
            zi = np.where(np.isnan(zi), zi_nearest, zi)

            fig = go.Figure(data=[go.Surface(x=xi, y=yi, z=zi, colorscale="Viridis")])
            fig.update_layout(
                title=f"Implied Volatility Surface of {ticker_symbol}",
                scene=dict(
                    xaxis_title="Time to Expiration (years)",
                    yaxis_title=y_label,
                    zaxis_title="Implied Volatility (%)",
                ),
                height=800,
            )
            st.plotly_chart(fig, use_container_width=True)

    # =========================================================================
    # SMILE / SKEW (2D slice for a single expiry)
    # =========================================================================
    with smile_tab:
        expiries = sorted(imp_vol_data["Expiration"].unique())
        if not expiries:
            st.info("No expiries available with the current filters.")
        else:
            chosen = st.selectbox("Expiration", expiries)
            slice_df = imp_vol_data[imp_vol_data["Expiration"] == chosen].sort_values("StrikePrice")
            T = float(slice_df["TimeToExpiry"].mean())
            F = spot_price * np.exp((risk_free_rate - dividend_yield) * T)

            use_moneyness = y_axis == "Moneyness"
            if use_moneyness:
                x_obs = np.log(slice_df["StrikePrice"].to_numpy(float) / F)
                x_label = "Log-moneyness ln(K/F)"
            else:
                x_obs = slice_df["StrikePrice"].to_numpy(float)
                x_label = "Strike ($)"

            fig2 = go.Figure()
            for kind, name, color in [("P", "OTM puts", "#EF553B"), ("C", "OTM calls", "#636EFA")]:
                sub = slice_df[slice_df["OptionType"] == kind]
                if not sub.empty:
                    xs = (np.log(sub["StrikePrice"].to_numpy(float) / F) if use_moneyness
                          else sub["StrikePrice"].to_numpy(float))
                    fig2.add_trace(go.Scatter(
                        x=xs, y=sub["ImpliedVolatility"].to_numpy(float) * 100,
                        mode="markers", name=name, marker=dict(color=color, size=7),
                    ))

            # Overlay the SVI fit for this expiry, if available.
            fits = cached_svi_fits(imp_vol_all, spot_price, risk_free_rate, dividend_yield)
            fit = fits.get(str(chosen))
            if fit is not None:
                k_line = np.linspace(x_obs.min() if use_moneyness else np.log(slice_df["StrikePrice"].min() / F),
                                     x_obs.max() if use_moneyness else np.log(slice_df["StrikePrice"].max() / F),
                                     100)
                iv_line = svi.svi_iv(k_line, fit["T"], fit["params"]) * 100
                x_line = k_line if use_moneyness else F * np.exp(k_line)
                fig2.add_trace(go.Scatter(
                    x=x_line, y=iv_line, mode="lines", name="SVI fit",
                    line=dict(color="#00CC96", width=2),
                ))

            fig2.update_layout(
                title=f"{ticker_symbol} volatility smile — {chosen} (T={T:.3f}y)",
                xaxis_title=x_label, yaxis_title="Implied Volatility (%)",
                height=550,
            )
            st.plotly_chart(fig2, use_container_width=True)

    # =========================================================================
    # DATA & EXPORT
    # =========================================================================
    with data_tab:
        st.dataframe(imp_vol_data, use_container_width=True, height=400)
        csv = imp_vol_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download IV data (CSV)", data=csv,
            file_name=f"{ticker_symbol}_iv_surface.csv", mime="text/csv",
        )
        html = fig.to_html(include_plotlyjs="cdn")
        st.download_button(
            "⬇️ Download surface (interactive HTML)", data=html,
            file_name=f"{ticker_symbol}_iv_surface.html", mime="text/html",
        )