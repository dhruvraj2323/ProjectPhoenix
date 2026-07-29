"""
=================================================
Project Phoenix
Test Orchestrator Engine Validator
M39
=================================================
"""

from orchestrator_engine.orchestrator_engine_models import (
    OrchestratorResult,
)

from orchestrator_engine.orchestrator_engine_validator import (
    OrchestratorEngineValidator,
)


def test_orchestrator_engine_validator():

    validator = OrchestratorEngineValidator()

    result = OrchestratorResult()

    assert validator.validate(result) is True

    assert validator.validate(None) is False