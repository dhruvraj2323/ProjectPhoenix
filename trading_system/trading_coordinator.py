"""
=================================================
Project Phoenix
Trading Coordinator
M39
=================================================
"""

from __future__ import annotations

from trading_system.engine_contracts import (
    MarketPipelineContract,
    StrategyEngineContract,
    RiskEngineContract,
    AIDecisionContract,
    ExecutionEngineContract,
    PaperTradingContract,
)

from trading_system.trading_context import (
    TradingContext,
)


class TradingCoordinator:
    """
    Coordinates complete trading workflow.
    """

    def __init__(
        self,
        market_pipeline: MarketPipelineContract,
        strategy_engine: StrategyEngineContract,
        risk_engine: RiskEngineContract,
        ai_engine: AIDecisionContract,
        execution_engine: ExecutionEngineContract,
        paper_engine: PaperTradingContract,
    ) -> None:

        self.market_pipeline = market_pipeline

        self.strategy_engine = strategy_engine

        self.risk_engine = risk_engine

        self.ai_engine = ai_engine

        self.execution_engine = execution_engine

        self.paper_engine = paper_engine

    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute complete trading flow.
        """

        engines = [

            self.market_pipeline,

            self.strategy_engine,

            self.risk_engine,

            self.ai_engine,

            self.execution_engine,

            self.paper_engine,

        ]

        for engine in engines:

            context = engine.execute(
                context
            )

            if context.rejected:

                break

        return context