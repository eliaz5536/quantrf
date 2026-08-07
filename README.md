# Quant Research Framework (QRF)
![alt text](image.png)
Interactive open-source quantitative finance platform for exploring financial models, analysing market data, and visualizations of option pricing and risk analysis using Streamlit.

The project extends and uses [**Georgios Drosogiannis**](https://github.com/George-Dros) on [volatility surface visualisation](https://github.com/George-Dros/Volatility_Surface) and [interactive Black-Scholes heatmaps](https://github.com/George-Dros/Black-Scholes-Interactive-heatmap), together with [**Killa Voillaume's**](https://github.com/KilianVoillaume) [Options Greek Visualizer](https://github.com/KilianVoillaume/Greeks_Streamlit_APP/tree/main).

---

# Features

### Interactive Option Pricing
- Real-time option valuatoin using the Black-Scholes model
- Dynamic parameter adjustment through an interactive Streamlit interface
- Support for both European Call and Put options
- Instant recalculation of theoretical option prices.

### Options Greeks Visualisation

Explore the major sensitivty measures that describe option risk with Delta, Gamma, Theta, Vega and Rho

Visualize how each Greek changes with respect to:
- Underlying asset price
- Time to expiration
- Implied volatility
- Interest rates
- Strike price


<table>
<tr>
<td align="center">
<!-- <img src="image-10.png" width="100%"><br> -->
<img width="779" height="578" alt="0628f06213934e8eb21d98a3dbac5951" src="https://github.com/user-attachments/assets/6041bc3b-2d1a-49b7-a983-593039b2362b" />
</td>

<td align="center">
<!-- <img src="image-2.png" width="100%"><br> -->
<img width="779" height="578" alt="image-4" src="https://github.com/user-attachments/assets/b0372c33-88f1-4bb7-b2f1-07bd90c8c55d" />
</td>

<td align="center">
<!-- <img src="image-3.png" width="100%"><br> -->
<img width="781" height="579" alt="image-6" src="https://github.com/user-attachments/assets/530f3901-4fe3-4da1-a376-53b60230539b" />
</td>
</tr>

<tr>
<td align="center">
<!-- <img src="image-4.png" width="100%"><br> -->
<img width="778" height="578" alt="image-2" src="https://github.com/user-attachments/assets/354b8e24-a611-4780-8df2-5db86546311e" />
</td>

<td align="center">
<!-- <img src="image-6.png" width="100%"><br> -->
<img width="779" height="579" alt="image-7" src="https://github.com/user-attachments/assets/a9331e26-6793-4677-8fe9-b62a6814fa6a" />
</td>

<td align="center">
<!-- <img src="image-7.png" width="100%"><br> -->
<img width="778" height="578" alt="image-3" src="https://github.com/user-attachments/assets/391b2a00-a185-490e-80c6-674b49387d03" />
</td>
</tr>

</table>

### Interactive Heatmaps

Generate interactive heatmaps illustrating relationships between stock price, strike price, time to expiration, interest rate, volatility and dividend yield.

These visualisations provide intuitive insight into multidimensional pricing behaviour that is difficult to observe through numerical outputs alone.

<img width="1460" height="828" alt="945eb2bcebe0e52a5be31ea090832de2" src="https://github.com/user-attachments/assets/41754370-f67c-4106-a235-1da4eba87f6e" />
<img width="1460" height="823" alt="bd93ae7aa860fe3cd3c70a62152233f3" src="https://github.com/user-attachments/assets/a2ca251d-3868-44de-a807-1cc80b017301" />

### Volatility Surface Analysis

Visualize three-dimensional implied volatility surface to understand how option values evolve under changing market conditions.

<img width="1450" height="800" alt="image-8" src="https://github.com/user-attachments/assets/5c357ea1-76ed-4425-ba7c-ef425fe0dc51" />

---

# Tech Stack

| Technology     | Purpose                                          |
| -------------- | ------------------------------------------------ |
| **Python**     | Core programming language                        |
| **NumPy**      | Numerical computing and vectorised operations    |
| **Pandas**     | Financial data manipulation and analysis         |
| **SciPy**      | Scientific computing and statistical methods     |
| **Matplotlib** | Financial plotting and visualisation             |
| **Seaborn**    | Statistical graphics and enhanced visualisations |
| **YFinance**   | Live financial market data retrieval             |
| **Streamlit**  | Interactive web application framework            |
| **Git**        | Version control and collaborative development    |

---

## Suggestions & Future Work

The Quant Research Framework is intended to evolve into a comprehensive quantitative finance platform that supports financial modelling, derivative pricing, risk management, and market research. Future development will focus on expanding the framework with additional mathematical models, numerical methods, and financial analytics commonly used in both academia and industry.

### Stochastic Processes & Asset Price Models
Future implementations may include:
- Geometric Brownian Motion (GBM)
- Black (1976) Futures Option Pricing Model
- Monte Carlo Simulation Methods
- GARCH (Generalised Autoregressive Conditional Heteroskedasticity) Models

### European Option Pricing & Lattice Models
Additoinal pricing models and numerical methods include:
- Cox-Ross-Rubinstein (1979) Binomial Tree Model
- Jarrow-Rudd (1983) Binomial Model
- Tian (1993) Binomial Tree Model
- Leisen-Reimer (1996) Binomial Tree Model
- Figlewski and Gao (1999) Adaptive Mesh Model
- Hull and White (2004) Finite Difference Methods

### American Option Pricing
Support for early exercise methods, including:
- Bjerksund-Stensland (1993)
- Brenner and Galai (1989)
- Ju-Zhong (1999)
- Bjerksund-Stensland (2002)

### Credit Risk Modelling
Future credit risk analytics may include:
- KMV-Merton Structural Credit Risk Model
- Probability of Default (PD)
- Credit Spread Analysis
- Structural and Reduced-Form Credit Risk Models

### Volatility & Risk Analytics
Future volatility and risk management capabilities may include:
- Variance-Covariance Matrix
- Historical Volatility
- Implied Volatility Surface Construction
- Volatility Smile and Skew Analysis
- Covariance and Correlation Analysis
- Principal Component Analysis (PCA)
- Valute at Risk (VaR)
- Conditional Value at Risk (CVaR)

## Credits
The following projects provided valuable inspiration and reference implementaitons during the development of this frameowrk:
- [**Georgios Drosogiannis's**](https://github.com/George-Dros) [Volatility Surface Visualisation](https://github.com/George-Dros/Volatility_Surface) and [Interactive Black-Scholes Heatmaps](https://github.com/George-Dros/Black-Scholes-Interactive-heatmap)
- [**Killa Voillaume's**](https://github.com/KilianVoillaume) [Options Greek Visualizer](https://github.com/KilianVoillaume/Greeks_Streamlit_APP/tree/main).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
