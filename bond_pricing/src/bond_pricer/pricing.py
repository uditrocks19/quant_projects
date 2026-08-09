def price_bond(
        cashflows,
        settelement_date,
        discount_rate,
        frequency=1
):
    """
    Calculate the present value of a bond's future cash flows.

    cashflows:
        List of (date, amount)

    settlement_date:
        Date on which we are valuing the bond

    discount_rate:
        Annual discount rate, e.g. 0.05 for 5%
    
    frequency:
        semiannual/annual/monthly
    """
    price = 0.0

    for payment_date, amount in cashflows:

        t = (payment_date - settelement_date).days
        t = t / 365.0

        # present value of this cashflow
        pv = (amount) / (1 + discount_rate / frequency) ** (t * frequency)
        price += pv

    return price
