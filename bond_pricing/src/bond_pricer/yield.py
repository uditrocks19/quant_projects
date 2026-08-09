from scipy.optimize import brentq
from pricing import price_bond

def solve_ytm(
        cashflows,
        settlement_date,
        market_price,
        frequency=1
):
    def objective(y):
        calculated_price = price_bond(
            cashflows,
            settlement_date,
            y,
            frequency
        )

        return calculated_price - market_price
    ytm = brentq(
        objective,
        -0.99,
        1.0
    )

    return ytm