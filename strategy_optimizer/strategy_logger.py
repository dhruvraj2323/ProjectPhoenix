"""
Project Phoenix
Milestone M13 - Strategy Optimizer Engine

Module:
    strategy_logger.py

Purpose:
    Logs optimization decisions.
"""

from __future__ import annotations

from strategy_optimizer.strategy_models import (
    OptimizationDecision,
)


class StrategyLogger:
    """
    Logs Strategy Optimizer decisions.
    """

    def log(
        self,
        decision: OptimizationDecision,
    ) -> None:
        """
        Log optimization decision.
        """

        print("===== Strategy Optimization =====")
        print(
            f"Status            : {decision.status.value}"
        )
        print(
            f"Approved          : {decision.approved}"
        )
        print(
            f"Reason            : {decision.reason}"
        )
        print(
            f"Optimization Type : "
            f"{decision.recommendation.optimization_type.value}"
        )
        print(
            f"Current Value     : "
            f"{decision.recommendation.current_value}"
        )
        print(
            f"Suggested Value   : "
            f"{decision.recommendation.suggested_value}"
        )
        print(
            f"Confidence        : "
            f"{decision.recommendation.confidence:.2f}"
        )