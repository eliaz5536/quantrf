import streamlit as st


def _section(title, purpose, equations, terms, behaviour):
    with st.expander(title, expanded=True):
        st.markdown(purpose)
        for equation in equations:
            st.latex(equation)
        st.markdown(f"**Terms.** {terms}")
        st.markdown(f"**Behaviour.** {behaviour}")


def black_scholes(model="bsm"):
    if model == "black76":
        _section(
            "Black (1976) mathematics",
            "Black's model prices an option on a futures or forward contract. The futures price is treated as the tradable state variable.",
            [
                r"d_1 = \frac{\ln(F/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}",
                r"C = e^{-rT}\left[F N(d_1) - K N(d_2)\right]",
                r"P = e^{-rT}\left[K N(-d_2) - F N(-d_1)\right]",
            ],
            r"$F$ is the futures or forward price, $K$ is strike, $T$ is time to maturity, $r$ is the continuously compounded risk-free rate, $\sigma$ is volatility, and $N(\cdot)$ is the standard normal cumulative distribution function.",
            "Higher futures prices increase call values and decrease put values. Volatility and maturity increase the value of optionality, while discounting reduces the present value of future payoffs.",
        )
        return

    _section(
        "Black-Scholes-Merton mathematics",
        "The model assumes that the continuously compounded return of the asset has a deterministic drift and normally distributed random shocks.",
        [
            r"dS_t = (r-q)S_t\,dt + \sigma S_t\,dW_t",
            r"d_1 = \frac{\ln(S/K) + (r-q+\frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}",
            r"C = S e^{-qT}N(d_1) - K e^{-rT}N(d_2)",
            r"P = K e^{-rT}N(-d_2) - S e^{-qT}N(-d_1)",
            r"C-P = S e^{-qT} - K e^{-rT}",
            r"\Delta_C=e^{-qT}N(d_1),\quad \Gamma=\frac{e^{-qT}\phi(d_1)}{S\sigma\sqrt{T}},\quad \nu=S e^{-qT}\sqrt{T}\phi(d_1)",
        ],
        r"$S$ is spot price, $K$ is strike, $T$ is time to maturity, $r$ is the risk-free rate, $q$ is continuous dividend yield, $\sigma$ is volatility, $W_t$ is Brownian motion, $N$ is the normal CDF, and $\phi$ is the normal density.",
        "The drift $r-q$ moves the expected asset level under the risk-neutral measure. Volatility widens the range of possible terminal prices, which increases the value of both calls and puts. Delta measures first-order spot sensitivity, gamma measures curvature, and vega measures volatility sensitivity.",
    )


