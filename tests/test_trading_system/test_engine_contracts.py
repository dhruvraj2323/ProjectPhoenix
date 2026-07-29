"""
=================================================
Project Phoenix
Engine Contracts Test
=================================================
"""

from trading_system.engine_contracts import (
    StrategyEngineContract,
)

from trading_system.trading_context import (
    TradingContext,
)


class DummyStrategyEngine(
    StrategyEngineContract,
):
    """
    Dummy implementation used
    for unit testing.
    """

    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:

        context.strategy_name = "Dummy Strategy"

        return context


def test_engine_contracts():

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    engine = DummyStrategyEngine()

    context = engine.execute(
        context,
    )

    assert context.strategy_name == "Dummy Strategy"

    print()

    print("Engine Contracts Test Passed")


if __name__ == "__main__":

    test_engine_contracts()