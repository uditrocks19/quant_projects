"""
Compare the standard error of plain Monte Carlo vs antithetic-variate
Monte Carlo for pricing a European call, at several path counts, to show
the variance reduction antithetic sampling buys for the same random-number
budget - and that antithetic can match plain MC's precision with fewer
total paths.

Run: env\\Scripts\\python.exe compare_variance_reduction.py
"""

from monte_carlo_pricer import (
    simulate_gbm,
    simulate_gbm_antithetic,
    monte_carlo_price,
    monte_carlo_price_antithetic,
)
from euro_call_pv import european_call

S0, K, r, sigma, T = 100, 100, 0.04, 0.2, 1.0


def run_comparison(n_paths, seed=42):
    plain_paths = simulate_gbm(S0, r, sigma, T, n_steps=1, n_paths=n_paths, seed=seed)
    plain_payoffs = european_call(plain_paths, K)
    plain_price, plain_se = monte_carlo_price(plain_payoffs, r, T)

    anti_paths = simulate_gbm_antithetic(S0, r, sigma, T, n_steps=1, n_paths=n_paths, seed=seed)
    anti_payoffs = european_call(anti_paths, K)
    anti_price, anti_se = monte_carlo_price_antithetic(anti_payoffs, r, T)

    return {
        "n_paths": n_paths,
        "plain_price": plain_price,
        "plain_se": plain_se,
        "anti_price": anti_price,
        "anti_se": anti_se,
        "se_reduction_pct": 1 - anti_se / plain_se,
        "variance_reduction_factor": (plain_se / anti_se) ** 2,
    }


if __name__ == "__main__":
    header = (
        f"{'n_paths':>10} | {'plain price':>12} {'plain SE':>10} | "
        f"{'anti price':>12} {'anti SE':>10} | {'SE reduction':>13} {'var factor':>10}"
    )
    print(header)
    print("-" * len(header))

    for n in [1_000, 10_000, 50_000, 100_000, 500_000]:
        r_ = run_comparison(n)
        print(
            f"{r_['n_paths']:>10} | "
            f"{r_['plain_price']:>12.4f} {r_['plain_se']:>10.4f} | "
            f"{r_['anti_price']:>12.4f} {r_['anti_se']:>10.4f} | "
            f"{r_['se_reduction_pct'] * 100:>12.1f}% {r_['variance_reduction_factor']:>9.2f}x"
        )
