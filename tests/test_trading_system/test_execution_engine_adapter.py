"""
=================================================
Project Phoenix
Test Execution Engine Adapter
M40.5
=================================================
"""

from trading_system.execution_engine_adapter import (
    ExecutionEngineAdapter,
)

from trading_system.trading_context import (
    TradingContext,
)


class DummyExecutionEngine:

    def execute(
        self,
        signal: str,
        quantity: float,
    ):

        return {

            "order_id": "ORD-1001",

            "execution_price": 2365.50,

        }


def test_execution_engine_adapter():

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    context.signal = "BUY"

    context.quantity = 0.50

    adapter = ExecutionEngineAdapter(

        DummyExecutionEngine(),

    )

    context = adapter.execute(

        context,

    )

    assert context.order_id == "ORD-1001"

    assert context.execution_price == 2365.50

    print()

    print("Execution Engine Adapter Test Passed")