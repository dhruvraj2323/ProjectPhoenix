"""
=================================================
Project Phoenix
Deployment Bootstrap
M61.7.2 - Deployment Approval Integration
=================================================
"""

from __future__ import annotations

from deployment.deployment_engine import (
    DeploymentEngine,
)


class Bootstrap:
    """
    Initializes and shuts down
    Project Phoenix.

    M61.7.2 responsibilities:
    - Delegate deployment initialization
      to DeploymentEngine
    - Respect DeploymentResult.approved
    - Block startup when deployment is rejected
    - Shutdown only an approved deployment
    """

    def __init__(
        self,
        deployment_engine: DeploymentEngine | None = None,
    ) -> None:

        self.deployment_engine = (
            deployment_engine
            if deployment_engine is not None
            else DeploymentEngine()
        )

        self.started = False

        self.deployment_result = None

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def start(
        self,
    ) -> bool:
        """
        Initialize Project Phoenix deployment.

        Returns True only when the deployment
        is approved.
        """

        print()

        print(
            "Initializing Project Phoenix...",
        )

        result = (
            self.deployment_engine.initialize()
        )

        self.deployment_result = result

        self.started = bool(
            result.approved
        )

        if self.started:

            print()

            print(
                "Project Phoenix initialized.",
            )

        else:

            print()

            print(
                "Project Phoenix startup blocked.",
            )

            print(
                f"Reason: {result.reason}"
            )

        return self.started

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> bool:
        """
        Shutdown Project Phoenix.

        Returns False when the deployment
        was never successfully started.
        """

        if not self.started:

            return False

        self.deployment_engine.shutdown()

        self.started = False

        print()

        print(
            "Project Phoenix stopped.",
        )

        return True