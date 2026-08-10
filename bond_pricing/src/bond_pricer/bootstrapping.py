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

    Returns:
        {
            maturity: discount_factor
        }
    """

     


        
