"""
Project Phoenix

Unit Test
Portfolio Engine
"""

from portfolio.portfolio_engine import PortfolioEngine

from portfolio.portfolio_models import (
    PortfolioContext,
    PositionInfo,
    PositionDirection,
)


def test_portfolio_engine():

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
            entry_price=4000.0,
            current_price=4010.0,
            floating_profit=-100.0,
        ),
    ]

    context = PortfolioContext(

        account_balance=100000.0,

        account_equity=100150.0,

        positions=positions,

    )

    engine = PortfolioEngine()

    decision = engine.evaluate(context)

    print("\n===== Portfolio Engine =====")
    print(f"Decision : {decision.decision.value}")
    print(f"Approved : {decision.approved}")
    print(f"Reason   : {decision.reason}")

    assert decision.approved is True

    print("\nPortfolio Engine Test Passed")


if __name__ == "__main__":

    test_portfolio_engine()