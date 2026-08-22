import numpy as np

def european_call(paths, K):
    # final stock price of every path
    ST = paths[:, -1]

    # call payoff max(ST - K, 0)
    payoffs = np.maximum(ST - K, 0)

    return payoffs