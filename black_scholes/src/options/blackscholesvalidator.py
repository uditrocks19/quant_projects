import math
from .blackscholes import BlackScholes


class OptionPriceValidator(BlackScholes):

    def __init__(self, S, K, r, sigma, T):
        super().__init__(S, K, r, sigma, T)

    def call_put_parity(self, tolerance=1e-8):
        call = self.call_price()
        put = self.put_price()

        lhs = call - put
        rhs = self.S - self.K * math.exp(-self.r * self.T)

        return abs(lhs - rhs) < tolerance