import numpy as np
import scipy.stats as si
import matplotlib
matplotlib.use('Qt5Agg')  # Bypassing Tkinter, using PyQt5
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class HestonPricer:
    def __init__(self, S0, v0, kappa, theta, sigma, rho, r):
        self.S0 = S0
        self.v0 = v0
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.r = r

    def simulate_paths(self, T, steps, paths):
        dt = T / steps
        Z1 = np.random.normal(size=(paths, steps))
        Z2 = self.rho * Z1 + np.sqrt(1 - self.rho**2) * np.random.normal(size=(paths, steps))
        S = np.zeros((paths, steps + 1))
        v = np.zeros((paths, steps + 1))
        S[:, 0] = self.S0
        v[:, 0] = self.v0
        for t in range(steps):
            v_t = np.maximum(v[:, t], 0)
            S[:, t+1] = S[:, t] * np.exp((self.r - 0.5 * v_t) * dt + np.sqrt(v_t * dt) * Z1[:, t])
            v[:, t+1] = v[:, t] + self.kappa * (self.theta - v_t) * dt + self.sigma * np.sqrt(v_t * dt) * Z2[:, t]
        return S

    def price_european_call(self, K, T, steps=100, paths=10000):
        S_paths = self.simulate_paths(T, steps, paths)
        payoffs = np.maximum(S_paths[:, -1] - K, 0)
        price = np.exp(-self.r * T) * np.mean(payoffs)
        return price

    def calculate_delta(self, K, T, steps=100, paths=10000, dS=1.0):
        original_S0 = self.S0
        self.S0 = original_S0 + dS
        price_up = self.price_european_call(K, T, steps, paths)
        self.S0 = original_S0 - dS
        price_down = self.price_european_call(K, T, steps, paths)
        self.S0 = original_S0
        return (price_up - price_down) / (2 * dS)

    def plot_volatility_surface(self, strikes, maturities):
        K_grid, T_grid = np.meshgrid(strikes, maturities)
        prices = np.zeros_like(K_grid, dtype=float)
        print("Calculating surface points. This may take a moment...")
        for i in range(K_grid.shape[0]):
            for j in range(K_grid.shape[1]):
                prices[i, j] = self.price_european_call(K=K_grid[i, j], T=T_grid[i, j], paths=5000)
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(K_grid, T_grid, prices, cmap='viridis', edgecolor='none')
        ax.set_title('Heston Model: Call Option Prices across Strike & Maturity')
        ax.set_xlabel('Strike Price (K)')
        ax.set_ylabel('Time to Maturity (T)')
        ax.set_zlabel('Option Price')
        fig.colorbar(surf, shrink=0.5, aspect=5)
        
        fig.savefig("heston_surface.png", dpi=300, bbox_inches='tight')
        print("\nSuccess: High-res 'heston_surface.png' saved to your folder.")
        print("Opening interactive 3D window...")
        plt.show()

# Execution Block
engine = HestonPricer(S0=100, v0=0.04, kappa=2.0, theta=0.04, sigma=0.3, rho=-0.7, r=0.03)
K_test = 100
T_test = 1.0
print("--- Heston Model Pricing Engine ---")
price = engine.price_european_call(K=K_test, T=T_test)
print(f"European Call Price (K={K_test}, T={T_test}): ${price:.4f}")
delta = engine.calculate_delta(K=K_test, T=T_test)
print(f"Option Delta (Finite Difference): {delta:.4f}\n")
strikes = np.linspace(80, 120, 10)
maturities = np.linspace(0.1, 2.0, 10)
engine.plot_volatility_surface(strikes, maturities)