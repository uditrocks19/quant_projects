"""
Cross-check: price a European call with the Monte Carlo engine in this
project and confirm it converges to the closed-form Black-Scholes price
from Project 2 (../black_scholes) within a few cents at 100k+ simulations.

Run: env\\Scripts\\python.exe compare_blackscholes_montecarlo.py
"""

import sys
from pathlib import Path

from monte_carlo_pricer import simulate_gbm, monte_carlo_price
from euro_call_pv import european_call

# black_scholes lives in a sibling project with no installed package,
# so reach its src/ dir on sys.path to import the BlackScholes class.
BLACK_SCHOLES_SRC = Path(__file__).resolve().parent.parent / "black_scholes" / "src"
sys.path.insert(0, str(BLACK_SCHOLES_SRC))

from options.blackscholes import BlackScholes  # noqa: E402


def cross_check_european_call(
    S0, K, r, sigma, T, n_paths=100_000, seed=None, tol=0.05
):
    """
    Price a European call two ways - Monte Carlo (GBM simulation) and the
    closed-form Black-Scholes formula - and confirm they agree.

    A European call has no path dependency, so simulating a single step
    straight to expiry (n_steps=1) is enough and is far cheaper than
    stepping through the full path at 100k+ simulations.

    Returns a dict with both prices, their difference, the MC standard
    error, and whether the two prices agree within `tol`.
    """
    paths = simulate_gbm(S0, r, sigma, T, n_steps=1, n_paths=n_paths, seed=seed)
    payoffs = european_call(paths, K)
    mc_price, mc_std_error = monte_carlo_price(payoffs, r, T)

    bs_price = BlackScholes(S0, K, T, r, sigma).call_price()

    diff = abs(mc_price - bs_price)

    return {
        "mc_price": mc_price,
        "mc_std_error": mc_std_error,
        "bs_price": bs_price,
        "diff": diff,
        "converged": diff <= tol,
        "n_paths": n_paths,
    }


if __name__ == "__main__":
    result = cross_check_european_call(
        S0=100, K=100, r=0.04, sigma=0.2, T=1.0, n_paths=200_00000, seed=42
    )

    print(f"Monte Carlo price : {result['mc_price']:.4f}  (SE: {result['mc_std_error']:.4f})")
    print(f"Black-Scholes price: {result['bs_price']:.4f}")
    print(f"Difference         : {result['diff']:.4f}")
    print(f"Converged within {result['diff']:.4f} <= tolerance: {result['converged']}")

    assert result["converged"], "Monte Carlo price did not converge to Black-Scholes price"
