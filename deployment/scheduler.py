"""
=================================================
Project Phoenix
Deployment Scheduler
M58
=================================================
"""

from __future__ import annotations

import time

from deployment.runtime import Runtime


class Scheduler:
    """
    Controls trading cycle execution.
    """

    def __init__(
        self,
        runtime: Runtime,
        interval: int = 60,
    ) -> None:

        self.runtime = runtime

        self.interval = interval

        self.running = False

    # --------------------------------------------------
    # Execute One Cycle
    # --------------------------------------------------

    def run_once(
        self,
    ) -> None:
        """
        Execute one trading cycle.
        """

        self.runtime.start()

    # --------------------------------------------------
    # Wait
    # --------------------------------------------------

    def wait(
        self,
    ) -> None:
        """
        Wait until next cycle.
        """

        time.sleep(
            self.interval,
        )

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> None:
        """
        Stop scheduler.
        """

        self.running = False