"""
Project Phoenix
Milestone M10 - Execution Rules Engine

Module:
    execution_engine.py

Purpose:
    Coordinates the complete execution workflow.
"""

from __future__ import annotations

from execution.execution_logger import ExecutionLogger
from execution.execution_models import (
    ExecutionDecision,
    ExecutionStatus,
)
from execution.execution_rules import ExecutionRules
from execution.execution_validator import ExecutionValidator
from risk.risk_models import RiskDecision


class ExecutionEngine:
    """
    Main Execution Rules Engine.
    """

    def __init__(self) -> None:
        self._rules = ExecutionRules()
        self._validator = ExecutionValidator()
        self._logger = ExecutionLogger()

    def execute(
        self,
        decision: RiskDecision,
    ) -> ExecutionDecision:
        """
        Execute the complete M10 workflow.
        """

        order = self._rules.create_order(decision)

        validation = self._validator.validate(order)

        execution = ExecutionDecision(
            status=(
                ExecutionStatus.READY
                if validation.valid
                else ExecutionStatus.REJECTED
            ),
            order=order,
            approved=validation.valid,
            reason=validation.reason,
        )

        self._logger.log(execution)

        return execution