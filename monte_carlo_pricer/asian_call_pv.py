import numpy as np

def asian_call(paths, K):
    # average stock  price of every path

    average_price = np.mean(paths, axis=1)

    # asian call payoff
    payoffs = np.maximum(average_price - K)

    return payoffs