def greeks(model="bsm"):
    if model == "black76":
        _section(
            "Black (1976) Greeks mathematics",
            "The Greeks are partial derivatives of the discounted Black futures-option value. They quantify how the option responds to changes in futures price, volatility, time, and interest rates.",
            [
                r"d_1=\frac{\ln(F/K)+\frac12\sigma^2T}{\sigma\sqrt{T}},\qquad d_2=d_1-\sigma\sqrt{T}",
                r"\Delta_C=e^{-rT}N(d_1),\qquad \Delta_P=-e^{-rT}N(-d_1)",
                r"\Gamma_C=\Gamma_P=\frac{e^{-rT}\phi(d_1)}{F\sigma\sqrt{T}}",
                r"\nu_C=\nu_P=F e^{-rT}\sqrt{T}\phi(d_1)",
                r"\Theta_C=-\frac{F e^{-rT}\phi(d_1)\sigma}{2\sqrt{T}}+r e^{-rT}\left[K N(d_2)-F N(d_1)\right]",
                r"\Theta_P=-\frac{F e^{-rT}\phi(d_1)\sigma}{2\sqrt{T}}+r e^{-rT}\left[K N(-d_2)-F N(-d_1)\right]",
                r"\rho_C=-T e^{-rT}\left[F N(d_1)-K N(d_2)\right] = -T C",
                r"\rho_P=-T e^{-rT}\left[K N(-d_2)-F N(-d_1)\right] = -T P",
            ],
            r"$\Delta$ measures futures-price sensitivity, $\Gamma$ measures the change in Delta, $\nu$ (Vega) measures volatility sensitivity, $\Theta$ measures time decay per year, and $\rho$ measures sensitivity to the risk-free rate. $F$ is futures price, $K$ is strike, $T$ is maturity, $r$ is the rate, $\sigma$ is volatility, $N$ is the normal CDF, and $\phi$ is the normal density.",
            "Calls have positive Delta and puts have negative Delta. Gamma and Vega are generally positive for both option types. Black (1976) discounts the futures exposure, so the rate sensitivities include the effect of changing the discount factor.",
        )
        return

    _section(
        "Black-Scholes-Merton Greeks mathematics",
        "The Greeks are derivatives of the option price with respect to the model inputs. They describe local risk: the effect of a small change while the other inputs are held fixed.",
        [
            r"d_1=\frac{\ln(S/K)+(r-q+\frac12\sigma^2)T}{\sigma\sqrt{T}},\qquad d_2=d_1-\sigma\sqrt{T}",
            r"\Delta_C=\frac{\partial C}{\partial S}=e^{-qT}N(d_1),\qquad \Delta_P=\frac{\partial P}{\partial S}=-e^{-qT}N(-d_1)",
            r"\Gamma_C=\Gamma_P=\frac{\partial^2 V}{\partial S^2}=\frac{e^{-qT}\phi(d_1)}{S\sigma\sqrt{T}}",
            r"\nu_C=\nu_P=\frac{\partial V}{\partial\sigma}=S e^{-qT}\sqrt{T}\phi(d_1)",
            r"\Theta_C=\frac{\partial C}{\partial t}=-\frac{S e^{-qT}\phi(d_1)\sigma}{2\sqrt{T}}-rK e^{-rT}N(d_2)+qS e^{-qT}N(d_1)",
            r"\Theta_P=\frac{\partial P}{\partial t}=-\frac{S e^{-qT}\phi(d_1)\sigma}{2\sqrt{T}}+rK e^{-rT}N(-d_2)-qS e^{-qT}N(-d_1)",
            r"\rho_C=\frac{\partial C}{\partial r}=KT e^{-rT}N(d_2),\qquad \rho_P=\frac{\partial P}{\partial r}=-KT e^{-rT}N(-d_2)",
        ],
        r"$\Delta$ is change in option value per one unit of spot price, $\Gamma$ is change in Delta per unit of spot price, $\nu$ (Vega) is change per unit of volatility, $\Theta$ is time decay, and $\rho$ is change per unit of the continuously compounded rate. $S$ is spot, $K$ is strike, $T$ is time to maturity, $r$ is the risk-free rate, $q$ is dividend yield, $\sigma$ is volatility, $N$ is the normal CDF, and $\phi$ is the normal density.",
        "Call Delta is positive and put Delta is negative. Gamma is largest near the strike and for short maturities, where the option value bends most sharply with spot price. Vega is usually largest near the strike and for longer maturities. Theta is commonly negative for long option positions, while call Rho is positive and put Rho is negative when rates increase.",
    )


def volatility_surface():
    _section(
        "Implied-volatility surface mathematics",
        "The surface in this application inverts observed option prices to find the volatility that makes the Black-Scholes price equal to the market price.",
        [
            r"V_{\mathrm{market}} = V_{\mathrm{BS}}(S,K,T,r,q,\sigma_{\mathrm{imp}})",
            r"\sigma_{\mathrm{imp}} = \operatorname*{arg\,zero}_{\sigma>0}\left[V_{\mathrm{BS}}(S,K,T,r,q,\sigma)-V_{\mathrm{market}}\right]",
            r"F=S e^{(r-q)T}, \qquad k=\ln(K/F)",
            r"w(k,T)=T\,\sigma_{\mathrm{imp}}(k,T)^2",
        ],
        r"$\sigma_{\mathrm{imp}}$ is implied volatility, $F$ is the forward price, $k$ is log-moneyness, and $w$ is total implied variance. The two surface axes are maturity $T$ and either strike $K$ or log-moneyness $k$.",
        "A flat volatility would produce the same volatility for every strike and maturity. Real markets usually show a smile or skew, so the surface changes with moneyness and time. Interpolation fills gaps between observed contracts; SVI fits a smooth total-variance slice to each expiry.",
    )


