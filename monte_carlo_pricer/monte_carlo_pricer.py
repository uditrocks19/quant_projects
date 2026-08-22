import numpy as np

def simulate_gbm(
        S0, r, sigma, T, n_steps, n_paths, seed=None
):

    # random number generator
    rng = np.random.default_rng(seed)

    # length of one time step
    dt = T / n_steps

    Z = rng.standard_normal((n_paths, n_steps))

    # GBM log return for each step
    log_returns =(
        (r - 0.5 * sigma ** 2) * dt
         + sigma * np.sqrt(dt) * Z
    )

    # Add all previous log returns
    cum_log_returns = (
        np.cumsum(log_returns, axis=1)
    )

    paths = S0 * np.exp(cum_log_returns)
    return paths


# paths = simulate_gbm(100, 0.04, 0.05, 1, 252, 10)

def simulate_gbm_antithetic(
        S0, r, sigma, T, n_steps, n_paths, seed=None
):
    # random number generator
    rng = np.random.default_rng(seed)

    # length of each step
    dt = T / n_steps

    Z = rng.standard_normal((n_paths // 2, n_steps))
    neg_Z = -Z
    Z = np.vstack([
        Z, neg_Z
    ])
    
     # GBM log return for each step
    log_returns =(
            (r - 0.5 * sigma ** 2) * dt
             + sigma * np.sqrt(dt) * Z
        )
    
        # Add all previous log returns
    cum_log_returns = (
            np.cumsum(log_returns, axis=1)
        )
    
    paths = S0 * np.exp(cum_log_returns)
    return paths
    



def monte_carlo_price(payoffs, r, T):

    # discount each payoff back to today
    discounted_payoffs = np.exp(-r * T) * payoffs


    # avg discounted payoffs
    price = np.mean(discounted_payoffs)
    # Standard error
    standard_error = (
        np.std(discounted_payoffs, ddof=1)
        / np.sqrt(len(discounted_payoffs))
    )

    return price, standard_error


def monte_carlo_price_antithetic(payoffs, r, T):
    # payoffs must be laid out as simulate_gbm_antithetic returns its
    # paths: first half from +Z, second half from -Z, row i paired with
    # row i + n_pairs. Averaging each pair BEFORE computing std is what
    # captures the variance reduction - pooling all payoffs and calling
    # monte_carlo_price on them would ignore the negative correlation
    # between the two branches and show no improvement.
    discounted_payoffs = np.exp(-r * T) * payoffs

    n_pairs = len(discounted_payoffs) // 2
    pair_avg = (
        discounted_payoffs[:n_pairs] + discounted_payoffs[n_pairs:]
    ) / 2

    price = np.mean(pair_avg)
    standard_error = np.std(pair_avg, ddof=1) / np.sqrt(n_pairs)

    return price, standard_error
