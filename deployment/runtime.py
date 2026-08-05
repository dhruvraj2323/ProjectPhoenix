"""
=================================================
Project Phoenix
Deployment Runtime
M58.12.12
=================================================
"""

from __future__ import annotations

from deployment.continuous_runner import (
    ContinuousRunner,
)

from deployment.runtime_config import (
    RuntimeConfig,
)


class Runtime:
    """
    Controls the runtime lifecycle
    of Project Phoenix.
    """

    def __init__(
        self,
    ) -> None:

        self.running = False

        self.config = RuntimeConfig()

        # ------------------------------------------
        # Continuous Runner
        # ------------------------------------------

        self.runner = ContinuousRunner(

            interval=self.config.interval,

        )

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def start(
        self,
        cycles: int | None = None,
    ) -> None:
        """
        Start runtime.
        """

        self.running = True

        print()

        print(
            "Runtime started.",
        )

        print()

        print(
            "Starting Continuous Runner...",
        )

        if cycles is None:

            cycles = self.config.cycles

        self.runner.start(

            cycles=cycles,

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

        self.runner.stop()

        self.running = False

        print()

        print(
            "Runtime stopped.",
        )