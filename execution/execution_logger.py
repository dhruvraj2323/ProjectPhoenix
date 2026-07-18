"""
Project Phoenix
Milestone M10 - Execution Rules Engine

Module:
    execution_logger.py

Purpose:
    Logs execution decisions.
"""

from __future__ import annotations

from execution.execution_models import ExecutionDecision


class ExecutionLogger:
    """
    Logs execution decisions.
    """

    def log(
        self,
        decision: ExecutionDecision,
    ) -> None:
        """
        Log an execution decision.
        """

        print("===== Execution Decision =====")
        print(f"Symbol      : {decision.order.symbol}")
        print(f"Side        : {decision.order.side.value}")
        print(f"Order Type  : {decision.order.order_type.value}")
        print(f"Volume      : {decision.order.volume}")
        print(f"Status      : {decision.status.value}")
        print(f"Approved    : {decision.approved}")
        print(f"Reason      : {decision.reason}")