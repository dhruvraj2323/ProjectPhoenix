"""
=================================================
Project Phoenix
Runtime
M61.8.5 - Trading Protection Boundary
=================================================
"""

from __future__ import annotations

from deployment.continuous_runner import (
    ContinuousRunner,
)

from deployment.health_monitor import (
    HealthMonitor,
)

from deployment.trading_protection import (
    TradingProtection,
)


class Runtime:
    """
    Project Phoenix runtime controller.

    M61.8.5 responsibilities:
    - Check deployment health before startup
    - Block startup when system is unhealthy
    - Pass TradingProtection to ContinuousRunner
    - Start ContinuousRunner only when healthy
    - Preserve runtime stop behavior
    """

    def __init__(
        self,
        interval: int = 300,
        trading_protection: (
            TradingProtection | None
        ) = None,
    ) -> None:

        self.interval = interval

        self.running = False

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

    # --------------------------------------------------
    # Readiness Check
    # --------------------------------------------------

    def is_ready(self) -> bool:
        """
        Return True when deployment health
        passes the startup readiness gate.
        """

        return (
            self.health_monitor.is_healthy()
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
        """

        if not self.is_ready():

            self.running = False

            print()

            print(
                "Runtime startup blocked."
            )

            print(
                "Deployment health check failed."
            )

            return False

        self.running = True

        print()

        print(
            "Runtime started."
        )

        try:

            self.continuous_runner.start(
                cycles=cycles,
            )

            return True

        except Exception as exc:

            print()

            print(
                "Runtime execution failed."
            )

            print(exc)

            self.running = False

            return False

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> None:

        self.running = False

        self.continuous_runner.stop()

        print()

        print(
            "Runtime stopped."
        )