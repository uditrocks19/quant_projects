from implied_volatility_solver import IVSolver
import matplotlib.pyplot as plt


S = 100
T = 1
r = 0.05

quotes = [
    {"strike": 80, "market_price": 24.50},
    {"strike": 90, "market_price": 15.20},
    {"strike": 100, "market_price": 10.45},
    {"strike": 110, "market_price": 7.20},
    {"strike": 120, "market_price": 5.10},
]

solver = IVSolver()

strikes = []
implied_vols = []

for quote in quotes:

    iv = solver.solve(
        S=S,
        K=quote["strike"],
        T=T,
        r=r,
        market_price=quote["market_price"]
    )

    strikes.append(quote["strike"])
    implied_vols.append(iv)

    print(
        f"Strike: {quote['strike']}, "
        f"IV: {iv:.2%}"
    )


plt.plot(strikes, implied_vols, marker="o")

plt.xlabel("Strike Price")
plt.ylabel("Implied Volatility")
plt.title("Volatility Smile")

plt.show()