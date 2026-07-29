"""
=================================================
Project Phoenix
Test Orchestrator Engine
M39
=================================================
"""

from orchestrator_engine.orchestrator_engine import (
    OrchestratorEngine,
)


def test_orchestrator_engine():

    engine = OrchestratorEngine()

    result = engine.run()

    assert result.approved is True

    assert result.status == "SUCCESS"

    assert result.reason == "Pipeline executed successfully."