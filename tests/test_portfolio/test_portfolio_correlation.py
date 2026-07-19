"""
Project Phoenix

Unit Test
Portfolio Correlation
"""

from portfolio.portfolio_correlation import (
    PortfolioCorrelation,
)

from portfolio.portfolio_models import (
    PortfolioContext,
    PositionInfo,
    PositionDirection,
)


def test_portfolio_correlation():

    positions = [

        PositionInfo(
            symbol="RELIANCE",
            direction=PositionDirection.BUY,
            volume=100.0,
            entry_price=2500.0,
            current_price=2510.0,
            floating_profit=100.0,
        ),

        PositionInfo(
            symbol="TCS",
            direction=PositionDirection.SELL,
            volume=100.0,
            entry_price=3500.0,
            current_price=3490.0,
            floating_profit=100.0,
        ),

    ]

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=100200.0,
        positions=positions,
    )

    correlation = PortfolioCorrelation()

    value = correlation.calculate(context)

    assert value == 50.0

    print("===== Portfolio Correlation =====")
    print(f"Correlation Risk : {value}")
    print()
    print("Portfolio Correlation Test Passed")


def test_portfolio_correlation_duplicate_exposure():

    positions = [

        PositionInfo(
            symbol="XAUUSD",
            direction=PositionDirection.BUY,
            volume=0.5,
            entry_price=3350.0,
            current_price=3360.0,
            floating_profit=50.0,
        ),

        PositionInfo(
            symbol="XAUUSD",
            direction=PositionDirection.BUY,
            volume=0.3,
            entry_price=3355.0,
            current_price=3360.0,
            floating_profit=15.0,
        ),

    ]

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=100065.0,
        positions=positions,
    )

    correlation = PortfolioCorrelation()

    value = correlation.calculate(context)

    assert value == 100.0

    print("===== Portfolio Correlation (Duplicate) =====")
    print(f"Correlation Risk : {value}")
    print()
    print("Portfolio Correlation Duplicate Test Passed")


if __name__ == "__main__":

    test_portfolio_correlation()
    test_portfolio_correlation_duplicate_exposure()