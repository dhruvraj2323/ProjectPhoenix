"""
=================================================
Project Phoenix
Live Strategy Pipeline
M58.12.6
=================================================
"""

from __future__ import annotations

from deployment.live_market_data import (
    LiveMarketData,
)

from deployment.market_data_adapter import (
    MarketDataAdapter,
)

from indicator_engine.indicator_context import (
    IndicatorContext,
)

from indicator_engine.indicator_engine import (
    IndicatorEngine,
)

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_engine import (
    PatternEngine,
)

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_engine import (
    StrategyEngine,
)


class LiveStrategyPipeline:

    def __init__(
        self,
    ) -> None:

        self.market = LiveMarketData()

        self.adapter = MarketDataAdapter()

        self.indicator = IndicatorEngine()

        self.pattern = PatternEngine()

        self.strategy = StrategyEngine()

    # --------------------------------------------------

    def execute(
        self,
        symbol: str,
        timeframe: str = "M15",
        bars: int = 500,
    ) -> StrategyContext | None:

        if not self.market.connect():

            return None

        try:

            candles = self.market.get_candles(

                symbol,

                timeframe,

                bars,

            )

            candles = self.adapter.normalize(
                candles
            )

            # -----------------------------
            # Indicator Engine
            # -----------------------------

            indicator_context = IndicatorContext(

                engine_id="LIVE-IND",

                symbol=symbol,

                timeframe=timeframe,

            )

            indicator_context.candles = candles

            indicator_context = self.indicator.run(
                indicator_context
            )

            # -----------------------------
            # Pattern Engine
            # -----------------------------

            pattern_context = PatternContext(

                engine_id="LIVE-PATTERN",

                symbol=symbol,

                timeframe=timeframe,

            )

            pattern_context.candles = candles

            pattern_context = self.pattern.run(
                pattern_context
            )

            # -----------------------------
            # Strategy Engine
            # -----------------------------

            strategy_context = StrategyContext(

                engine_id="LIVE-STRATEGY",

                symbol=symbol,

                timeframe=timeframe,

            )

            strategy_context.indicators = (
                indicator_context.indicators
            )

            strategy_context.patterns = (
                pattern_context.patterns
            )

            strategy_context.market_data = {

                "price": candles[-1]["close"]

            }

            return self.strategy.run(
                strategy_context
            )

        finally:

            self.market.disconnect()