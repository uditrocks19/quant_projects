from blackscholes import BlackScholes
from scipy.optimize import brentq


class IVSolver:

    def solve(self, S, K, T, r, market_price):

        def objective(sigma):
            bs = BlackScholes(S, K, T, r, sigma)
            return bs.call_price() - market_price

        return brentq(objective, 1e-5, 5.0)