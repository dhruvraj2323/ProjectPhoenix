"""
=================================================
Project Phoenix
Pipeline Manager
M31
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_executor import PipelineExecutor
from market_pipeline.pipeline_validator import PipelineValidator


class PipelineManager:
    """
    High-level manager responsible for executing
    the complete Project Phoenix Market Pipeline.
    """

    def __init__(self) -> None:

        self.validator = PipelineValidator()
        self.executor = PipelineExecutor()

    # ---------------------------------------------------------

    def run(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Run complete pipeline.
        """

        self.validator.validate(context)

        context = self.executor.execute(context)

        return context