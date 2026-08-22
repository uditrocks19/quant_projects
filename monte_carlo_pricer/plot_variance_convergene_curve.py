import matplotlib.pyplot as plt

from monte_carlo_pricer import simulate_gbm, monte_carlo_price
from euro_call_pv import european_call


def mc_standard_error(
    S0,
    r,
    sigma,
    T,
    n_steps,
    n_paths,
    seed,
    K
):

    paths = simulate_gbm(
        S0,
        r,
        sigma,
        T,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=seed
    )

    payoffs = european_call(
        paths,
        K
    )

    _, mc_std_error = monte_carlo_price(
        payoffs,
        r,
        T
    )

    return mc_std_error


n_paths = [
    100,
    1000,
    10000,
    100000]

errors = []

for n in n_paths:

    error = mc_standard_error(
        S0=100,
        r=0.04,
        sigma=0.20,
        T=1,
        n_steps=252,
        n_paths=n,
        seed=42,
        K=120
    )

    errors.append(error)


plt.plot(n_paths, errors, marker="o")

plt.xscale("log")

plt.xlabel("Number of Simulations")
plt.ylabel("Monte Carlo Standard Error")
plt.title("Monte Carlo Standard Error vs Number of Simulations")

plt.grid(True)

plt.show()