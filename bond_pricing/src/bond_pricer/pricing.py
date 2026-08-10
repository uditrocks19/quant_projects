from .day_count import year_fraction, add_months


def price_bond(
        cashflows,
        settelement_date,
        discount_rate,
        frequency=1,
        day_count="ACT/365"
):
    """
    Calculate the present value (dirty price) of a bond's future cash flows.

    cashflows:
        List of (date, amount)

    settlement_date:
        Date on which we are valuing the bond

    discount_rate:
        Annual discount rate, e.g. 0.05 for 5%

    frequency:
        semiannual/annual/monthly

    day_count:
        Day count convention used to turn date spans into year fractions,
        see day_count.year_fraction (default "ACT/365").
    """
    price = 0.0

    for payment_date, amount in cashflows:

        t = year_fraction(settelement_date, payment_date, day_count)

        # present value of this cashflow
        pv = (amount) / (1 + discount_rate / frequency) ** (t * frequency)
        price += pv

    return price


def accrued_interest(
        cashflows,
        settlement_date,
        coupon_amount,
        frequency=1,
        day_count="ACT/365"
):
    """
    Interest earned since the last coupon date, not yet paid out.

    coupon_amount:
        The regular coupon cash amount per period (excluding any final
        redemption/principal amount).

    The last coupon date is inferred by stepping back one coupon period
    (12/frequency months) from the next upcoming cashflow date.
    """
    future_dates = sorted(payment_date for payment_date, _ in cashflows if payment_date > settlement_date)
    if not future_dates:
        return 0.0

    next_coupon_date = future_dates[0]
    months_in_period = 12 // frequency
    last_coupon_date = add_months(next_coupon_date, -months_in_period)

    accrued_period = year_fraction(last_coupon_date, settlement_date, day_count)
    full_period = year_fraction(last_coupon_date, next_coupon_date, day_count)

    return coupon_amount * (accrued_period / full_period)


def clean_price(
        cashflows,
        settlement_date,
        discount_rate,
        coupon_amount,
        frequency=1,
        day_count="ACT/365"
):
    """
    Quoted price: dirty price minus accrued interest.
    """
    dirty_price = price_bond(cashflows, settlement_date, discount_rate, frequency, day_count)
    ai = accrued_interest(cashflows, settlement_date, coupon_amount, frequency, day_count)
    return dirty_price - ai
