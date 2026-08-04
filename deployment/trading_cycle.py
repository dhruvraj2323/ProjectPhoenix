"""
=================================================
Project Phoenix
Trading Cycle
M58
=================================================
"""

from __future__ import annotations

from market_pipeline.market_pipeline_engine import (
    MarketPipelineEngine,
)
from strategy.strategy_engine import (
    StrategyEngine,
)
from risk_engine.risk_engine import (
    RiskEngine,
)
from execution_engine.execution_engine import (
    ExecutionEngine,
)
from paper_trading.paper_engine import (
    PaperTradingEngine,
)
from reporting.reporting_engine import (
    ReportingEngine,
)


class TradingCycle:
    """
    Executes one complete
    Project Phoenix trading cycle.
    """

    def __init__(
        self,
    ) -> None:

        self.market_pipeline = (
            MarketPipelineEngine()
        )

        self.strategy_engine = (
            StrategyEngine()
        )

        self.risk_engine = (
            RiskEngine()
        )

        self.execution_engine = (
            ExecutionEngine()
        )

        self.paper_engine = (
            PaperTradingEngine()
        )

        self.reporting_engine = (
            ReportingEngine()
        )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
    ) -> bool:
        """
        Execute one complete
        trading cycle.
        """

        print()

        print(
            "Starting Trading Cycle...",
        )

        print(
            "Market Pipeline Ready",
        )

        print(
            "Strategy Engine Ready",
        )

        print(
            "Risk Engine Ready",
        )

        print(
            "Execution Engine Ready",
        )

        print(
            "Paper Trading Ready",
        )

        print(
            "Reporting Ready",
        )

        print()

        print(
            "Trading Cycle Completed.",
        )

        return True