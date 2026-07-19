"""
Project Phoenix

Unit Test
Trading Orchestrator Pipeline
"""

from orchestrator.orchestrator_pipeline import (
    OrchestratorPipeline,
)


def test_orchestrator_pipeline():

    pipeline = OrchestratorPipeline()

    result = pipeline.execute()

    print("===== Trading Pipeline =====")

    for stage in result.stages:

        print(
            f"{stage.name:<12}: "
            f"{'PASS' if stage.completed else 'FAIL'}"
        )

    print(
        f"\nCompleted Stages : "
        f"{result.metadata.completed_stages}"
    )

    print(
        f"Execution Time   : "
        f"{result.metadata.execution_time_ms:.3f} ms"
    )

    assert result.metadata.completed_stages == 7

    assert len(result.stages) == 7

    print("\nTrading Pipeline Test Passed")


if __name__ == "__main__":

    test_orchestrator_pipeline()