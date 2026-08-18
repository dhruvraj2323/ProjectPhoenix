"""
=================================================
Project Phoenix
Trade Reconciliation
M63.4
=================================================

Purpose
-------
Reconcile Phoenix internal execution state against
broker-side MT5 order, position and history state.

This module does NOT execute, modify or close trades.

It only determines whether the observed broker state
matches the expected Phoenix execution state.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


# =========================================================
# Reconciliation Status
# =========================================================

class ReconciliationStatus(Enum):
    MATCHED = "MATCHED"
    MISSING_ORDER = "MISSING_ORDER"
    UNEXPECTED_POSITION = "UNEXPECTED_POSITION"
    DUPLICATE_ORDER = "DUPLICATE_ORDER"
    REJECTED_ORDER = "REJECTED_ORDER"
    PARTIAL_EXECUTION = "PARTIAL_EXECUTION"
    STALE_STATE = "STALE_STATE"
    EXECUTION_MISMATCH = "EXECUTION_MISMATCH"


# =========================================================
# Reconciliation Result
# =========================================================

@dataclass(frozen=True)
class ReconciliationResult:
    status: ReconciliationStatus
    expected_ticket: int | None = None
    observed_order_count: int = 0
    observed_position_count: int = 0
    observed_history_count: int = 0
    expected_volume: float = 0.0
    observed_volume: float = 0.0
    message: str = ""

    @property
    def matched(self) -> bool:
        return (
            self.status
            == ReconciliationStatus.MATCHED
        )


# =========================================================
# Trade Reconciler
# =========================================================

class TradeReconciler:
    """
    Compares expected Phoenix execution state with
    broker-side state.

    Broker objects are intentionally treated as generic
    objects because MT5 namedtuple structures are supplied
    by the broker API.
    """

    def reconcile(
        self,
        expected_ticket: int | None,
        expected_volume: float,
        orders: list[Any] | tuple[Any, ...] | None,
        positions: list[Any] | tuple[Any, ...] | None,
        history: list[Any] | tuple[Any, ...] | None,
        execution_status: Any = None,
    ) -> ReconciliationResult:

        orders = list(
            orders
            if orders is not None
            else []
        )

        positions = list(
            positions
            if positions is not None
            else []
        )

        history = list(
            history
            if history is not None
            else []
        )

        # -------------------------------------------------
        # Rejected / failed Phoenix execution
        # -------------------------------------------------

        if self._is_rejected(execution_status):

            return ReconciliationResult(
                status=(
                    ReconciliationStatus.REJECTED_ORDER
                ),
                expected_ticket=expected_ticket,
                observed_order_count=len(orders),
                observed_position_count=len(positions),
                observed_history_count=len(history),
                expected_volume=expected_volume,
                message=(
                    "Phoenix execution was rejected "
                    "or failed."
                ),
            )

        # -------------------------------------------------
        # Missing broker state
        # -------------------------------------------------

        if expected_ticket is None:

            return ReconciliationResult(
                status=(
                    ReconciliationStatus.MISSING_ORDER
                ),
                observed_order_count=len(orders),
                observed_position_count=len(positions),
                observed_history_count=len(history),
                expected_volume=expected_volume,
                message=(
                    "Phoenix execution has no broker "
                    "ticket."
                ),
            )

        # -------------------------------------------------
        # Duplicate broker order
        # -------------------------------------------------

        matching_orders = [
            order
            for order in orders
            if self._ticket(order)
            == expected_ticket
        ]

        if len(matching_orders) > 1:

            return ReconciliationResult(
                status=(
                    ReconciliationStatus.DUPLICATE_ORDER
                ),
                expected_ticket=expected_ticket,
                observed_order_count=len(orders),
                observed_position_count=len(positions),
                observed_history_count=len(history),
                expected_volume=expected_volume,
                observed_volume=self._total_volume(
                    matching_orders
                ),
                message=(
                    "Multiple broker orders were found "
                    "for the same Phoenix ticket."
                ),
            )

        # -------------------------------------------------
        # Position mismatch
        # -------------------------------------------------

        matching_positions = [
            position
            for position in positions
            if self._ticket(position)
            == expected_ticket
        ]

        if len(matching_positions) == 0:

            # History may prove that the execution already
            # completed and the position is legitimately gone.
            if history:

                return ReconciliationResult(
                    status=(
                        ReconciliationStatus.STALE_STATE
                    ),
                    expected_ticket=expected_ticket,
                    observed_order_count=len(orders),
                    observed_position_count=len(
                        positions
                    ),
                    observed_history_count=len(
                        history
                    ),
                    expected_volume=expected_volume,
                    message=(
                        "Execution history exists but "
                        "current position state is absent."
                    ),
                )

            return ReconciliationResult(
                status=(
                    ReconciliationStatus.UNEXPECTED_POSITION
                ),
                expected_ticket=expected_ticket,
                observed_order_count=len(orders),
                observed_position_count=len(
                    positions
                ),
                observed_history_count=len(history),
                expected_volume=expected_volume,
                message=(
                    "Expected position was not found "
                    "in broker state."
                ),
            )

        # -------------------------------------------------
        # Volume reconciliation
        # -------------------------------------------------

        observed_volume = self._total_volume(
            matching_positions
        )

        if not self._volume_matches(
            expected_volume,
            observed_volume,
        ):

            if observed_volume < expected_volume:

                return ReconciliationResult(
                    status=(
                        ReconciliationStatus.PARTIAL_EXECUTION
                    ),
                    expected_ticket=expected_ticket,
                    observed_order_count=len(orders),
                    observed_position_count=len(
                        positions
                    ),
                    observed_history_count=len(history),
                    expected_volume=expected_volume,
                    observed_volume=observed_volume,
                    message=(
                        "Observed broker volume is lower "
                        "than the expected execution volume."
                    ),
                )

            return ReconciliationResult(
                status=(
                    ReconciliationStatus.EXECUTION_MISMATCH
                ),
                expected_ticket=expected_ticket,
                observed_order_count=len(orders),
                observed_position_count=len(
                    positions
                ),
                observed_history_count=len(history),
                expected_volume=expected_volume,
                observed_volume=observed_volume,
                message=(
                    "Observed broker volume does not "
                    "match Phoenix execution volume."
                ),
            )

        # -------------------------------------------------
        # Final successful reconciliation
        # -------------------------------------------------

        return ReconciliationResult(
            status=ReconciliationStatus.MATCHED,
            expected_ticket=expected_ticket,
            observed_order_count=len(orders),
            observed_position_count=len(
                positions
            ),
            observed_history_count=len(history),
            expected_volume=expected_volume,
            observed_volume=observed_volume,
            message="Phoenix and broker state match.",
        )

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _ticket(
        broker_object: Any,
    ) -> int | None:

        return getattr(
            broker_object,
            "ticket",
            None,
        )

    @staticmethod
    def _volume(
        broker_object: Any,
    ) -> float:

        value = getattr(
            broker_object,
            "volume",
            0.0,
        )

        try:
            return float(value)
        except (
            TypeError,
            ValueError,
        ):
            return 0.0

    @classmethod
    def _total_volume(
        cls,
        broker_objects: list[Any],
    ) -> float:

        return sum(
            cls._volume(item)
            for item in broker_objects
        )

    @staticmethod
    def _volume_matches(
        expected: float,
        observed: float,
    ) -> bool:

        return abs(
            float(expected)
            - float(observed)
        ) < 1e-9

    @staticmethod
    def _is_rejected(
        execution_status: Any,
    ) -> bool:

        if execution_status is None:
            return False

        value = getattr(
            execution_status,
            "value",
            execution_status,
        )

        return str(value).upper() in {
            "FAILED",
            "REJECTED",
        }