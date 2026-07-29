"""
=================================================
Project Phoenix
Execution Manager
M37
=================================================
"""

from __future__ import annotations

from execution_engine.execution_context import (
    ExecutionContext,
)

from execution_engine.execution_engine import (
    ExecutionEngine,
)


class ExecutionManager:
    """
    High-level interface for Execution Engine.
    """

    def __init__(self) -> None:

        self.engine = ExecutionEngine()

    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:
        """
        Execute the complete
        execution workflow.
        """

        return self.engine.run(
            context,
        )