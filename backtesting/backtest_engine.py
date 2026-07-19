"""
Project Phoenix
Milestone M16 - Backtesting Engine

Module:
    backtest_engine.py

Purpose:
    Coordinates the complete Backtesting Engine.
"""

from __future__ import annotations

from backtesting.backtest_models import (
    BacktestContext,
    BacktestDecision,
    BacktestStatus,
)

from backtesting.backtest_simulator import (
    BacktestSimulator,
)

from backtesting.backtest_statistics import (
    BacktestStatisticsCalculator,
)

from backtesting.backtest_validator import (
    BacktestValidator,
)

from backtesting.backtest_logger import (
    BacktestLogger,
)


class BacktestEngine:
    """
    Coordinates the complete
    Backtesting Engine.
    """

    def __init__(self) -> None:

        self.simulator = (
            BacktestSimulator()
        )

        self.statistics = (
            BacktestStatisticsCalculator()
        )

        self.validator = (
            BacktestValidator()
        )

        self.logger = (
            BacktestLogger()
        )

    def run(
        self,
        context: BacktestContext,
    ) -> BacktestDecision:
        """
        Execute complete backtest workflow.
        """

        trades = self.simulator.simulate(
            context
        )

        statistics = (
            self.statistics.calculate(
                trades
            )
        )

        validation = (
            self.validator.validate(
                statistics
            )
        )

        decision = BacktestDecision(

            status=(

                BacktestStatus.APPROVED

                if validation.valid

                else

                BacktestStatus.REJECTED

            ),

            statistics=statistics,

            approved=validation.valid,

            reason=validation.reason,

        )

        self.logger.log(
            decision
        )

        return decision