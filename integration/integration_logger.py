"""
=================================================
Project Phoenix
System Integration Logger
=================================================

Logs the final integration execution report.
"""

from integration.integration_models import (
    IntegrationResult,
)


class IntegrationLogger:
    """
    Logs the complete integration result.
    """

    @staticmethod
    def log(result: IntegrationResult) -> None:

        print("===== System Integration =====")

        print(f"Status            : {result.status}")
        print(f"Approved          : {result.approved}")

        print()

        print(f"Validation        : {result.validation.valid}")
        print(f"Reason            : {result.validation.reason}")

        print()

        print(f"System Healthy    : {result.health.healthy}")
        print(
            f"Modules Completed : "
            f"{result.health.completed_modules}/{result.health.total_modules}"
        )

        print()

        print(
            f"Completed Stages  : "
            f"{result.summary.completed_stages}"
        )

        print(
            f"Failed Stages     : "
            f"{result.summary.failed_stages}"
        )

        print(
            f"Execution Time    : "
            f"{result.summary.execution_time_ms:.3f} ms"
        )