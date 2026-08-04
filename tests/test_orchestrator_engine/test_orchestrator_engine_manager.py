"""
=================================================
Project Phoenix
Test Orchestrator Engine Manager
M56
=================================================
"""

from orchestrator_engine.orchestrator_engine_manager import (
    OrchestratorEngineManager,
)


def test_orchestrator_engine_manager():

    manager = (
        OrchestratorEngineManager()
    )

    result = manager.execute()

    assert result.approved

    assert result.status == "SUCCESS"

    assert (
        result.reason
        == "Pipeline executed successfully."
    )