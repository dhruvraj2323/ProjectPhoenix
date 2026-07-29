"""
=================================================
Project Phoenix
Unit Test
Strategy Engine Adapter
=================================================
"""

from trading_system.trading_context import (
    TradingContext,
)

from trading_system.strategy_engine_adapter import (
    StrategyEngineAdapter,
)


class DummyStrategy:

    def execute(
        self,
        candles,
        indicators,
        patterns,
    ):

        return {

            "strategy_name": "Phoenix Strategy",

            "signal": "BUY",

            "signal_strength": 92.5,

        }


def test_strategy_engine_adapter():

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    context.candles = [1, 2, 3]

    context.indicators = {

        "EMA": 100,

    }

    context.patterns = {

        "ENGULFING": True,

    }

    adapter = StrategyEngineAdapter(

        DummyStrategy(),

    )

    context = adapter.execute(

        context,

    )

    print("\n===== Strategy Adapter =====")

    print(context.strategy_name)

    print(context.signal)

    print(context.signal_strength)

    assert context.strategy_name == "Phoenix Strategy"

    assert context.signal == "BUY"

    assert context.signal_strength == 92.5

    print("\nStrategy Engine Adapter Test Passed")


if __name__ == "__main__":

    test_strategy_engine_adapter()