def binomial(model):
    descriptions = {
        "crr": (
            "Cox-Ross-Rubinstein mathematics",
            [
                r"\Delta t=T/N,\qquad u=e^{\sigma\sqrt{\Delta t}},\qquad d=u^{-1}",
                r"p=\frac{e^{r\Delta t}-d}{u-d},\qquad S_{j,i}=S_0u^{j-i}d^i",
                r"V_{j,i}=e^{-r\Delta t}\left[pV_{j+1,i}+(1-p)V_{j+1,i+1}\right]",
                r"C_{N,i}=\max(S_{N,i}-K,0),\qquad P_{N,i}=\max(K-S_{N,i},0)",
            ],
            "CRR uses multiplicative up and down moves chosen so the tree matches the local volatility and risk-neutral drift. Backward induction discounts the expected continuation value.",
        ),
        "jr": (
            "Jarrow-Rudd mathematics",
            [
                r"\Delta t=T/N,\qquad u=e^{(r-\frac12\sigma^2)\Delta t+\sigma\sqrt{\Delta t}}",
                r"d=e^{(r-\frac12\sigma^2)\Delta t-\sigma\sqrt{\Delta t}},\qquad p=\frac12",
                r"V_{j,i}=e^{-r\Delta t}\left[\frac12V_{j+1,i+1}+\frac12V_{j+1,i}\right]",
            ],
            "Jarrow-Rudd fixes the probability at one half and puts the risk-neutral drift into the up and down factors. This produces a recombining lattice with symmetric branch probabilities.",
        ),
        "lr": (
            "Leisen-Reimer mathematics",
            [
                r"d_1=\frac{\ln(S_0/K)+(r+\frac12\sigma^2)T}{\sigma\sqrt{T}},\qquad d_2=d_1-\sigma\sqrt{T}",
                r"p=H(d_2,N),\qquad p'=H(d_1,N)",
                r"u=e^{r\Delta t}\frac{p'}{p},\qquad d=\frac{e^{r\Delta t}-pu}{1-p}",
                r"V_{j,i}=e^{-r\Delta t}\left[pV_{j+1,i}+(1-p)V_{j+1,i+1}\right]",
            ],
            "Leisen-Reimer uses a Peizer-Pratt inversion $H$ to map the Black-Scholes probabilities into a finite tree. The implementation forces an odd number of steps because the inversion is designed around a central strike node.",
        ),
        "tian": (
            "Tian mathematics",
            [
                r"R=e^{r\Delta t},\qquad V=e^{\sigma^2\Delta t}",
                r"u=\frac{RV}{2}\left(V+1+\sqrt{V^2+2V-3}\right)",
                r"d=\frac{RV}{2}\left(V+1-\sqrt{V^2+2V-3}\right),\qquad p=\frac{R-d}{u-d}",
                r"V_{j,i}=e^{-r\Delta t}\left[pV_{j+1,i}+(1-p)V_{j+1,i+1}\right]",
            ],
            "Tian chooses the branch factors to match additional moments of the lognormal diffusion beyond the first two moments. This can improve convergence for some parameter regions, although numerical stability still depends on the time step.",
        ),
    }
    title, equations, behaviour = descriptions[model]
    _section(
        title,
        "A binomial tree replaces continuous asset evolution by two possible moves at each short interval and values the derivative by backward induction.",
        equations,
        r"$S_0$ is the initial asset price, $K$ is strike, $T$ is maturity, $N$ is the number of steps, $\Delta t$ is the step length, $u$ and $d$ are up and down factors, $p$ is the risk-neutral probability, and $V$ is an option value.",
        behaviour,
    )


