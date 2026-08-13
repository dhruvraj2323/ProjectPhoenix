"""
=================================================
Project Phoenix
Deployment Bootstrap
M61.6.3 - Runtime Readiness Integration
=================================================
"""

from __future__ import annotations

from deployment.runtime import (
    Runtime,
)


class Bootstrap:
    """
    Initializes and shuts down
    Project Phoenix.

    M61.6.3:
    Bootstrap now respects the Runtime
    readiness gate.
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

        self.started = False

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def start(
        self,
        cycles: int = 1,
    ) -> bool:
        """
        Start Project Phoenix.

        Returns True only when Runtime
        successfully starts.
        """

        print()

        print(
            "Initializing Project Phoenix...",
        )

        result = self.runtime.start(
            cycles=cycles,
        )

        self.started = bool(
            result
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

        return self.started

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> bool:
        """
        Shutdown Project Phoenix.
        """

        if not self.started:

            return False

        self.runtime.stop()

        self.started = False

        print()

        print(
            "Project Phoenix stopped.",
        )

        return True