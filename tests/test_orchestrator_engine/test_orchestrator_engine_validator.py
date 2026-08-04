"""
=================================================
Project Phoenix
Test Orchestrator Engine Validator
M56
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

    # -----------------------------
    # Valid Result
    # -----------------------------

    result = OrchestratorResult()

    assert validator.validate(result)

    # -----------------------------
    # Already Approved
    # -----------------------------

    approved = OrchestratorResult()

    approved.approved = True

    assert not validator.validate(approved)

    # -----------------------------
    # Invalid Status
    # -----------------------------

    invalid = OrchestratorResult()

    invalid.status = "SUCCESS"

    assert not validator.validate(invalid)