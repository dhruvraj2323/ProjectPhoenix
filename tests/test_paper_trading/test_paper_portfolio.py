"""
=================================================
Project Phoenix
Paper Portfolio Test
=================================================
"""

from paper_trading.paper_portfolio import PaperPortfolioManager


def run_test():

    portfolio = PaperPortfolioManager()

    portfolio.update_floating_profit(25.0)
    portfolio.close_trade(50.0)

    result = portfolio.portfolio()

    print("===== Paper Portfolio =====")

    print(f"Balance           : {result.balance}")
    print(f"Equity            : {result.equity}")
    print(f"Floating Profit   : {result.floating_profit}")
    print(f"Closed Profit     : {result.closed_profit}")

    assert result.balance == 10050.0
    assert result.equity == 10075.0

    print()
    print("Paper Portfolio Test Passed")


if __name__ == "__main__":

    run_test()