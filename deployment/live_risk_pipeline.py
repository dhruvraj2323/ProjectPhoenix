"""
=================================================
Project Phoenix
Live Risk Pipeline
M58.12.7
=================================================
"""

from __future__ import annotations

from deployment.live_strategy_pipeline import (
    LiveStrategyPipeline,
)

from risk_engine.risk_context import (
    RiskContext,
)

from risk_engine.risk_engine import (
    RiskEngine,
)


class LiveRiskPipeline:
    """
    Executes the Strategy Engine followed by the
    Risk Engine using live MT5 market data.
    """

    def __init__(
        self,
    ) -> None:

        self.strategy = LiveStrategyPipeline()

        self.risk = RiskEngine()

    # --------------------------------------------------

    def execute(
        self,
        symbol: str,
        timeframe: str = "M15",
        bars: int = 500,
        account_id: str = "DEMO-001",
        balance: float = 10000.0,
        equity: float = 10000.0,
        free_margin: float = 10000.0,
    ) -> RiskContext | None:

        strategy_context = self.strategy.execute(

            symbol=symbol,

            timeframe=timeframe,

            bars=bars,

        )

        if strategy_context is None:

            return None

        context = RiskContext(

            engine_id="LIVE-RISK",

            account_id=account_id,

            balance=balance,

            equity=equity,

            free_margin=free_margin,

        )

        context.metadata["strategy_context"] = (
            strategy_context
        )

        return self.risk.run(
            context
        )