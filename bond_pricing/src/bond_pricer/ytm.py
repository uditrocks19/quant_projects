from scipy.optimize import brentq

from .pricing import price_bond
from .day_count import year_fraction


def solve_ytm(cashflows, settlement_date, market_price, frequency=1, day_count="ACT/365"):
    """
    Solves for yield to maturity: the flat discount rate that makes
    price_bond(cashflows, ...) equal a given market price.
    """
    def f(y):
        return price_bond(cashflows, settlement_date, y, frequency, day_count) - market_price

    lo, hi = -0.99, 5.0  # -99% to 500% yield, plenty wide for any real bond

    return brentq(f, lo, hi, xtol=0.001)


def macaulay_duration(
    cashflows,
    settlement_date,
    market_rate,
    frequency,
    day_count="ACT/365"
):
    pv = 0
    sv = 0
    for transaction_date, cash in cashflows:
        t = year_fraction(settlement_date, transaction_date, day_count)
        pv_1 = cash / (1 + market_rate / frequency) ** (frequency * t)
        pv += pv_1
        sv += t * pv_1
    return sv / pv


def modified_duration(
    cashflows,
    settlement_date,
    market_rate,
    frequency,
    day_count="ACT/365"
):
    modified_dur = macaulay_duration(
        cashflows,
        settlement_date,
        market_rate,
        frequency,
        day_count,
    ) / (1 + market_rate / frequency)
    return modified_dur


def calculate_convexity(
        cashflows,
        settlement_date,
        market_rate,
        frequency,
        day_count="ACT/365"
):
    price = price_bond(cashflows, settlement_date, market_rate, frequency, day_count)

    con = 0
    for transaction_date, cashflow in cashflows:
        t = year_fraction(settlement_date, transaction_date, day_count)
        con += cashflow * t * (t + 1 / frequency) / (1 + market_rate / frequency) ** (frequency * t + 2)

    return con / price
