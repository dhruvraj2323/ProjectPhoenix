"""
Project Phoenix

Unit Test
Trading Orchestrator Logger
"""

from orchestrator.orchestrator_logger import (
    OrchestratorLogger,
)

from orchestrator.orchestrator_models import (
    ExecutionMetadata,
    OrchestratorStatus,
    TradingDecision,
    TradingResult,
    TradingStage,
)


def test_orchestrator_logger():

    stages = [

        TradingStage(
            name="Signal",
            completed=True,
            reason="Completed",
        ),

        TradingStage(
            name="Risk",
            completed=True,
            reason="Completed",
        ),

        TradingStage(
            name="Portfolio",
            completed=True,
            reason="Completed",
        ),

        TradingStage(
            name="Strategy",
            completed=True,
            reason="Completed",
        ),

        TradingStage(
            name="AI",
            completed=True,
            reason="Completed",
        ),

        TradingStage(
            name="Execution",
            completed=True,
            reason="Completed",
        ),

        TradingStage(
            name="Performance",
            completed=True,
            reason="Completed",
        ),

    ]

    metadata = ExecutionMetadata(

        execution_time_ms=2.75,

        completed_stages=7,

    )

    result = TradingResult(

        stages=stages,

        metadata=metadata,

    )

    decision = TradingDecision(

        status=OrchestratorStatus.APPROVED,

        approved=True,

        result=result,

        reason="Pipeline validation passed.",

    )

    logger = OrchestratorLogger()

    logger.log(
        decision
    )

    print("\nTrading Orchestrator Logger Test Passed")


if __name__ == "__main__":

    test_orchestrator_logger()