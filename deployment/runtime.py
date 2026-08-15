"""
=================================================
Project Phoenix
Runtime
M62.7.3 - Runtime Lifecycle Integration
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

from deployment.operational_alert_dispatcher import (
    OperationalAlertDispatcher,
)

from deployment.operational_incident_classifier import (
    OperationalIncidentClassifier,
)

from deployment.operational_incident_models import (
    OperationalIncidentEventType,
)

from deployment.runtime_lifecycle import (
    RuntimeLifecycle,
)

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
    RuntimeOperationalStatus,
)

from deployment.runtime_readiness import (
    RuntimeReadinessAdapter,
)

from deployment.runtime_session import (
    RuntimeSession,
)

from deployment.runtime_status import (
    RuntimeStatus,
)

from deployment.runtime_watchdog import (
    RuntimeWatchdog,
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
    - Expose the authoritative RuntimeLifecycle contract
    - Manage runtime session metadata
    - Apply health degradation
    - Apply health recovery
    - Synchronize TradingProtection with health state
    - Integrate RuntimeWatchdog
    - Generate operational incidents
    - Dispatch operational alerts
    - Pass TradingProtection to ContinuousRunner
    - Start ContinuousRunner only when ready
    - Preserve runtime stop behavior

    This class does not:
    - execute trades
    - grant live-trading approval
    - close positions
    - cancel orders
    - automatically restart the runtime
    - directly send Telegram or Email alerts

    RuntimeLifecycle remains stateless and authoritative for
    transition validation.

    RuntimeOperationalStatus remains the single runtime
    state store.

    RuntimeSession owns session identity and timing metadata.
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
        watchdog: RuntimeWatchdog | None = None,
        alert_dispatcher: (
            OperationalAlertDispatcher | None
        ) = None,
    ) -> None:

        self.interval = interval

        self.running = False

        self.configuration_readiness = (
            configuration_readiness
        )

        # --------------------------------------------------
        # Authoritative Lifecycle Contract
        #
        # RuntimeLifecycle is intentionally stateless.
        # Runtime does not create a second lifecycle state
        # store here.
        # --------------------------------------------------

        self.lifecycle = RuntimeLifecycle()

        # --------------------------------------------------
        # Runtime Session
        #
        # Session identity is independent from the
        # lifecycle transition contract.
        # --------------------------------------------------

        self.session = (
            RuntimeSession.create()
        )

        # --------------------------------------------------
        # Shared Health Monitor
        # --------------------------------------------------

        self.health_monitor = (
            HealthMonitor()
        )

        # --------------------------------------------------
        # Trading Protection
        # --------------------------------------------------

        self.trading_protection = (
            trading_protection
            if trading_protection is not None
            else TradingProtection()
        )

        # --------------------------------------------------
        # Continuous Runner
        # --------------------------------------------------

        self.continuous_runner = (
            ContinuousRunner(
                interval=interval,
                trading_protection=(
                    self.trading_protection
                ),
            )
        )

        # --------------------------------------------------
        # Health Degradation Policy
        # --------------------------------------------------

        self.health_degradation_policy = (
            HealthDegradationPolicy()
        )

        # --------------------------------------------------
        # Runtime Watchdog
        # --------------------------------------------------

        self.watchdog = (
            watchdog
            if watchdog is not None
            else RuntimeWatchdog(
                health_monitor=(
                    self.health_monitor
                ),
            )
        )

        # --------------------------------------------------
        # Operational Alert Dispatcher
        # --------------------------------------------------

        self.alert_dispatcher = (
            alert_dispatcher
            if alert_dispatcher is not None
            else OperationalAlertDispatcher()
        )

        # --------------------------------------------------
        # Operational Alert Sequence
        # --------------------------------------------------

        self._alert_sequence = 0

        # --------------------------------------------------
        # Operational Status
        #
        # This remains the single runtime state store.
        # --------------------------------------------------

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

    # ==================================================
    # Configuration Readiness
    # ==================================================

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

    # ==================================================
    # Deployment Health
    # ==================================================

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

    # ==================================================
    # Readiness Check
    # ==================================================

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

    # ==================================================
    # Operational State
    # ==================================================

    def operational_state(
        self,
    ) -> RuntimeOperationalStatus:
        """
        Return current runtime operational status.

        RuntimeOperationalStatus remains the single
        authoritative runtime state store.
        """

        return self._operational_status

    # ==================================================
    # Lifecycle Contract
    # ==================================================

    def transition_to(
        self,
        next_state: RuntimeOperationalState,
        reason: str = "",
    ) -> RuntimeOperationalStatus:
        """
        Validate and apply a lifecycle transition.

        RuntimeLifecycle owns transition validation.

        RuntimeOperationalStatus remains the runtime's
        actual state store.

        This method intentionally does not:
        - execute trades
        - grant trading permission
        - control TradingProtection
        - send alerts
        - start ContinuousRunner
        - stop ContinuousRunner
        """

        current_state = (
            self._operational_status.state
        )

        self.lifecycle.validate_transition(
            current_state,
            next_state,
        )

        transition_reason = (
            reason
            if reason
            else (
                f"Runtime transitioned from "
                f"{current_state.value} to "
                f"{next_state.value}."
            )
        )

        self._operational_status = (
            RuntimeOperationalStatus(
                state=next_state,
                reason=transition_reason,
            )
        )

        return self._operational_status

    # ==================================================
    # Operational Alert Support
    # ==================================================

    def _next_alert_sequence(
        self,
    ) -> int:
        """
        Generate the next deterministic runtime-local
        alert sequence number.
        """

        self._alert_sequence += 1

        return self._alert_sequence

    def _emit_operational_alert(
        self,
        event_type: OperationalIncidentEventType,
        message: str,
    ) -> None:
        """
        Create and dispatch one operational incident.

        Alert delivery failures are intentionally isolated
        from runtime execution.
        """

        sequence = (
            self._next_alert_sequence()
        )

        incident = (
            OperationalIncidentClassifier.classify(
                event_type=event_type,
                message=message,
                timestamp=(
                    datetime.now(
                        timezone.utc
                    )
                ),
                incident_id=(
                    f"INC-{sequence:06d}"
                ),
                processing_cycle_id=(
                    f"RUNTIME-{sequence:06d}"
                ),
            )
        )

        try:

            self.alert_dispatcher.dispatch(
                incident
            )

        except Exception as exc:

            print()
            print(
                "Operational alert dispatch failed."
            )
            print(exc)

    # ==================================================
    # Health Degradation / Recovery
    # ==================================================

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

        # --------------------------------------------------
        # Healthy / Recovery
        # --------------------------------------------------

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

            self.trading_protection.update(
                health_state,
            )

            current_state = (
                self._operational_status.state
            )

            if (
                current_state
                == RuntimeOperationalState.DEGRADED
            ):

                self.transition_to(
                    RuntimeOperationalState.RUNNING,
                    reason=(
                        "Runtime health recovered; "
                        "runtime is operational."
                    ),
                )

            return True

        # --------------------------------------------------
        # Unhealthy / Degradation
        # --------------------------------------------------

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

            self.trading_protection.update(
                health_state,
            )

            current_state = (
                self._operational_status.state
            )

            if (
                current_state
                == RuntimeOperationalState.RUNNING
            ):

                self.transition_to(
                    RuntimeOperationalState.DEGRADED,
                    reason=decision.reason,
                )

            return True

        return False

    # ==================================================
    # Runtime Watchdog
    # ==================================================

    def check_watchdog(
        self,
    ) -> WatchdogHealthState:
        """
        Check runtime health through RuntimeWatchdog.

        The watchdog always observes current health.

        A stopped runtime is never started or degraded
        by the watchdog.

        For a running runtime, a new watchdog transition
        is processed exactly once.
        """

        health_state = (
            self.watchdog.check()
        )

        # --------------------------------------------------
        # Stopped runtime
        # --------------------------------------------------

        if not self.running:

            if self.watchdog.has_transitioned():

                self.watchdog.clear_transition()

            return health_state

        # --------------------------------------------------
        # Running runtime
        # --------------------------------------------------

        if self.watchdog.has_transitioned():

            transition = (
                self.watchdog.last_transition
            )

            if transition is not None:

                # ------------------------------------------
                # Healthy → Unhealthy
                # ------------------------------------------

                if (
                    transition.current_state
                    == WatchdogHealthState.UNHEALTHY
                ):

                    self.apply_health_state(
                        WatchdogHealthState.UNHEALTHY
                    )

                    self._emit_operational_alert(
                        OperationalIncidentEventType
                        .HEALTH_DEGRADED,
                        "Runtime health degraded.",
                    )

                # ------------------------------------------
                # Unhealthy → Healthy
                # ------------------------------------------

                elif (
                    transition.previous_state
                    == WatchdogHealthState.UNHEALTHY
                    and
                    transition.current_state
                    == WatchdogHealthState.HEALTHY
                ):

                    self.apply_health_state(
                        WatchdogHealthState.HEALTHY
                    )

                    self._emit_operational_alert(
                        OperationalIncidentEventType
                        .HEALTH_RECOVERED,
                        "Runtime health recovered.",
                    )

            self.watchdog.clear_transition()

        return health_state

    # ==================================================
    # Runtime Status
    # ==================================================

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

    # ==================================================
    # Start
    # ==================================================

    def start(
        self,
        cycles: int = 1,
    ) -> bool:
        """
        Start Project Phoenix runtime.

        Runtime session control is established here.

        The lifecycle contract itself remains stateless;
        the RuntimeOperationalStatus stores the current
        operational state.
        """

        # --------------------------------------------------
        # Duplicate Start Protection
        # --------------------------------------------------

        if self.running:

            return False

        # --------------------------------------------------
        # Begin Session
        #
        # A Runtime instance represents one runtime
        # controller. A session is created once and becomes
        # active when startup begins.
        # --------------------------------------------------

        if self.session.terminal:

            return False

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

        # --------------------------------------------------
        # Activate Session
        # --------------------------------------------------

        if not self.session.active:

            try:

                self.session = (
                    self.session.start()
                )

            except RuntimeError:

                self._operational_status = (
                    RuntimeOperationalStatus(
                        state=(
                            RuntimeOperationalState.FAILED
                        ),
                        reason=(
                            "Runtime session could "
                            "not be started."
                        ),
                    )
                )

                return False

        # --------------------------------------------------
        # Configuration Readiness Gate
        # --------------------------------------------------

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

            self._emit_operational_alert(
                OperationalIncidentEventType
                .CONFIGURATION_FAILURE,
                (
                    "Runtime startup blocked "
                    "by configuration readiness."
                ),
            )

            return False

        # --------------------------------------------------
        # Deployment Health Gate
        # --------------------------------------------------

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

            self._emit_operational_alert(
                OperationalIncidentEventType
                .DEPLOYMENT_HEALTH_FAILURE,
                (
                    "Runtime startup blocked "
                    "by deployment health."
                ),
            )

            return False

        # --------------------------------------------------
        # Runtime Ready
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Start Continuous Runner
        # --------------------------------------------------

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

            self._emit_operational_alert(
                OperationalIncidentEventType
                .RUNTIME_FAILURE,
                "Runtime execution failed.",
            )

            return False

    # ==================================================
    # Stop
    # ==================================================

    def stop(
        self,
    ) -> None:
        """
        Stop Project Phoenix runtime.

        The operational state follows:

            RUNNING / DEGRADED
                ↓
            STOPPING
                ↓
            STOPPED

        Session metadata becomes terminal after shutdown.
        """

        # --------------------------------------------------
        # Duplicate Stop Protection
        # --------------------------------------------------

        if not self.running:

            return

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

        # --------------------------------------------------
        # Close Runtime Session
        # --------------------------------------------------

        if self.session.active:

            try:

                self.session = (
                    self.session.stop()
                )

            except RuntimeError:

                pass

        print()
        print(
            "Runtime stopped."
        )

        self._emit_operational_alert(
            OperationalIncidentEventType
            .RUNTIME_SHUTDOWN,
            "Runtime stopped.",
        )