"""
=================================================
Project Phoenix
Strategy Context
M52
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from strategy.strategy_models import (
    StrategyResult,
    MultiTimeframeResult,
)


@dataclass(slots=True)
class StrategyContext:
    """
    Shared runtime context for Strategy Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    engine_id: str

    symbol: str

    timeframe: str

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    # --------------------------------------------------
    # Input Data
    # --------------------------------------------------

    indicators: dict[str, Any] = field(
        default_factory=dict,
    )

    patterns: list[dict[str, Any]] = field(
        default_factory=list,
    )

    market_data: dict[str, Any] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # M51 Strategy Intelligence
    # --------------------------------------------------

    pattern_score: float = 0.0

    indicator_score: float = 0.0

    confirmation_score: float = 0.0

    strategy_score: float = 0.0

    selected_strategy_rank: int = 0

    # --------------------------------------------------
    # M52 Multi-Timeframe Intelligence
    # --------------------------------------------------

    primary_timeframe: str = "M15"

    execution_timeframe: str = "M1"

    entry_timeframe: str = "M5"

    trend_timeframe: str = "H1"

    major_trend_timeframe: str = "H4"

    market_bias_timeframe: str = "D1"

    alignment_score: float = 0.0

    multi_timeframe_score: float = 0.0

    market_bias: str = "NONE"

    timeframe_scores: dict[
        str,
        float,
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Strategy Result
    # --------------------------------------------------

    strategy_result: StrategyResult = field(
        default_factory=StrategyResult,
    )

    multi_timeframe_result: MultiTimeframeResult = field(
        default_factory=MultiTimeframeResult,
    )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    strategy_candidates: list[
        dict[str, Any]
    ] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Runtime State
    # --------------------------------------------------

    completed: bool = False

    failed: bool = False

    reason: str = ""

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def complete(
        self,
    ) -> None:

        self.completed = True

        self.failed = False

    def fail(
        self,
        reason: str,
    ) -> None:

        self.completed = False

        self.failed = True

        self.reason = reason

    def reset(
        self,
    ) -> None:

        self.strategy_result = (
            StrategyResult()
        )

        self.multi_timeframe_result = (
            MultiTimeframeResult()
        )

        self.metadata.clear()

        self.pattern_score = 0.0

        self.indicator_score = 0.0

        self.confirmation_score = 0.0

        self.strategy_score = 0.0

        self.alignment_score = 0.0

        self.multi_timeframe_score = 0.0

        self.market_bias = "NONE"

        self.selected_strategy_rank = 0

        self.timeframe_scores.clear()

        self.strategy_candidates.clear()

        self.completed = False

        self.failed = False

        self.reason = ""