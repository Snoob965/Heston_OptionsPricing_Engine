# 📈 Advanced Options Pricing Engine: Heston Stochastic Volatility

A Python-based quantitative finance engine implementing the **Heston Model** to price European options and visualize 3D implied volatility surfaces. This project focuses on overcoming the limitations of constant-volatility models through vectorized Monte Carlo simulations and advanced discretization schemes.

---

## 🧵 The String of Thought: Why the Heston Model?

### 1. The Flaw of Black-Scholes
The Black-Scholes-Merton (BSM) model is the foundation of options pricing, but it relies on a fatal assumption: that asset volatility remains constant over time. In real financial markets, this is demonstrably false. Markets exhibit "volatility clustering" (large swings follow large swings) and "leverage effects" (volatility increases as asset prices drop). When plotted, real-world implied volatilities form a "smile" or "smirk," which BSM cannot natively replicate.

### 2. The Heston Solution
The Heston Model fixes this by treating variance not as a constant, but as a stochastic (randomized) process of its own. It models the asset price and its variance as two correlated geometric Brownian motions:

Asset Price Process: 
$$dS_t = r S_t dt + \sqrt{v_t} S_t dW_t^S$$

Variance Process (CIR): 
$$dv_t = \kappa(\theta - v_t)dt + \sigma \sqrt{v_t} dW_t^v$$

Where $dW_t^S dW_t^v = \rho dt$ (Correlation between price and volatility). This allows the model to capture the reality that when equities crash, volatility heavily spikes (a negative correlation, $\rho < 0$).

### 3. The Computational Challenge & Architecture
Because the Heston SDEs cannot be solved with a simple closed-form algebraic formula like Black-Scholes, pricing requires either complex characteristic function integration or **Monte Carlo Simulation**. 

This engine utilizes a highly optimized Monte Carlo approach mirroring quantitative desk environments:
* **Vectorized Processing:** Instead of utilizing slow Python `for` loops across individual paths, the engine leverages `NumPy` to process tens of thousands of simulated paths and time steps simultaneously in contiguous memory blocks.
* **Euler-Maruyama Discretization:** Time is sliced into discrete steps to simulate the continuous-time stochastic differential equations.
* **Full Truncation Scheme:** A critical edge case in the Heston model is that discrete simulation can result in mathematically impossible negative variances (violating the Feller condition $2\kappa\theta > \sigma^2$). This engine implements a Full Truncation scheme, mathematically enforcing $v_t = \max(v_t, 0)$ at each micro-step to prevent simulation collapse.

---

## 📊 Output Visualization: 3D Volatility Surface

Below is a screen recording of the engine's interactive PyQt5 output. By calculating the European Call price across a grid of differing Strike Prices ($K$) and Maturities ($T$), the engine renders a 3D visualization of the options pricing landscape.


https://github.com/user-attachments/assets/e514a9d0-2dd6-4575-8e6e-1329a966ddff


---

## 🚀 Technical Specifications

* **Language:** Python 3.10+
* **Vectorized Math Engine:** `numpy`
* **Statistical Distributions:** `scipy.stats`
* **Interactive Rendering:** `matplotlib` with the `PyQt5` backend for standalone GUI window generation, bypassing standard Tkinter limitations.
* **Greeks Calculation:** Implements central finite difference methods to calculate option Delta ($\Delta$).

## 💻 Quick Start
Ensure Python is installed, then install the dependencies and run the engine.
```bash
# Clone the repository
git clone [https://github.com/Snoob965/heston-pricing-engine.git](https://github.com/Snoob965/heston-pricing-engine.git)
cd heston-pricing-engine

# Install required mathematical and GUI libraries
pip install -r requirements.txt

# Execute the pricing engine and launch the interactive 3D surface
python heston_engine.py

https://github.com/user-attachments/assets/762e4e2d-8def-4f8b-a99a-1ff5c8d16ae5

