"""
=================================================
Project Phoenix
Continuous Runner
M58
=================================================
"""

from __future__ import annotations

import time

from deployment.trading_cycle import (
    TradingCycle,
)


class ContinuousRunner:
    """
    Executes Project Phoenix
    continuously.
    """

    def __init__(
        self,
        interval: int = 300,
    ) -> None:

        self.interval = interval

        self.running = False

        self.trading_cycle = (
            TradingCycle()
        )

    # --------------------------------------------------
    # Run One Cycle
    # --------------------------------------------------

    def run_once(
        self,
    ) -> bool:
        """
        Execute one trading cycle.
        """

        return (
            self.trading_cycle.execute()
        )

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    def start(
        self,
        cycles: int = 1,
    ) -> None:
        """
        Start continuous execution.

        'cycles' is limited for testing.
        """

        self.running = True

        count = 0

        while self.running:

            self.run_once()

            count += 1

            if count >= cycles:

                break

            time.sleep(
                self.interval,
            )

        self.running = False

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> None:

        self.running = False