def trinomial():
    _section(
        "Trinomial tree mathematics",
        "A trinomial tree allows the asset to move up, remain near its current level, or move down at every time step. The extra branch can improve flexibility and numerical stability.",
        [
            r"\Delta t=T/N,\qquad S_{j,i}=S_0u^{i}m^{j-|i|}d^{-i}\quad\text{(schematic node notation)}",
            r"p_u+p_m+p_d=1",
            r"V_{j,i}=e^{-r\Delta t}\left[p_uV_{j+1,i+1}+p_mV_{j+1,i}+p_dV_{j+1,i-1}\right]",
            r"V_{N,i}=\max(S_{N,i}-K,0)\quad\text{for a call}",
        ],
        r"$p_u$, $p_m$, and $p_d$ are risk-neutral probabilities for up, middle, and down moves. The probabilities are calibrated so that they sum to one and reproduce the desired drift and variance. $m$ denotes the middle branch factor.",
        "The middle branch lets the lattice represent a wider range of local behaviour than a binomial tree. The option value is the discounted risk-neutral expectation over all three possible next states.",
    )


def finite_difference(model):
    _section(
        f"{model} finite-difference mathematics",
        "The finite-difference method replaces the continuous Black-Scholes PDE with algebraic equations on a grid of log-prices and times.",
        [
            r"\frac{\partial V}{\partial t}+(r-q)S\frac{\partial V}{\partial S}+\frac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}-rV=0",
            r"x=\ln S,\qquad \mu=r-q-\frac12\sigma^2",
            r"V_t+\mu V_x+\frac12\sigma^2V_{xx}-rV=0",
            r"A V^{j}=B V^{j+1}+\text{boundary terms}",
        ],
        r"$V(S,t)$ is the option value, $S$ is spot price, $t$ is time, $r$ is the discount rate, $q$ is dividend yield, and $\sigma$ is volatility. $A$ and $B$ are tridiagonal finite-difference operators on the grid.",
        f"The grid approximates how value diffuses through price space as time moves toward the present. In this repository the {model} public pricing route is currently a stable Black-Scholes fallback, while the displayed sensitivity curve still illustrates the model interface.",
    )


def interest_rates(model):
    if model == "cir":
        _section(
            "Cox-Ingersoll-Ross mathematics",
            "The CIR model describes a short rate that mean-reverts while its random volatility scales with the square root of the rate.",
            [
                r"dr_t=\kappa(\theta-r_t)dt+\sigma\sqrt{r_t}\,dW_t",
                r"E[r_t\mid r_0]=\theta+(r_0-\theta)e^{-\kappa t}",
                r"P(0,T)=\exp\left(A(T)-B(T)r_0\right),\qquad y(0,T)=-\frac{\ln P(0,T)}{T}",
            ],
            r"$r_t$ is the short rate, $\kappa$ is mean-reversion speed, $\theta$ is the long-run rate, and $\sigma$ controls rate volatility. The square-root term reduces randomness near zero.",
            r"Rates are pulled toward $\theta$. A larger $\kappa$ produces faster reversion; a larger $\sigma$ creates more variable rate paths and changes bond prices and yields.",
        )
    else:
        _section(
            "Vasicek mathematics",
            "The Vasicek model uses a Gaussian mean-reverting short-rate process.",
            [
                r"dr_t=\kappa(\theta-r_t)dt+\sigma\,dW_t",
                r"E[r_t\mid r_0]=\theta+(r_0-\theta)e^{-\kappa t}",
                r"P(0,T)=A(T)e^{-B(T)r_0},\qquad y(0,T)=-\frac{\ln P(0,T)}{T}",
            ],
            r"$r_t$ is the short rate, $\kappa$ is mean-reversion speed, $\theta$ is the long-run level, and $\sigma$ is constant instantaneous volatility.",
            r"The rate tends toward the long-run mean, but unlike CIR it may become negative because the Gaussian shock is additive rather than proportional to $\sqrt{r_t}$.",
        )


