"""
Project Phoenix
Milestone M18 - Configuration & Settings Engine

Module:
    config_logger.py

Purpose:
    Logs Configuration Engine decisions.
"""

from __future__ import annotations

from config.config_models import (
    ConfigurationContext,
    ConfigurationDecision,
)


class ConfigurationLogger:
    """
    Logs configuration decisions.
    """

    def log(
        self,
        context: ConfigurationContext,
        decision: ConfigurationDecision,
    ) -> None:
        """
        Log configuration result.
        """

        print("===== Configuration =====")

        print(
            f"Status          : "
            f"{decision.status.value}"
        )

        print(
            f"Environment     : "
            f"{context.environment}"
        )

        print(
            f"Version         : "
            f"{context.version}"
        )

        print(
            f"Items Loaded    : "
            f"{len(decision.items)}"
        )

        print(
            f"Approved        : "
            f"{decision.approved}"
        )

        print(
            f"Reason          : "
            f"{decision.reason}"
        )