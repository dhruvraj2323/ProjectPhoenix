"""
=================================================
Project Phoenix
Runtime
M62.3.4.3 - Runtime Status Integration
=================================================
"""

from __future__ import annotations

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.continuous_runner import (
    ContinuousRunner,
)

from deployment.health_monitor import (
    HealthMonitor,
)

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
    RuntimeOperationalStatus,
)

from deployment.runtime_readiness import (
    RuntimeReadinessAdapter,
)

from deployment.runtime_status import (
    RuntimeStatus,
)

from deployment.trading_protection import (
    TradingProtection,
)


class Runtime:
    """
    Project Phoenix runtime controller.

    Responsibilities:
    - Check configuration readiness before startup
    - Check deployment health before startup
    - Block startup when readiness fails
    - Track runtime operational state
    - Expose a structured runtime status snapshot
    - Pass TradingProtection to ContinuousRunner
    - Start ContinuousRunner only when ready
    - Preserve runtime stop behavior

    This class does not:
    - connect to MT5
    - approve live trading
    - execute trades
    """

    def __init__(
        self,
        interval: int = 300,
        trading_protection: (
            TradingProtection | None
        ) = None,
        configuration_readiness: (
            ConfigurationReadinessResult | None
        ) = None,
    ) -> None:

        self.interval = interval

        self.running = False

        self.configuration_readiness = (
            configuration_readiness
        )

        self.health_monitor = (
            HealthMonitor()
        )

        self.trading_protection = (
            trading_protection
            if trading_protection is not None
            else TradingProtection()
        )

        self.continuous_runner = (
            ContinuousRunner(
                interval=interval,
                trading_protection=(
                    self.trading_protection
                ),
            )
        )

        self._operational_status = (
            RuntimeOperationalStatus(
                state=(
                    RuntimeOperationalState.STOPPED
                ),
                reason=(
                    "Runtime has not started."
                ),
            )
        )

    # --------------------------------------------------
    # Configuration Readiness
    # --------------------------------------------------

    def configuration_is_ready(
        self,
    ) -> bool:
        """
        Return True when configuration readiness
        passes the startup gate.

        When no configuration readiness result
        is supplied, preserve the existing runtime
        startup contract.
        """

        if (
            self.configuration_readiness
            is None
        ):
            return True

        readiness = (
            RuntimeReadinessAdapter.evaluate(
                self.configuration_readiness
            )
        )

        return readiness.ready

    # --------------------------------------------------
    # Deployment Health
    # --------------------------------------------------

    def deployment_is_healthy(
        self,
    ) -> bool:
        """
        Return True when deployment health
        passes the startup health gate.
        """

        return (
            self.health_monitor.is_healthy()
        )

    # --------------------------------------------------
    # Readiness Check
    # --------------------------------------------------

    def is_ready(
        self,
    ) -> bool:
        """
        Return True only when both configuration
        readiness and deployment health pass.
        """

        if not self.configuration_is_ready():
            return False

        return self.deployment_is_healthy()

    # --------------------------------------------------
    # Operational State
    # --------------------------------------------------

    def operational_state(
        self,
    ) -> RuntimeOperationalStatus:
        """
        Return the current runtime operational status.
        """

        return self._operational_status

    # --------------------------------------------------
    # Runtime Status
    # --------------------------------------------------

    def status_snapshot(
        self,
    ) -> RuntimeStatus:
        """
        Return an immutable runtime observability
        snapshot.

        The snapshot contains operational readiness,
        deployment health, runtime state, reason,
        and timestamp.

        No credentials, trading decisions,
        live approval, or MT5 connection details
        are exposed.
        """

        return RuntimeStatus(
            operational_state=(
                self._operational_status.state
            ),
            configuration_ready=(
                self.configuration_is_ready()
            ),
            deployment_healthy=(
                self.deployment_is_healthy()
            ),
            runtime_running=(
                self.running
            ),
            reason=(
                self._operational_status.reason
            ),
            timestamp=(
                __import__(
                    "datetime"
                ).datetime.now(
                    __import__(
                        "datetime"
                    ).timezone.utc
                )
            ),
        )

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def start(
        self,
        cycles: int = 1,
    ) -> bool:
        """
        Start Project Phoenix runtime.

        Startup is blocked when:
        1. configuration readiness fails, or
        2. deployment health fails.
        """

        self._operational_status = (
            RuntimeOperationalStatus(
                state=(
                    RuntimeOperationalState.STARTING
                ),
                reason=(
                    "Runtime startup initiated."
                ),
            )
        )

        # ----------------------------------------------
        # Configuration Readiness Gate
        # ----------------------------------------------

        if not self.configuration_is_ready():

            self.running = False

            self._operational_status = (
                RuntimeOperationalStatus(
                    state=(
                        RuntimeOperationalState.FAILED
                    ),
                    reason=(
                        "Runtime startup blocked "
                        "by configuration readiness."
                    ),
                )
            )

            print()

            print(
                "Runtime startup blocked."
            )

            print(
                "Configuration readiness "
                "check failed."
            )

            return False

        # ----------------------------------------------
        # Deployment Health Gate
        # ----------------------------------------------

        if not self.deployment_is_healthy():

            self.running = False

            self._operational_status = (
                RuntimeOperationalStatus(
                    state=(
                        RuntimeOperationalState.FAILED
                    ),
                    reason=(
                        "Runtime startup blocked "
                        "by deployment health."
                    ),
                )
            )

            print()

            print(
                "Runtime startup blocked."
            )

            print(
                "Deployment health check failed."
            )

            return False

        # ----------------------------------------------
        # Runtime Ready
        # ----------------------------------------------

        self._operational_status = (
            RuntimeOperationalStatus(
                state=(
                    RuntimeOperationalState.READY
                ),
                reason=(
                    "Runtime configuration and "
                    "deployment health are ready."
                ),
            )
        )

        self.running = True

        print()

        print(
            "Runtime started."
        )

        # ----------------------------------------------
        # Start Continuous Runner
        # ----------------------------------------------

        try:

            self.continuous_runner.start(
                cycles=cycles,
            )

            self._operational_status = (
                RuntimeOperationalStatus(
                    state=(
                        RuntimeOperationalState.RUNNING
                    ),
                    reason=(
                        "Runtime is operational."
                    ),
                )
            )

            return True

        except Exception as exc:

            print()

            print(
                "Runtime execution failed."
            )

            print(exc)

            self.running = False

            self._operational_status = (
                RuntimeOperationalStatus(
                    state=(
                        RuntimeOperationalState.FAILED
                    ),
                    reason=(
                        "Runtime execution failed."
                    ),
                )
            )

            return False

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> None:
        """
        Stop Project Phoenix runtime.
        """

        self._operational_status = (
            RuntimeOperationalStatus(
                state=(
                    RuntimeOperationalState.STOPPING
                ),
                reason=(
                    "Runtime shutdown initiated."
                ),
            )
        )

        self.running = False

        self.continuous_runner.stop()

        self._operational_status = (
            RuntimeOperationalStatus(
                state=(
                    RuntimeOperationalState.STOPPED
                ),
                reason=(
                    "Runtime stopped."
                ),
            )
        )

        print()

        print(
            "Runtime stopped."
        )