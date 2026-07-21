"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Router
=================================================
"""

from market_pipeline.pipeline_models import PipelineStage
from market_pipeline.pipeline_router import PipelineRouter


def test_pipeline_router():

    router = PipelineRouter()

    current = PipelineStage.INITIALIZED

    visited = [current]

    while router.has_next_stage(current):

        current = router.get_next_stage(current)

        visited.append(current)

    expected = [

        PipelineStage.INITIALIZED,

        PipelineStage.MARKET_DATA,

        PipelineStage.INDICATORS,

        PipelineStage.PATTERNS,

        PipelineStage.SIGNAL,

        PipelineStage.RISK,

        PipelineStage.PORTFOLIO,

        PipelineStage.AI,

        PipelineStage.EXECUTION,

        PipelineStage.COMPLETED,

    ]

    assert visited == expected

    assert router.is_final_stage(PipelineStage.COMPLETED)

    assert router.reset() == PipelineStage.INITIALIZED

    print("===== Pipeline Router =====")

    for index, stage in enumerate(visited, start=1):

        print(f"{index:02d}. {stage.value}")

    print()

    print("Pipeline Router Test Passed")


if __name__ == "__main__":
    test_pipeline_router()