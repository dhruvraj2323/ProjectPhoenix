"""
=================================================
Project Phoenix
Execution Engine
M37
=================================================
"""

from __future__ import annotations

from execution_engine.execution_context import (
    ExecutionContext,
)
from execution_engine.execution_logger import (
    ExecutionLogger,
)
from execution_engine.execution_processor import (
    ExecutionProcessor,
)
from execution_engine.execution_validator import (
    ExecutionValidator,
)


class ExecutionEngine:
    """
    Main execution pipeline.
    """

    def __init__(
        self,
    ) -> None:

        self.processor = ExecutionProcessor()

        self.validator = ExecutionValidator()

        self.logger = ExecutionLogger()

    def run(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:

        self.logger.log_start(
            context,
        )

        if not self.validator.validate(
            context,
        ):

            self.logger.log_failure(
                context,
            )

            return context

        context = self.processor.process(
            context,
        )

        self.logger.log_finish(
            context,
        )

        return context