def american_options(model):
    common_terms = (
        r"$S$ is spot, $K$ is strike, $T$ is maturity, $r$ is the risk-free "
        r"rate, $b$ is cost of carry, $\sigma$ is volatility, $N$ is the "
        r"normal CDF, and $\Pi$ is immediate exercise payoff."
    )

    descriptions = {
        "1993": (
            "Bjerksund-Stensland (1993) mathematics",
            "The 1993 approximation represents early exercise with a flat critical boundary. It replaces the unknown optimal stopping surface with a tractable exercise trigger and an analytic continuation value.",
            [
                r"\Pi_C(S)=\max(S-K,0),\qquad \Pi_P(S)=\max(K-S,0)",
                r"V_{\mathrm{Am}}(S)\approx V_{\mathrm{BS}}(S)+\operatorname{EEP}(S;B)",
                r"\text{exercise when }S\geq B\text{ for a call},\qquad \text{exercise when }S\leq B\text{ for a put}",
                r"B=\text{critical exercise price},\qquad V(B)=\Pi(B),\quad \frac{\partial V}{\partial S}(B)=\frac{\partial\Pi}{\partial S}(B)",
            ],
            common_terms + r" The boundary $B$ is chosen using value matching and smooth pasting; $\operatorname{EEP}$ is the early-exercise premium.",
            "The approximation is most sensitive to the estimated boundary. A call is more likely to be exercised early when carry is low, especially when dividends reduce the benefit of continuing to hold the option.",
        ),
        "2002": (
            "Bjerksund-Stensland (2002) mathematics",
            "The 2002 approximation improves the exercise-boundary representation by using a time-dependent trigger. The option is valued as a European option plus the value of exercising optimally at the approximated boundary.",
            [
                r"V_{\mathrm{Am}}(S,t)\approx V_{\mathrm{BS}}(S,t)+\operatorname{EEP}(S,t;B(t))",
                r"B(t)=B_0+(B_\infty-B_0)\left(1-e^{-\lambda(T-t)}\right)",
                r"\Pi_C(S)=\max(S-K,0),\qquad \Pi_P(S)=\max(K-S,0)",
                r"V(B(t),t)=\Pi(B(t)),\qquad V_S(B(t),t)=\Pi_S(B(t))",
            ],
            common_terms + r" $B(t)$ is the time-dependent critical boundary, $B_0$ and $B_\infty$ describe its endpoint levels, and $\lambda$ controls its transition toward maturity.",
            "The moving boundary captures the fact that the optimal exercise level changes as maturity approaches. Early exercise remains most relevant for dividend-paying calls and sufficiently in-the-money puts.",
        ),
        "1999": (
            "Ju-Zhong (1999) mathematics",
            "Ju-Zhong adds an early-exercise premium to the European option value and calibrates that premium to an approximated exercise boundary. In this application the calculation is evaluated with a refined American lattice using the Ju-Zhong model label.",
            [
                r"V_{\mathrm{Am}}=V_{\mathrm{Eur}}+\operatorname{EEP}",
                r"V_{\mathrm{Am}}(S,t)=\max\left(\Pi(S),\;e^{-r\Delta t}\mathbb{E}^{\mathbb{Q}}[V_{\mathrm{Am}}(S_{t+\Delta t},t+\Delta t)\mid S_t=S]\right)",
                r"u=e^{\sigma\sqrt{\Delta t}},\qquad d=u^{-1},\qquad \Delta t=T/N",
                r"p=\frac{e^{b\Delta t}-d}{u-d},\qquad V_{j,i}=\max\left(\Pi(S_{j,i}),e^{-r\Delta t}[pV_{j+1,i}+(1-p)V_{j+1,i+1}]\right)",
            ],
            common_terms + r" $\mathbb{Q}$ is the risk-neutral measure, $N$ is the number of lattice steps, and $u$, $d$, and $p$ are the up factor, down factor, and risk-neutral probability.",
            "The lattice checks exercise at every node, so the value is the greater of immediate exercise and discounted continuation. Increasing the number of steps generally reduces lattice discretisation error.",
        ),
        "1989": (
            "Brenner-Galai (1989) mathematics",
            "The Brenner-Galai approach expresses an American option as a European value plus an early-exercise correction. In this application the correction is obtained through the same refined early-exercise lattice used by the numerical approximation.",
            [
                r"V_{\mathrm{Am}}=V_{\mathrm{Eur}}+\operatorname{EEP}",
                r"\operatorname{EEP}=\sup_{\tau\leq T}\mathbb{E}^{\mathbb{Q}}\left[e^{-r\tau}\Pi(S_\tau)\right]-V_{\mathrm{Eur}}",
                r"V_{j,i}=\max\left(\Pi(S_{j,i}),e^{-r\Delta t}[pV_{j+1,i}+(1-p)V_{j+1,i+1}]\right)",
                r"S_{j,i}=S_0u^{j-i}d^i,\qquad u=e^{\sigma\sqrt{\Delta t}},\quad d=u^{-1}",
            ],
            common_terms + r" $\tau$ is an exercise time, $S_{j,i}$ is a lattice node, and $\operatorname{EEP}$ is the value of the early-exercise right above the European contract.",
            "The exercise feature creates an upper envelope over continuation and intrinsic value. The premium is usually larger for deep-in-the-money puts and for calls when dividends make early exercise economically attractive.",
        ),
    }

    title, purpose, equations, terms, behaviour = descriptions.get(
        str(model), descriptions["1993"]
    )
    _section(title, purpose, equations, terms, behaviour)


