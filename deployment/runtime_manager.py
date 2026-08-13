"""
=================================================
Project Phoenix
Runtime Manager
M61.6.3 - Runtime Readiness Integration
=================================================
"""

from __future__ import annotations

from deployment.runtime import (
    Runtime,
)


class RuntimeManager:
    """
    Controls the Project Phoenix runtime.

    M61.6.3 responsibilities:
    - Own the Runtime instance
    - Delegate startup to Runtime
    - Respect the Runtime readiness gate
    - Delegate shutdown
    - Expose runtime state
    """

    def __init__(
        self,
        runtime: Runtime | None = None,
    ) -> None:

        self.runtime = (
            runtime
            if runtime is not None
            else Runtime()
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

        Returns False when the Runtime readiness
        gate blocks startup.
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