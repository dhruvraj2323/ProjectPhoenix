"""
=================================================
Project Phoenix
Integration Pipeline Test
=================================================
"""

from integration.integration_pipeline import (
    IntegrationPipeline,
)


def run_test():

    pipeline = IntegrationPipeline()

    pipeline.build_pipeline()

    print("===== Integration Pipeline =====")

    for stage in pipeline.get_pipeline():

        status = "PASS" if stage.completed else "FAIL"

        print(f"{stage.name:<22}: {status}")

    print()

    print(
        f"Completed Stages : {pipeline.completed_stages()}"
    )

    print(
        f"Failed Stages    : {pipeline.failed_stages()}"
    )

    print(
        f"Pipeline Status  : {'APPROVED' if pipeline.pipeline_completed() else 'FAILED'}"
    )

    assert pipeline.completed_stages() == 16

    assert pipeline.failed_stages() == 0

    assert pipeline.pipeline_completed()

    print()

    print("Integration Pipeline Test Passed")


if __name__ == "__main__":

    run_test()