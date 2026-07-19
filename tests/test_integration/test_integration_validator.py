"""
=================================================
Project Phoenix
Integration Validator Test
=================================================
"""

from integration.integration_pipeline import (
    IntegrationPipeline,
)

from integration.integration_validator import (
    IntegrationValidator,
)


def run_test():

    pipeline = IntegrationPipeline()

    pipeline.build_pipeline()

    validator = IntegrationValidator(pipeline)

    result = validator.validate()

    print("===== Integration Validator =====")

    print(f"Valid  : {result.valid}")
    print(f"Reason : {result.reason}")

    assert result.valid

    print()

    print("Integration Validator Test Passed")


if __name__ == "__main__":

    run_test()