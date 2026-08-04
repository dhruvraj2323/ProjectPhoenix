"""
=================================================
Project Phoenix
Pipeline Runner Test
M58
=================================================
"""

from deployment.pipeline_runner import (
    PipelineRunner,
)


def test_pipeline_runner():

    runner = PipelineRunner()

    assert runner.execute() is True