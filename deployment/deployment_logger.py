"""
=================================================
Project Phoenix
Deployment Logger
M61.10.4 - Trading Protection Observability
=================================================

Logs deployment events.
"""

from deployment.deployment_models import (
    DeploymentResult,
)


class DeploymentLogger:
    """
    Deployment logging.

    M61.10.4 responsibilities:
    - Log deployment approval state
    - Log deployment reason
    - Log runtime state
    - Log health state
    - Log trading protection state
    - Log deployment version
    - Log deployment environment
    """

    @staticmethod
    def log(
        result: DeploymentResult,
    ) -> None:

        print(
            "===== Deployment ====="
        )

        print(
            f"Approved        : "
            f"{result.approved}"
        )

        print(
            f"Reason          : "
            f"{result.reason}"
        )

        print()

        print(
            f"Running         : "
            f"{result.status.running}"
        )

        print(
            f"Healthy         : "
            f"{result.status.healthy}"
        )

        print(
            f"Health State    : "
            f"{result.health_state.value}"
        )

        print(
            f"Protection      : "
            f"{result.trading_protection_state.value}"
        )

        print(
            f"Version         : "
            f"{result.status.version}"
        )

        print(
            f"Environment     : "
            f"{result.status.environment}"
        )