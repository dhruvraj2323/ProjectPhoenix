"""
=================================================
Project Phoenix
Test Orchestrator Models
M39
=================================================
"""

from orchestrator_engine.orchestrator_engine_models import (
    EngineHealth,
    OrchestratorResult,
    OrchestratorStatus,
    PipelineStage,
)


def test_orchestrator_models():

    status = OrchestratorStatus()

    assert status.running is False

    assert status.current_stage == ""

    assert status.completed_stages == 0

    assert status.total_stages == 0

    result = OrchestratorResult()

    assert result.approved is False

    assert result.status == "PENDING"

    assert result.reason == ""

    stage = PipelineStage(
        name="Strategy Engine",
    )

    assert stage.name == "Strategy Engine"

    assert stage.completed is False

    assert stage.success is False

    engine = EngineHealth(
        engine_name="Execution Engine",
    )

    assert engine.engine_name == "Execution Engine"

    assert engine.ready is False

    assert engine.running is False

    assert engine.failed is False