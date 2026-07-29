"""
=================================================
Project Phoenix
Unit Test
Paper Trading Adapter
M40.6
=================================================
"""

from trading_system.paper_trading_adapter import (
    PaperTradingAdapter,
)

from trading_system.trading_context import (
    TradingContext,
)


class DummyPaperEngine:
    """
    Dummy Paper Trading Engine.
    """

    def execute(
        self,
        signal,
        symbol,
        quantity,
    ):

        return {
            "paper_order_id": "PAPER-001",
            "status": "FILLED",
            "signal": signal,
            "symbol": symbol,
            "quantity": quantity,
        }


def test_paper_trading_adapter():

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    context.signal = "BUY"

    context.quantity = 1.0

    adapter = PaperTradingAdapter(

        DummyPaperEngine(),

    )

    context = adapter.execute(

        context,

    )

    assert context.paper_trade["status"] == "FILLED"

    assert context.paper_trade["paper_order_id"] == "PAPER-001"

    print("\nPaper Trading Adapter Test Passed")


if __name__ == "__main__":

    test_paper_trading_adapter()