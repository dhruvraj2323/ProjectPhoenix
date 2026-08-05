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
        Execute TradingCycle continuously.

        For deployment testing,
        the number of cycles can be limited.
        """

        self.running = True

        current_cycle = 1

        while self.running:

            print()

            print("=" * 60)

            print(
                f"Starting Cycle {current_cycle}"
            )

            print("=" * 60)

            try:

                success = self.run_once()

                if success:

                    print()

                    print(
                        f"Cycle {current_cycle} Completed Successfully."
                    )

                else:

                    print()

                    print(
                        f"Cycle {current_cycle} Failed."
                    )

            except Exception as exc:

                print()

                print(
                    f"Cycle {current_cycle} Exception:"
                )

                print(exc)

            if (
                cycles > 0
                and current_cycle >= cycles
            ):

                break

            print()

            print(
                f"Waiting {self.interval} seconds..."
            )

            time.sleep(
                self.interval,
            )

            current_cycle += 1

        self.running = False

        print()

        print(
            "Continuous Runner Stopped."
        )

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(
        self,
    ) -> None:

        self.running = False