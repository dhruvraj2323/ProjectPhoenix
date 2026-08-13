"""
=================================================
Project Phoenix
Deployment Engine
M61.7.1 - Deployment Approval Gate
=================================================

Master deployment controller.
"""

from deployment.runtime_manager import RuntimeManager
from deployment.health_monitor import HealthMonitor
from deployment.deployment_logger import DeploymentLogger
from deployment.deployment_models import (
    DeploymentStatus,
    DeploymentResult,
)


class DeploymentEngine:
    """
    Master Deployment Controller.

    M61.7.1 responsibilities:
    - Start runtime through RuntimeManager
    - Evaluate deployment health
    - Approve deployment only when runtime
      startup and health checks both succeed
    - Reject unsafe deployment states
    """

    def __init__(self):

        self.runtime = RuntimeManager()

        self.monitor = HealthMonitor()

    # --------------------------------------------------
    # Initialize
    # --------------------------------------------------

    def initialize(
        self,
    ) -> DeploymentResult:
        """
        Initialize the deployment.

        Deployment is approved only when:

        1. Runtime starts successfully
        2. Health report is healthy
        """

        runtime_started = (
            self.runtime.start()
        )

        report = (
            self.monitor.health_report()
        )

        runtime_running = (
            self.runtime.status()
        )

        healthy = (
            report["healthy"]
        )

        approved = (
            runtime_started
            and runtime_running
            and healthy
        )

        # --------------------------------------------------
        # Approval Reason
        # --------------------------------------------------

        if approved:

            reason = (
                "Deployment initialized "
                "successfully."
            )

        elif not runtime_started:

            reason = (
                "Deployment rejected: "
                "runtime startup failed."
            )

        elif not runtime_running:

            reason = (
                "Deployment rejected: "
                "runtime is not running."
            )

        else:

            reason = (
                "Deployment rejected: "
                "health check failed."
            )

        # --------------------------------------------------
        # Deployment Status
        # --------------------------------------------------

        status = DeploymentStatus(
            running=runtime_running,
            healthy=healthy,
            version="1.0",
            environment="Production",
        )

        # --------------------------------------------------
        # Deployment Result
        # --------------------------------------------------

        result = DeploymentResult(
            approved=approved,
            reason=reason,
            status=status,
            health_report=report,
        )

        DeploymentLogger.log(
            result
        )

        return result

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    def shutdown(
        self,
    ) -> bool:
        """
        Shutdown Deployment Engine.
        """

        self.runtime.stop()

        return True