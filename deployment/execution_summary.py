"""
=================================================
Project Phoenix
Execution Summary
M61.3
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# =================================================
# Symbol Execution Status
# =================================================

class SymbolExecutionStatus(str, Enum):
    """
    Final execution outcome for one symbol.
    """

    EXECUTED = "EXECUTED"

    NO_TRADE = "NO_TRADE"

    FAILED = "FAILED"


# =================================================
# Cycle Execution Status
# =================================================

class CycleExecutionStatus(str, Enum):
    """
    Final execution outcome for the complete
    multi-symbol trading cycle.
    """

    ALL_EXECUTED = "ALL_EXECUTED"

    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"

    NO_TRADES = "NO_TRADES"

    ALL_FAILED = "ALL_FAILED"


# =================================================
# Symbol Execution Result
# =================================================

@dataclass(slots=True)
class SymbolExecutionResult:
    """
    Execution outcome for one configured symbol.
    """

    symbol: str = ""

    status: SymbolExecutionStatus = (
        SymbolExecutionStatus.NO_TRADE
    )

    trade_id: str = ""

    error: str = ""


# =================================================
# Cycle Execution Summary
# =================================================

@dataclass(slots=True)
class CycleExecutionSummary:
    """
    Consolidated execution outcome for one
    complete multi-symbol trading cycle.
    """

    total_symbols: int = 0

    executed_symbols: int = 0

    no_trade_symbols: int = 0

    failed_symbols: int = 0

    status: CycleExecutionStatus = (
        CycleExecutionStatus.NO_TRADES
    )

    symbol_results: list[
        SymbolExecutionResult
    ] = field(
        default_factory=list,
    )

    # -------------------------------------------------
    # Add Symbol Result
    # -------------------------------------------------

    def add_result(
        self,
        result: SymbolExecutionResult,
    ) -> None:
        """
        Add one symbol execution result.
        """

        self.symbol_results.append(
            result
        )

        self._recalculate()

    # -------------------------------------------------
    # Recalculate
    # -------------------------------------------------

    def _recalculate(
        self,
    ) -> None:
        """
        Recalculate cycle-level counters and
        final execution status.
        """

        self.total_symbols = (
            len(self.symbol_results)
        )

        self.executed_symbols = sum(
            1
            for result in self.symbol_results
            if result.status
            == SymbolExecutionStatus.EXECUTED
        )

        self.no_trade_symbols = sum(
            1
            for result in self.symbol_results
            if result.status
            == SymbolExecutionStatus.NO_TRADE
        )

        self.failed_symbols = sum(
            1
            for result in self.symbol_results
            if result.status
            == SymbolExecutionStatus.FAILED
        )

        # -------------------------------------------------
        # No Symbols
        # -------------------------------------------------

        if self.total_symbols == 0:

            self.status = (
                CycleExecutionStatus.NO_TRADES
            )

            return

        # -------------------------------------------------
        # All Executed
        # -------------------------------------------------

        if (
            self.executed_symbols
            == self.total_symbols
        ):

            self.status = (
                CycleExecutionStatus.ALL_EXECUTED
            )

            return

        # -------------------------------------------------
        # All Failed
        # -------------------------------------------------

        if (
            self.failed_symbols
            == self.total_symbols
        ):

            self.status = (
                CycleExecutionStatus.ALL_FAILED
            )

            return

        # -------------------------------------------------
        # No Trades
        # -------------------------------------------------

        if (
            self.executed_symbols == 0
            and self.failed_symbols == 0
        ):

            self.status = (
                CycleExecutionStatus.NO_TRADES
            )

            return

        # -------------------------------------------------
        # Partial Success
        # -------------------------------------------------

        self.status = (
            CycleExecutionStatus.PARTIAL_SUCCESS
        )