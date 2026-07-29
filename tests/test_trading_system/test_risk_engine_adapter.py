"""
=================================================
Project Phoenix
Unit Test
Risk Engine Adapter
=================================================
"""

from trading_system.trading_context import (
    TradingContext,
)

from trading_system.risk_engine_adapter import (
    RiskEngineAdapter,
)


class DummyRisk:

    def execute(
        self,
        signal,
        signal_strength,
        symbol,
        timeframe,
    ):

        return {

            "risk_score": 18.5,

            "risk_passed": True,

        }


def test_risk_engine_adapter():

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    context.signal = "BUY"

    context.signal_strength = 92.5

    adapter = RiskEngineAdapter(

        DummyRisk(),

    )

    context = adapter.execute(

        context,

    )

    print("\n===== Risk Adapter =====")

    print(context.risk_score)

    print(context.risk_passed)

    assert context.risk_score == 18.5

    assert context.risk_passed is True

    print("\nRisk Engine Adapter Test Passed")


if __name__ == "__main__":

    test_risk_engine_adapter()