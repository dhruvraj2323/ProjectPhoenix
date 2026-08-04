"""
=================================================
Project Phoenix
Deployment Runtime
M58
=================================================
"""

from __future__ import annotations


class Runtime:
    """
    Controls the runtime lifecycle
    of Project Phoenix.
    """

    def __init__(
        self,
    ) -> None:

        self.running = False

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def start(
        self,
    ) -> None:
        """
        Start runtime.
        """

        self.running = True

        print()

        print(
            "Runtime started.",
        )

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> None:
        """
        Stop runtime.
        """

        self.running = False

        print()

        print(
            "Runtime stopped.",
        )