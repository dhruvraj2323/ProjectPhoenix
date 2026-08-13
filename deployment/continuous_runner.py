"""
=================================================
Project Phoenix
Continuous Runner
M61.8.5 - Trading Protection Boundary
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

from deployment.trading_protection import (
    TradingProtection,
)


class ContinuousRunner:
    """
    Executes Project Phoenix continuously.

    M61.8.5 responsibilities:
    - Execute TradingCycle
    - Interpret cycle execution summary
    - Respect TradingProtection
    - Block new trading when protection is PAUSED
    - Preserve continuous execution behavior
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

        self.trading_protection = (
            trading_protection
            if trading_protection is not None
            else TradingProtection()
        )

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

        When trading protection is PAUSED,
        TradingCycle.execute() is not called.

        The runner itself remains operational.
        """

        try:

            # --------------------------------------------------
            # Trading Protection Boundary
            # --------------------------------------------------

            if not self.trading_protection.can_trade():

                print()

                print(
                    "Trading Protection Active:"
                )

                print(
                    "New trading is paused."
                )

                return True

            # --------------------------------------------------
            # Execute Trading Cycle
            # --------------------------------------------------

            success = (
                self.trading_cycle.execute()
            )

            execution_summary = getattr(
                self.trading_cycle,
                "execution_summary",
                None,
            )

            if execution_summary is None:

                return bool(success)

            if (
                execution_summary.status
                == CycleExecutionStatus.ALL_FAILED
            ):

                return False

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
                # Protected Cycle
                # --------------------------------------------------

                if (
                    not self.trading_protection.can_trade()
                ):

                    print()

                    print(
                        f"Cycle {current_cycle} "
                        "Paused - Trading Protection Active."
                    )

                elif execution_summary is not None:

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