def monte_carlo(mode):
    if mode == "gbm":
        _section(
            "Monte Carlo and geometric Brownian motion",
            "The stock simulation uses the exact discretization of the risk-neutral geometric Brownian motion over each time step.",
            [
                r"dS_t=rS_tdt+\sigma S_tdW_t",
                r"S_{t+\Delta t}=S_t\exp\left((r-\frac12\sigma^2)\Delta t+\sigma\sqrt{\Delta t}Z\right),\qquad Z\sim N(0,1)",
                r"\mathbb{E}[S_T]=S_0e^{rT},\qquad \widehat{\mathbb{E}}[S_T]=\frac{1}{M}\sum_{m=1}^{M}S_T^{(m)}",
                r"\operatorname{SE}(\widehat{\mathbb{E}}[S_T])=\frac{s_{S_T}}{\sqrt{M}}",
            ],
            r"$S_t$ is the asset price, $S_0$ is its initial value, $r$ is the drift under the risk-neutral measure, $\sigma$ is volatility, $Z$ is a standard normal shock, and $M$ is the number of simulated paths.",
            "The paths spread more widely as volatility or maturity increases. The histogram approximates the terminal price distribution; the running mean becomes more stable as $M$ increases, illustrating the Law of Large Numbers.",
        )
    else:
        _section(
            "Law of Large Numbers for sample means",
            "Repeated independent samples show how an empirical average approaches the population mean.",
            [
                r"X_1,\ldots,X_n\overset{\mathrm{iid}}{\sim}F,\qquad \mathbb{E}[X_i]=\mu,\quad \operatorname{Var}(X_i)=\sigma^2",
                r"\bar X_n=\frac{1}{n}\sum_{i=1}^{n}X_i,\qquad \mathbb{E}[\bar X_n]=\mu,\qquad \operatorname{Var}(\bar X_n)=\frac{\sigma^2}{n}",
                r"\frac{1}{R}\sum_{j=1}^{R}\bar X_n^{(j)}\xrightarrow[R\to\infty]{\mathrm{a.s.}}\mu",
            ],
            r"$n$ is the observations per sample, $R$ is the number of repeated samples, $\mu$ is the population mean, and $\sigma^2$ is population variance.",
            "Larger samples make each sample mean less variable because its variance falls as $1/n$. More repetitions make the histogram and its running average better approximate the population behaviour.",
        )
