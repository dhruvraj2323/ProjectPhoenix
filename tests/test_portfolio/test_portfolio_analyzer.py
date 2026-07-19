"""
Project Phoenix

Unit Test
Portfolio Analyzer
"""

from portfolio.portfolio_analyzer import PortfolioAnalyzer

from portfolio.portfolio_models import (
    PortfolioContext,
    PositionInfo,
    PositionDirection,
)


def test_portfolio_analyzer():

    positions = [

        PositionInfo(
            symbol="RELIANCE",
            direction=PositionDirection.BUY,
            volume=100.0,
            entry_price=2500.0,
            current_price=2525.0,
            floating_profit=250.0,
        ),

        PositionInfo(
            symbol="TCS",
            direction=PositionDirection.SELL,
            volume=50.0,
            entry_price=3800.0,
            current_price=3820.0,
            floating_profit=-100.0,
        ),

    ]

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=100150.0,
        positions=positions,
    )

    analyzer = PortfolioAnalyzer()

    metrics = analyzer.analyze(context)

    print("===== Portfolio Analyzer =====")
    print(f"Balance          : {metrics.balance}")
    print(f"Equity           : {metrics.equity}")
    print(f"Floating Profit  : {metrics.floating_profit}")
    print(f"Floating Loss    : {metrics.floating_loss}")
    print(f"Used Margin      : {metrics.used_margin}")
    print(f"Free Margin      : {metrics.free_margin}")
    print(f"Margin Level     : {metrics.margin_level}")
    print(f"Portfolio Heat   : {metrics.portfolio_heat}")
    print(f"Open Positions   : {metrics.open_positions}")

    assert metrics.balance == 100000.0
    assert metrics.open_positions == 2

    print("\nPortfolio Analyzer Test Passed")


if __name__ == "__main__":

    test_portfolio_analyzer()