import math

class BlackScholes:
    def __init__(self, S, K, T, r, sigma):
        self.S = S # spot price
        self.K = K # strike price
        self.T = T # expiry time
        self.r = r # risk free rate
        self.sigma = sigma # volatility


    @staticmethod

    def normal_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    def d1(self):
        return (

            math.log(self.S / self.K) +
            (self.r  + 0.5 * self.sigma ** 2) * self.T
        ) / (self.sigma * math.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * math.sqrt(self.T)

    def call_price(self):
        d1 = self.d1()
        d2 = self.d2()

        return (
            self.S * self.normal_cdf(d1) -
            self.K * math.exp(-self.r * self.T) * \
            self.normal_cdf(d2)
        )

    def put_price(self):
        d1 = self.d1()
        d2 = self.d2()

        return (
            self.K * math.exp(-self.r * self.T)
            * self.normal_cdf(-d2)
            - self.S * self.normal_cdf(-d1)
        )

    def call_put_parity(self):
        """
        diff between call and put pricr

        """
        return (
            self.S - self.K * math.exp(-self.r * self.T)
        )

    def delta_call(self):
        return (
         self.normal_cdf(self.d1())
        )

    def delta_put(self):
        return self.delta_call() - 1

    def gamma(self):
        d1 = self.d1()

        return (
            math.exp(-d1 * d1 / 2)
            / (
                self.S
                * self.sigma
                * math.sqrt(2 * math.pi * self.T)
            )
        )

    def vega(self):
        d1 = self.d1()
        return (
            self.S * math.sqrt(self.T) * math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)
        )

    def theta(self):
        d1 = self.d1()
        d2 = self.d2()

        phi_d1 = math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)

        return (
            -self.S * phi_d1 * self.sigma / (2 * math.sqrt(self.T))
            - self.r * self.K * math.exp(-self.r * self.T) * self.normal_cdf(d2)
        )