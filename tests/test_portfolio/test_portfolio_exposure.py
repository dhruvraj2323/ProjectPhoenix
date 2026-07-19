"""
Project Phoenix

Unit Test
Portfolio Exposure
"""

from portfolio.portfolio_exposure import (
    PortfolioExposure,
)

from portfolio.portfolio_models import (
    PortfolioContext,
    PositionInfo,
    PositionDirection,
)


def test_portfolio_exposure():

    positions = [

        PositionInfo(
            symbol="RELIANCE",
            direction=PositionDirection.BUY,
            volume=100.0,
            entry_price=2500.0,
            current_price=2520.0,
            floating_profit=200.0,
        ),

        PositionInfo(
            symbol="TCS",
            direction=PositionDirection.SELL,
            volume=40.0,
            entry_price=3500.0,
            current_price=3480.0,
            floating_profit=80.0,
        ),

        PositionInfo(
            symbol="RELIANCE",
            direction=PositionDirection.BUY,
            volume=60.0,
            entry_price=2530.0,
            current_price=2545.0,
            floating_profit=90.0,
        ),

    ]

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=100370.0,
        positions=positions,
    )

    exposure = PortfolioExposure()

    result = exposure.calculate(context)

    print("===== Portfolio Exposure =====")
    print(f"Gross Exposure : {result.gross_exposure}")
    print(f"Net Exposure   : {result.net_exposure}")
    print(f"Long Exposure  : {result.long_exposure}")
    print(f"Short Exposure : {result.short_exposure}")
    print(f"Symbol Exposure: {result.symbol_exposure}")

    assert result.gross_exposure == 200.0
    assert result.net_exposure == 120.0
    assert result.long_exposure == 160.0
    assert result.short_exposure == 40.0
    assert result.symbol_exposure["RELIANCE"] == 160.0
    assert result.symbol_exposure["TCS"] == 40.0

    print("\nPortfolio Exposure Test Passed")


if __name__ == "__main__":

    test_portfolio_exposure()