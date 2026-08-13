"""
=================================================
Project Phoenix
Runtime Manager
M61.8.4 - Trading Protection Integration
=================================================
"""

from __future__ import annotations

from deployment.runtime import Runtime

from deployment.runtime_watchdog import (
    HealthTransition,
    RuntimeWatchdog,
    WatchdogHealthState,
)

from deployment.trading_protection import (
    TradingProtection,
    TradingProtectionState,
)


class RuntimeManager:
    """
    Controls the Project Phoenix runtime.

    M61.8.4 responsibilities:
    - Own Runtime
    - Own RuntimeWatchdog
    - Own TradingProtection
    - Delegate runtime lifecycle
    - Expose runtime health state
    - Expose trading protection state
    - Update trading protection from health state

    M61.8.4 does NOT:
    - stop runtime automatically
    - restart runtime automatically
    - close existing positions
    - cancel existing orders
    - execute trades
    """

    def __init__(
        self,
        runtime: Runtime | None = None,
        watchdog: RuntimeWatchdog | None = None,
        trading_protection: TradingProtection | None = None,
    ) -> None:

        self.trading_protection = (
            trading_protection
            if trading_protection is not None
            else TradingProtection()
        )

        self.runtime = (
            runtime
            if runtime is not None
            else Runtime(
                trading_protection=(
                    self.trading_protection
                ),
            )
        )

        self.watchdog = (
            watchdog
            if watchdog is not None
            else RuntimeWatchdog()
        )

        self.running = False

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def start(
        self,
        cycles: int = 1,
    ) -> bool:
        """
        Start the application runtime.
        """

        result = self.runtime.start(
            cycles=cycles,
        )

        self.running = (
            self.runtime.running
        )

        return bool(result)

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> bool:
        """
        Stop the application runtime.
        """

        self.runtime.stop()

        self.running = (
            self.runtime.running
        )

        return True

    # --------------------------------------------------
    # Restart
    # --------------------------------------------------

    def restart(
        self,
        cycles: int = 1,
    ) -> bool:
        """
        Restart the application runtime.
        """

        self.stop()

        return self.start(
            cycles=cycles,
        )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def status(
        self,
    ) -> bool:

        self.running = (
            self.runtime.running
        )

        return self.running

    # --------------------------------------------------
    # Health Check
    # --------------------------------------------------

    def health_state(
        self,
    ) -> WatchdogHealthState:
        """
        Check runtime health and update trading
        protection accordingly.
        """

        state = (
            self.watchdog.check()
        )

        self.trading_protection.update(
            state,
        )

        return state

    # --------------------------------------------------
    # Health Transition
    # --------------------------------------------------

    def health_transition(
        self,
    ) -> HealthTransition | None:
        """
        Return the latest observed health transition.
        """

        return (
            self.watchdog.last_transition
        )

    # --------------------------------------------------
    # Health Transition Detection
    # --------------------------------------------------

    def health_transition_detected(
        self,
    ) -> bool:

        return (
            self.watchdog.has_transitioned()
        )

    # --------------------------------------------------
    # Health Recovery
    # --------------------------------------------------

    def health_recovered(
        self,
    ) -> bool:

        return (
            self.watchdog.has_recovered()
        )

    # --------------------------------------------------
    # Clear Health Transition
    # --------------------------------------------------

    def clear_health_transition(
        self,
    ) -> None:

        self.watchdog.clear_transition()

    # --------------------------------------------------
    # Trading Protection State
    # --------------------------------------------------

    def trading_protection_state(
        self,
    ) -> TradingProtectionState:
        """
        Return the current trading protection state.
        """

        return (
            self.trading_protection.state
        )

    # --------------------------------------------------
    # Trading Permission
    # --------------------------------------------------

    def can_trade(
        self,
    ) -> bool:
        """
        Return whether new trading activity
        is currently permitted.
        """

        return (
            self.trading_protection.can_trade()
        )

    # --------------------------------------------------
    # Trading Pause
    # --------------------------------------------------

    def trading_paused(
        self,
    ) -> bool:
        """
        Return whether new trading activity
        is currently paused.
        """

        return (
            self.trading_protection.is_paused()
        )

    # --------------------------------------------------
    # Trading Protection Transition
    # --------------------------------------------------

    def trading_protection_transition(
        self,
    ):
        """
        Return the latest trading protection
        transition.
        """

        return (
            self.trading_protection.last_transition
        )

    # --------------------------------------------------
    # Clear Trading Protection Transition
    # --------------------------------------------------

    def clear_trading_protection_transition(
        self,
    ) -> None:

        self.trading_protection.clear_transition()