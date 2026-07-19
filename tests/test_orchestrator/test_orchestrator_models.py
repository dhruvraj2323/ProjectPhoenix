"""
Project Phoenix

Unit Test
Trading Orchestrator Models
"""

from orchestrator.orchestrator_models import (
    ExecutionMetadata,
    OrchestratorStatus,
    TradingContext,
    TradingDecision,
    TradingResult,
    TradingStage,
)


def test_orchestrator_models():

    stage = TradingStage(
        name="Signal",
        completed=True,
        reason="Passed",
    )

    metadata = ExecutionMetadata(
        execution_time_ms=25.8,
        completed_stages=1,
    )

    context = TradingContext(
        symbol="RELIANCE",
        timeframe="15m",
    )

    result = TradingResult(
        stages=[stage],
        metadata=metadata,
    )

    decision = TradingDecision(
        status=OrchestratorStatus.APPROVED,
        approved=True,
        result=result,
        reason="Pipeline completed.",
    )

    assert context.symbol == "RELIANCE"

    assert stage.completed is True

    assert metadata.completed_stages == 1

    assert decision.approved is True

    print("Trading Orchestrator Models Test Passed")


if __name__ == "__main__":

    test_orchestrator_models()