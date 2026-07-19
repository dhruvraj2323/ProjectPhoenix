"""
Project Phoenix

Unit Test
Trading Orchestrator Validator
"""

from orchestrator.orchestrator_pipeline import (
    OrchestratorPipeline,
)

from orchestrator.orchestrator_validator import (
    OrchestratorValidator,
)


def test_orchestrator_validator():

    pipeline = OrchestratorPipeline()

    result = pipeline.execute()

    validator = OrchestratorValidator()

    validation = validator.validate(
        result
    )

    print("===== Pipeline Validator =====")

    print(
        f"Valid  : {validation.valid}"
    )

    print(
        f"Reason : {validation.reason}"
    )

    assert validation.valid is True

    print("\nPipeline Validator Test Passed")


if __name__ == "__main__":

    test_orchestrator_validator()