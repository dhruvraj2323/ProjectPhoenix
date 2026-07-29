"""
=================================================
Project Phoenix
System Integration
M39
=================================================
"""

from __future__ import annotations

import time

from trading_system.integration_logger import (
    IntegrationLogger,
)

from trading_system.integration_report import (
    IntegrationReport,
)

from trading_system.trading_context import (
    TradingContext,
)

from trading_system.trading_coordinator import (
    TradingCoordinator,
)


class TradingSystem:
    """
    Main entry point of Project Phoenix
    trading integration.
    """

    def __init__(
        self,
        coordinator: TradingCoordinator,
    ) -> None:

        self.coordinator = coordinator

        self.logger = IntegrationLogger()

    def execute(
        self,
        context: TradingContext,
    ) -> IntegrationReport:
        """
        Execute complete trading workflow.
        """

        start = time.perf_counter()

        self.logger.info(

            "TradingSystem",

            "Trading workflow started.",

        )

        result = self.coordinator.execute(
            context,
        )

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        report = IntegrationReport(

            trading_id=context.trading_id,

            symbol=context.symbol,

            timeframe=context.timeframe,

            strategy_name=context.strategy_name,

            ai_decision=context.ai_decision,

            risk_passed=context.risk_passed,

            order_id=context.order_id,

            approved=context.approved,

            rejected=context.rejected,

            decision=context.decision,

            reason=context.reason,

        )

        report.mark_completed(
            elapsed,
        )

        self.logger.info(

            "TradingSystem",

            "Trading workflow completed.",

        )

        return report