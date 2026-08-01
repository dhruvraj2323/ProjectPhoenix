"""
=================================================
Project Phoenix
Strategy Signal Builder
M51
=================================================
"""

from __future__ import annotations

from strategy.strategy_models import (
    StrategySignal,
    StrategyType,
    TradeDirection,
)


class StrategySignalBuilder:
    """
    Builds StrategySignal objects.

    Responsibility:

    • Build StrategySignal

    • Populate intelligence fields

    • Return fully initialized signal

    The builder never decides
    BUY or SELL.
    """

    def build(
        self,
        strategy_id: str,
        strategy_name: StrategyType,
        direction: TradeDirection,
        entry_price: float,
        stop_loss: float,
        take_profit: float,
        risk_percent: float,
        reason: str,
        strategy_score: float,
        pattern_score: float,
        indicator_score: float,
        confirmation_score: float,
        confidence: float,
        rank: int = 0,
        selected: bool = False,
    ) -> StrategySignal:
        """
        Build complete strategy signal.
        """

        signal = StrategySignal(

            strategy_id=strategy_id,

            strategy_name=strategy_name,

            direction=direction,

            confidence=confidence,

            entry_price=entry_price,

            stop_loss=stop_loss,

            take_profit=take_profit,

            risk_percent=risk_percent,

            reason=reason,

        )

        signal.strategy_score = (
            strategy_score
        )

        signal.pattern_score = (
            pattern_score
        )

        signal.indicator_score = (
            indicator_score
        )

        signal.confirmation_score = (
            confirmation_score
        )

        signal.rank = rank

        signal.selected = selected

        return signal