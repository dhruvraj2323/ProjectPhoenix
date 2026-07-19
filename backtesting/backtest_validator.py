"""
Project Phoenix
Milestone M16 - Backtesting Engine

Module:
    backtest_validator.py

Purpose:
    Validates backtesting statistics.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtesting.backtest_models import (
    BacktestStatistics,
)


@dataclass
class BacktestValidationResult:
    """
    Result returned by the Backtest Validator.
    """

    valid: bool

    reason: str


class BacktestValidator:
    """
    Validates backtesting results.
    """

    def validate(
        self,
        statistics: BacktestStatistics,
    ) -> BacktestValidationResult:
        """
        Validate backtesting statistics.
        """

        if statistics.total_trades <= 0:

            return BacktestValidationResult(

                valid=False,

                reason="No trades available.",

            )

        if not (

            0.0
            <= statistics.win_rate
            <= 100.0

        ):

            return BacktestValidationResult(

                valid=False,

                reason="Invalid win rate.",

            )

        if statistics.profit_factor < 0:

            return BacktestValidationResult(

                valid=False,

                reason="Invalid profit factor.",

            )

        if statistics.max_drawdown < 0:

            return BacktestValidationResult(

                valid=False,

                reason="Invalid drawdown.",

            )

        return BacktestValidationResult(

            valid=True,

            reason="Backtest validation passed.",

        )