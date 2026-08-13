class BenchmarkBond:
    def __init__(self,
                 market_price: float,
                 maturity: int,
                 coupon_rate: float,
                 face_value: float):
        self.market_price = market_price
        self.maturity = maturity
        self.coupon_rate = coupon_rate
        self.face_value = face_value

    def cashflows(self):
        cashflows = []
        for year in range(1, self.maturity + 1):
            cash = self.coupon_rate * self.face_value
            if year == self.maturity:
                cash += self.face_value
            cashflows.append((year, cash))

        return cashflows

def bootstrap_discount_factors(bonds):
    """
    Bootstrap zero-coupon discount factors.

    Assumes `bonds` contains exactly one bond per integer maturity year,
    covering every year from 1 up to the longest maturity (no gaps).

    Returns:
        {
            maturity: discount_factor
        }
    """
    discount_factors = {}
    for bond in sorted(bonds, key=lambda x: x.maturity):

        if bond.maturity in discount_factors:
            raise ValueError(
                f"Duplicate bond maturity {bond.maturity}: only one bond per "
                "maturity year is supported."
            )

        price = bond.market_price
        cashflows = bond.cashflows()

        for year, cashflow in cashflows:
            # subtract the pv of earlier cashflows
            if year < bond.maturity:
                if year not in discount_factors:
                    raise ValueError(
                        f"Missing discount factor for year {year}: bootstrapping "
                        f"requires a bond at every maturity year up to {bond.maturity}."
                    )
                price -= cashflow * discount_factors[year]

        final_cashflow = cashflows[-1][1]
        discount_factors[bond.maturity] = price / final_cashflow

    return discount_factors


def discount_factors_to_spot_rates(discount_factors):
    """
    input : takes a dict of year key and value as discount factor
    output: spits out  a dictionary of year as key value as rate
    """
    spot_rates = {}
    for year, df in discount_factors.items():
        spot_rates[year] = df ** (-1 / year) - 1

    return spot_rates


if __name__ == "__main__":
    # Sample par-ish benchmark curve, one bond per year from 1y to 10y.
    # Coupons/prices are illustrative, not real market quotes.
    sample_data = [
        (1, 97.50, 0.0250),
        (2, 96.00, 0.0275),
        (3, 95.00, 0.0300),
        (4, 94.25, 0.0320),
        (5, 93.75, 0.0335),
        (6, 93.50, 0.0350),
        (7, 93.50, 0.0360),
        (8, 93.75, 0.0370),
        (9, 94.25, 0.0378),
        (10, 95.00, 0.0385),
    ]

    benchmark_bonds = [
        BenchmarkBond(market_price=price, maturity=maturity, coupon_rate=coupon, face_value=100)
        for maturity, price, coupon in sample_data
    ]

    discount_factors = bootstrap_discount_factors(benchmark_bonds)
    spot_rates = discount_factors_to_spot_rates(discount_factors)

    print(f"{'Year':>4}  {'Discount Factor':>16}  {'Spot Rate':>10}")
    for year in sorted(spot_rates):
        print(f"{year:>4}  {discount_factors[year]:>16.6f}  {spot_rates[year]:>9.4%}")


        
