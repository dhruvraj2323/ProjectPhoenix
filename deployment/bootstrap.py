"""
=================================================
Project Phoenix
Deployment Bootstrap
M58
=================================================
"""

from __future__ import annotations

from deployment.runtime import Runtime


class Bootstrap:
    """
    Initializes and shuts down
    Project Phoenix.
    """

    def __init__(
        self,
    ) -> None:

        self.runtime = Runtime()

        self.started = False

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def start(
        self,
    ) -> None:
        """
        Start Project Phoenix.
        """

        print()

        print(
            "Initializing Project Phoenix...",
        )

        self.started = True

        self.runtime.start()

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> None:
        """
        Shutdown Project Phoenix.
        """

        if not self.started:

            return

        self.runtime.stop()

        self.started = False

        print()

        print(
            "Project Phoenix stopped.",
        )