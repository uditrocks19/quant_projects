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


def price_from_curve(
        cashflows,
        settlement_date,
        spot_rates,
        day_count="ACT/365"
):
    """
    Present value of a bond's cashflows discounted off a zero-coupon spot
    rate curve (e.g. bootstrapping.discount_factors_to_spot_rates), instead
    of a single flat discount rate.

    cashflows:
        List of (date, amount)

    spot_rates:
        {maturity_year: annually-compounded spot rate}. Cashflow dates that
        don't fall on a curve year are linearly interpolated between the
        surrounding rates; dates outside the curve's range use the nearest
        end point's rate (flat extrapolation).
    """
    known_years = sorted(spot_rates)
    price = 0.0

    for payment_date, amount in cashflows:
        t = year_fraction(settlement_date, payment_date, day_count)
        r = _interpolate_spot_rate(t, known_years, spot_rates)
        price += amount / (1 + r) ** t

    return price


def _interpolate_spot_rate(t, known_years, spot_rates):
    if t <= known_years[0]:
        return spot_rates[known_years[0]]
    if t >= known_years[-1]:
        return spot_rates[known_years[-1]]

    for y1, y2 in zip(known_years, known_years[1:]):
        if y1 <= t <= y2:
            r1, r2 = spot_rates[y1], spot_rates[y2]
            weight = (t - y1) / (y2 - y1)
            return r1 + weight * (r2 - r1)


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
