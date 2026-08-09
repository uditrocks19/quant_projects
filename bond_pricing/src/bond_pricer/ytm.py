from scipy.optimize import brentq

from .pricing import price_bond


   


def solve_ytm(cashflows, settlement_date, market_price, frequency=1):
    """
    Solves for yield to maturity: the flat discount rate that makes
    price_bond(cashflows, ...) equal a given market price.
    """
    def f(y):
        return price_bond(cashflows, settlement_date, y, frequency) - market_price

    lo, hi = -0.99, 5.0  # -99% to 500% yield, plenty wide for any real bond

    return brentq(f, lo, hi, xtol=0.001)


def macaulay_duration(
    cashflows,
    settlement_date,
    market_rate,
    frequency
):
    pv = 0
    sv = 0
    for transaction_date, cash in cashflows:
        t = (transaction_date - settlement_date).days
        t = t / 365.0
        pv_1 = cash / (1 + market_rate / frequency) ** (frequency * t)
        pv += pv_1
        sv += t * pv_1
    return sv / pv


def modified_duration(
    cashflows,
    settlement_date,
    market_rate,
    frequency
):
    modified_dur = macaulay_duration(
        cashflows,
        settlement_date,
        market_rate,
        frequency,
    ) / (1 + market_rate / frequency)
    return modified_dur


def calculate_convexity(
        cashflows,
        settlement_date,
        market_rate,
        frequency
):
    price = price_bond(cashflows, settlement_date, market_rate, frequency)

    con = 0
    for transaction_date, cashflow in cashflows:
        t = (transaction_date - settlement_date).days
        t = t / 365.0
        con += cashflow * t * (t + 1 / frequency) / (1 + market_rate / frequency) ** (frequency * t + 2)

    return con / price