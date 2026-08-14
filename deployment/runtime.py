"""
=================================================
Project Phoenix
Runtime
M62.4.5 - Runtime Trading Protection Integration
=================================================
"""

from __future__ import annotations

from datetime import datetime, timezone

from config.configuration_readiness_models import (
    ConfigurationReadinessResult,
)

from deployment.continuous_runner import (
    ContinuousRunner,
)

from deployment.health_degradation_policy import (
    HealthDegradationPolicy,
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

from deployment.runtime_watchdog import (
    WatchdogHealthState,
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
    - Expose structured runtime status
    - Apply health degradation
    - Apply health recovery
    - Synchronize TradingProtection with health state
    - Pass TradingProtection to ContinuousRunner
    - Start ContinuousRunner only when ready
    - Preserve runtime stop behavior

    This class does not:
    - execute trades
    - grant live-trading approval
    - close positions
    - cancel orders
    - automatically restart the runtime
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

        self.health_degradation_policy = (
            HealthDegradationPolicy()
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
        Return True when deployment health passes
        the startup health gate.
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
        Return True only when configuration readiness
        and deployment health both pass.
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
        Return current runtime operational status.
        """

        return self._operational_status

    # --------------------------------------------------
    # Health Degradation / Recovery
    # --------------------------------------------------

    def apply_health_state(
        self,
        health_state: WatchdogHealthState,
    ) -> bool:
        """
        Apply an observed watchdog health state.

        HEALTHY:
            Recover an already-running runtime to RUNNING
            and activate TradingProtection.

        UNHEALTHY:
            Move an already-running runtime to DEGRADED
            and pause TradingProtection.

        This method does not:
        - start runtime
        - stop runtime
        - restart runtime
        - execute trades
        """

        decision = (
            self.health_degradation_policy.evaluate(
                health_state,
            )
        )

        # ----------------------------------------------
        # Healthy / Recovery
        # ----------------------------------------------

        if (
            health_state
            == WatchdogHealthState.HEALTHY
        ):

            if not self.running:
                return False

            if (
                self._operational_status.state
                not in (
                    RuntimeOperationalState.DEGRADED,
                    RuntimeOperationalState.RUNNING,
                )
            ):
                return False

            # TradingProtection owns the actual
            # protection transition.
            self.trading_protection.update(
                health_state,
            )

            self._operational_status = (
                RuntimeOperationalStatus(
                    state=(
                        RuntimeOperationalState.RUNNING
                    ),
                    reason=(
                        "Runtime health recovered; "
                        "runtime is operational."
                    ),
                )
            )

            return True

        # ----------------------------------------------
        # Unhealthy / Degradation
        # ----------------------------------------------

        if (
            health_state
            == WatchdogHealthState.UNHEALTHY
        ):

            if not self.running:
                return False

            if (
                self._operational_status.state
                not in (
                    RuntimeOperationalState.RUNNING,
                    RuntimeOperationalState.DEGRADED,
                )
            ):
                return False

            # TradingProtection owns the actual
            # protection transition.
            self.trading_protection.update(
                health_state,
            )

            self._operational_status = (
                RuntimeOperationalStatus(
                    state=(
                        RuntimeOperationalState.DEGRADED
                    ),
                    reason=(
                        decision.reason
                    ),
                )
            )

            return True

        return False

    # --------------------------------------------------
    # Runtime Status
    # --------------------------------------------------

    def status_snapshot(
        self,
    ) -> RuntimeStatus:
        """
        Return immutable runtime observability snapshot.
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
                datetime.now(
                    timezone.utc
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

        Startup is blocked when configuration readiness
        or deployment health fails.
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