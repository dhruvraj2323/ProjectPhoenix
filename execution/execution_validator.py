"""
Project Phoenix
Milestone M10 - Execution Rules Engine

Module:
    execution_validator.py

Purpose:
    Validates an OrderRequest before execution.
"""

from __future__ import annotations

from dataclasses import dataclass

from execution.execution_models import OrderRequest


@dataclass
class ExecutionValidationResult:
    """
    Result returned by the execution validator.
    """

    valid: bool

    reason: str = ""


class ExecutionValidator:
    """
    Validates execution requests.
    """

    def validate(
        self,
        order: OrderRequest,
    ) -> ExecutionValidationResult:
        """
        Validate an OrderRequest.
        """

        if order.volume <= 0:
            return ExecutionValidationResult(
                valid=False,
                reason="Volume must be greater than zero.",
            )

        if order.stop_loss <= 0:
            return ExecutionValidationResult(
                valid=False,
                reason="Invalid stop-loss.",
            )

        if order.take_profit <= 0:
            return ExecutionValidationResult(
                valid=False,
                reason="Invalid take-profit.",
            )

        if not order.symbol:
            return ExecutionValidationResult(
                valid=False,
                reason="Symbol is required.",
            )

        return ExecutionValidationResult(
            valid=True,
            reason="Execution validation passed.",
        )