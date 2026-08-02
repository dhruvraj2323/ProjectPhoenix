"""
=================================================
Project Phoenix
Live Portfolio Test
=================================================
"""

from live_trading.live_portfolio import LivePortfolioManager


def run_test():

    portfolio = LivePortfolioManager()

    portfolio.update_floating_profit(30.0)
    portfolio.close_trade(75.0)

    result = portfolio.portfolio()

    print("===== Live Portfolio =====")

    print(f"Balance           : {result.balance}")
    print(f"Equity            : {result.equity}")
    print(f"Floating Profit   : {result.floating_profit}")
    print(f"Closed Profit     : {result.closed_profit}")

    assert result.balance == 10075.0
    assert result.equity == 10105.0

    print()
    print("Live Portfolio Test Passed")


if __name__ == "__main__":

    run_test()