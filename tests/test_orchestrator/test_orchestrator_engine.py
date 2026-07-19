"""
Project Phoenix

Unit Test
Trading Orchestrator Engine
"""

from orchestrator.orchestrator_engine import (
    OrchestratorEngine,
)


def test_orchestrator_engine():

    engine = OrchestratorEngine()

    decision = engine.execute()

    print("\n===== Trading Orchestrator =====")

    print(
        f"Status   : {decision.status.value}"
    )

    print(
        f"Approved : {decision.approved}"
    )

    print(
        f"Reason   : {decision.reason}"
    )

    assert decision.approved is True

    print("\nTrading Orchestrator Engine Test Passed")


if __name__ == "__main__":

    test_orchestrator_engine()