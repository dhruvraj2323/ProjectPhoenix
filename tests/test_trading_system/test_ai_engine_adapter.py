"""
=================================================
Project Phoenix
Unit Test
AI Engine Adapter
=================================================
"""

from trading_system.ai_engine_adapter import (
    AIEngineAdapter,
)

from trading_system.trading_context import (
    TradingContext,
)


class DummyAIEngine:

    def execute(
        self,
        signal,
        signal_strength,
        risk_score,
    ):

        return {

            "ai_score": 91.5,

            "ai_confidence": 97.2,

            "ai_decision": "APPROVED",

        }


def test_ai_engine_adapter():

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    context.signal = "BUY"

    context.signal_strength = 88.0

    context.risk_score = 12.5

    adapter = AIEngineAdapter(

        DummyAIEngine(),

    )

    context = adapter.execute(

        context,

    )

    assert context.ai_score == 91.5

    assert context.ai_confidence == 97.2

    assert context.ai_decision == "APPROVED"