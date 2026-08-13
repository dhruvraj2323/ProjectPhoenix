"""
=================================================
Project Phoenix
Deployment Engine
M61.10.3 - Runtime Protection Observability
=================================================

Master deployment controller.
"""

from deployment.runtime_manager import (
    RuntimeManager,
)

from deployment.health_monitor import (
    HealthMonitor,
)

from deployment.deployment_logger import (
    DeploymentLogger,
)

from deployment.deployment_models import (
    DeploymentStatus,
    DeploymentResult,
)

from deployment.deployment_health import (
    DeploymentHealthState,
    health_state_from_report,
)


class DeploymentEngine:
    """
    Master Deployment Controller.

    M61.10.3 responsibilities:
    - Start runtime through RuntimeManager
    - Evaluate deployment health
    - Evaluate runtime trading protection state
    - Approve deployment only when runtime
      startup and health checks both succeed
    - Reject unsafe deployment states
    - Stop runtime when post-startup health
      validation fails
    - Expose protection state in DeploymentResult
    """

    def __init__(self):

        self.runtime = RuntimeManager()

        self.monitor = HealthMonitor()

    # --------------------------------------------------
    # Health State
    # --------------------------------------------------

    def health_state(
        self,
    ) -> DeploymentHealthState:
        """
        Return the current deployment health state.
        """

        report = (
            self.monitor.health_report()
        )

        return (
            health_state_from_report(
                report,
            )
        )

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
        2. Runtime is running
        3. Health report is healthy

        Runtime trading protection state is captured
        in the deployment result.

        If runtime starts but the post-startup
        health check fails, the runtime is stopped
        before the deployment is rejected.
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

        health_state = (
            health_state_from_report(
                report,
            )
        )

        healthy = (
            health_state
            == DeploymentHealthState.HEALTHY
        )

        trading_protection_state = (
            self.runtime.trading_protection_state()
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
            # M61.9.5 Health Failure Protection
            # --------------------------------------------------

            self.runtime.stop()

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
            health_state=health_state,
            trading_protection_state=(
                trading_protection_state
            ),
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