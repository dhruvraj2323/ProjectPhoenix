"""
=================================================
Project Phoenix
Continuous Runner
M61.5 - Deployment Runtime Status
=================================================
"""

from __future__ import annotations

import time

from deployment.execution_summary import (
    CycleExecutionStatus,
)

from deployment.trading_cycle import (
    TradingCycle,
)


class ContinuousRunner:
    """
    Executes Project Phoenix continuously.

    M61.5 responsibilities:
    - Execute TradingCycle
    - Interpret cycle execution summary
    - Distinguish successful, partial,
      no-trade and failed cycles
    - Preserve continuous execution behavior
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

        Returns
        -------
        bool
            True when the cycle completed without
            an execution exception.

            False when TradingCycle raised an
            exception or the cycle ended with
            ALL_FAILED status.
        """

        try:

            success = (
                self.trading_cycle.execute()
            )

            # --------------------------------------------------
            # Execution Summary
            # --------------------------------------------------

            execution_summary = getattr(
                self.trading_cycle,
                "execution_summary",
                None,
            )

            if execution_summary is None:

                return bool(success)

            # --------------------------------------------------
            # ALL_FAILED
            # --------------------------------------------------

            if (
                execution_summary.status
                == CycleExecutionStatus.ALL_FAILED
            ):

                return False

            # --------------------------------------------------
            # ALL_EXECUTED
            # PARTIAL_SUCCESS
            # NO_TRADES
            # --------------------------------------------------

            return bool(success)

        except Exception as exc:

            print()

            print(
                "Continuous Runner Cycle Exception:"
            )

            print(exc)

            return False

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

                execution_summary = getattr(
                    self.trading_cycle,
                    "execution_summary",
                    None,
                )

                # --------------------------------------------------
                # Cycle Status
                # --------------------------------------------------

                if execution_summary is not None:

                    status = (
                        execution_summary.status
                    )

                    if (
                        status
                        == CycleExecutionStatus.ALL_EXECUTED
                    ):

                        print()

                        print(
                            f"Cycle {current_cycle} "
                            "Completed Successfully."
                        )

                    elif (
                        status
                        == CycleExecutionStatus.PARTIAL_SUCCESS
                    ):

                        print()

                        print(
                            f"Cycle {current_cycle} "
                            "Completed With Partial Success."
                        )

                    elif (
                        status
                        == CycleExecutionStatus.NO_TRADES
                    ):

                        print()

                        print(
                            f"Cycle {current_cycle} "
                            "Completed With No Trades."
                        )

                    elif (
                        status
                        == CycleExecutionStatus.ALL_FAILED
                    ):

                        print()

                        print(
                            f"Cycle {current_cycle} "
                            "Failed - All Symbols Failed."
                        )

                    else:

                        print()

                        print(
                            f"Cycle {current_cycle} "
                            "Completed."
                        )

                elif success:

                    print()

                    print(
                        f"Cycle {current_cycle} "
                        "Completed Successfully."
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

            # --------------------------------------------------
            # Cycle Limit
            # --------------------------------------------------

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