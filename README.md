<center><h1>QuantRF</h1></center>

<img width="1920" height="857" alt="quantrf_logo" src="https://github.com/user-attachments/assets/f89f68cc-1912-4f2f-895b-1bbe5d013dbd" />

Interactive open-source quantitative finance platform for exploring financial models, analysing market data, and visualizations of option pricing and risk analysis using Streamlit.

The project extends and uses [**Georgios Drosogiannis**](https://github.com/George-Dros) on [volatility surface visualisation](https://github.com/George-Dros/Volatility_Surface) and [interactive Black-Scholes heatmaps](https://github.com/George-Dros/Black-Scholes-Interactive-heatmap), together with [**Killa Voillaume's**](https://github.com/KilianVoillaume) [Options Greek Visualizer](https://github.com/KilianVoillaume/Greeks_Streamlit_APP/tree/main).

---

# Features

### Interactive Option Pricing
- Real-time option valuation using the Black-Scholes model
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

### Binomial Trees

<img width="1460" height="921" alt="44cae6bee9d41d753cd72cd507bd311a" src="https://github.com/user-attachments/assets/75afac9c-b374-43f6-8827-2beee62d719a" />

<img width="1460" height="1031" alt="77a2692949354623966bb837baa112dc" src="https://github.com/user-attachments/assets/3cc20e49-cad5-4ca8-a102-a0f2c2929c57" />

<img width="1460" height="1031" alt="5d3cc5ab0fc8a3dd1b3ddc3e5bd6322b" src="https://github.com/user-attachments/assets/18903ff6-c8d9-45b7-9b99-02ed000b6643" />

### Credit Risk Models
Evaluate the firm's asset using KMV-Merton Structural Credit Risk Model to determine when the asset value is below the debt face value at maturity.

### Risk Management
Determine the loss distribution by calculating the value at risk (VaR).

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

The Quant Research Framework is intended to evolve into a comprehensive quantitative finance platform that supports financial modelling, derivative pricing, risk management, and market research. Future development will focus on expanding the framework with additional mathematical models, numerical methods, and financial analytics commonly used in both academia and industry. The following fields that need to be reviewed and focused on are the following:

### Mathematical Notation and Description
The mathematical description can be simplified to make it easy-to-read and easier to understand through understanding each term of the mathematical model.

### Credit Risk Modelling
Credit risk analytics models can be expanded including:
- Probability of Default (PD)
- Credit Spread Analysis
- Structural and Reduced-Form Credit Risk Models

### Volatility & Risk Analytics
Volatility and risk analytics can be explored in depth including:
- Variance-Covariance Matrix
- Volatility Smile and Skew Analysis
- Covariance and Correlation Analysis
- Principal Component Analysis (PCA)

### Excel Spreadsheet
The use of examples through Spreadsheet can make the following method easy to follow and accessible for those who do not use Python.
These examples can be derived from CFA as a prime example.

### Further Models supported from Research Papers
Popular models that are further supported from research papers in the field of finance and economics can be modelled and implemented.

## Credits
The following projects provided valuable inspiration and reference implementaitons during the development of this frameowrk:
- [**Georgios Drosogiannis's**](https://github.com/George-Dros) [Volatility Surface Visualisation](https://github.com/George-Dros/Volatility_Surface) and [Interactive Black-Scholes Heatmaps](https://github.com/George-Dros/Black-Scholes-Interactive-heatmap)
- [**Killa Voillaume's**](https://github.com/KilianVoillaume) [Options Greek Visualizer](https://github.com/KilianVoillaume/Greeks_Streamlit_APP/tree/main).

## References
The following materials that were used to produce the descriptions are the following:
- Sinclair, E., 2010. Option trading: Pricing and volatility strategies and techniques. John Wiley & Sons.
- Passarelli, D., 2012. Trading options Greeks: How time, volatility, and other pricing factors drive profits. John Wiley & Sons.
- McMillan, L.G., 2002. Study Guide for the 4th Edition of Options as a Strategic Investment. Penguin.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
