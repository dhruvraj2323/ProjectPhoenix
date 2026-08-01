"""
=================================================
Project Phoenix
Strategy AI Memory
M53
=================================================
"""

from __future__ import annotations

from strategy.strategy_ai_models import (
    AILearningRecord,
    AIMemorySummary,
    AIMemoryType,
    AITradeSimilarity,
)

from strategy.strategy_models import (
    TradeSnapshot,
    TradeDirection,
)


class StrategyAIMemory:
    """
    AI Memory Manager.

    Responsibilities

    • Store completed trades

    • Store learning records

    • Retrieve historical trades

    • Search similar trades

    • Build memory summaries

    This module never performs
    learning or confidence calculation.
    """

    def __init__(
        self,
    ) -> None:

        self._trade_memory: list[
            TradeSnapshot
        ] = []

        self._learning_memory: list[
            AILearningRecord
        ] = []

    # --------------------------------------------------
    # Trade Memory
    # --------------------------------------------------

    def add_trade(
        self,
        trade: TradeSnapshot,
    ) -> None:
        """
        Store completed trade.
        """

        self._trade_memory.append(
            trade,
        )

    def get_trade(
        self,
        trade_id: str,
    ) -> TradeSnapshot | None:
        """
        Return single trade.
        """

        for trade in self._trade_memory:

            if trade.trade_id == trade_id:

                return trade

        return None

    def get_all_trades(
        self,
    ) -> list[
        TradeSnapshot
    ]:
        """
        Return all trades.
        """

        return list(
            self._trade_memory,
        )

    # --------------------------------------------------
    # Learning Records
    # --------------------------------------------------

    def add_learning_record(
        self,
        record: AILearningRecord,
    ) -> None:
        """
        Store learning record.
        """

        self._learning_memory.append(
            record,
        )

    def get_learning_records(
        self,
    ) -> list[
        AILearningRecord
    ]:
        """
        Return all learning records.
        """

        return list(
            self._learning_memory,
        )

    # --------------------------------------------------
    # Basic Statistics
    # --------------------------------------------------

    @property
    def total_trades(
        self,
    ) -> int:

        return len(
            self._trade_memory,
        )

    @property
    def total_learning_records(
        self,
    ) -> int:

        return len(
            self._learning_memory,
        )

    # --------------------------------------------------
    # Similarity Search
    # --------------------------------------------------

    def find_similar_trades(
        self,
        trade: TradeSnapshot,
        limit: int = 10,
    ) -> list[
        AITradeSimilarity
    ]:
        """
        Search historical trades
        with similar characteristics.
        """

        similarities: list[
            AITradeSimilarity
        ] = []

        for historical in self._trade_memory:

            if (
                historical.trade_id
                == trade.trade_id
            ):
                continue

            score = 0.0

            if (
                historical.strategy_id
                == trade.strategy_id
            ):
                score += 30.0

            if (
                historical.direction
                == trade.direction
            ):
                score += 25.0

            if (
                historical.timeframe
                == trade.timeframe
            ):
                score += 15.0

            pattern_gap = abs(
                historical.pattern_score
                - trade.pattern_score
            )

            indicator_gap = abs(
                historical.indicator_score
                - trade.indicator_score
            )

            alignment_gap = abs(
                historical.alignment_score
                - trade.alignment_score
            )

            score += max(
                0.0,
                15.0 - pattern_gap,
            )

            score += max(
                0.0,
                10.0 - indicator_gap,
            )

            score += max(
                0.0,
                5.0 - alignment_gap,
            )

            similarity = AITradeSimilarity(

                trade_id=historical.trade_id,

                similarity_score=round(
                    score,
                    2,
                ),

                historical_win_rate=(
                    100.0
                    if historical.win
                    else 0.0
                ),

                confidence=(
                    historical.ai_confidence
                ),

                matched_patterns=int(
                    pattern_gap < 5.0
                ),

                matched_indicators=int(
                    indicator_gap < 5.0
                ),

                matched_timeframes=int(
                    historical.timeframe
                    == trade.timeframe
                ),

                direction=(
                    historical.direction
                ),

                reason="Historical similarity",
            )

            similarities.append(
                similarity,
            )

        similarities.sort(

            key=lambda item: (
                item.similarity_score
            ),

            reverse=True,

        )

        return similarities[
            :limit
        ]

    # --------------------------------------------------
    # Memory Summary
    # --------------------------------------------------

    def build_memory_summary(
        self,
        memory_type: AIMemoryType,
    ) -> AIMemorySummary:
        """
        Build AI memory summary.
        """

        trades = self._trade_memory

        total = len(
            trades,
        )

        if total == 0:

            return AIMemorySummary(

                memory_type=memory_type,

            )

        winning = sum(

            1

            for trade in trades

            if trade.win

        )

        losing = total - winning

        average_profit = sum(

            trade.pnl

            for trade in trades

        ) / total

        average_confidence = sum(

            trade.ai_confidence

            for trade in trades

        ) / total

        win_rate = (

            winning
            / total

        ) * 100.0

        return AIMemorySummary(

            memory_type=memory_type,

            total_records=total,

            winning_records=winning,

            losing_records=losing,

            average_similarity=0.0,

            average_confidence=round(
                average_confidence,
                2,
            ),

            average_profit=round(
                average_profit,
                2,
            ),

            win_rate=round(
                win_rate,
                2,
            ),

        )

    # --------------------------------------------------
    # Memory Maintenance
    # --------------------------------------------------

    def clear_short_term_memory(
        self,
        keep_last: int = 50,
    ) -> None:
        """
        Keep only the most recent trades
        in short-term memory.
        """

        if keep_last <= 0:

            self._trade_memory.clear()

            return

        self._trade_memory = (
            self._trade_memory[
                -keep_last:
            ]
        )

    def archive_memory(
        self,
    ) -> list[
        TradeSnapshot
    ]:
        """
        Return a snapshot of the current
        trade memory.

        Future versions will archive
        records into SQLite or PostgreSQL.
        """

        return list(
            self._trade_memory,
        )

    # --------------------------------------------------
    # Export Learning Data
    # --------------------------------------------------

    def export_learning_records(
        self,
    ) -> list[
        AILearningRecord
    ]:
        """
        Export all learning records.
        """

        return list(
            self._learning_memory,
        )

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def has_trade(
        self,
        trade_id: str,
    ) -> bool:
        """
        Check whether a trade exists.
        """

        return any(

            trade.trade_id == trade_id

            for trade in self._trade_memory

        )

    def remove_trade(
        self,
        trade_id: str,
    ) -> bool:
        """
        Remove a trade from memory.

        Returns True if removed.
        """

        for index, trade in enumerate(
            self._trade_memory,
        ):

            if trade.trade_id == trade_id:

                del self._trade_memory[
                    index
                ]

                return True

        return False

    def reset(
        self,
    ) -> None:
        """
        Reset complete AI memory.
        """

        self._trade_memory.clear()

        self._learning_memory.clear()