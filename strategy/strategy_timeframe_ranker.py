"""
=================================================
Project Phoenix
Strategy Timeframe Ranker
M52
=================================================
"""

from __future__ import annotations

from strategy.strategy_models import (
    TimeframeAnalysis,
)


class StrategyTimeframeRanker:
    """
    Ranks timeframe analyses based on
    frozen Project Phoenix priority.

    This module is responsible only
    for ordering and selecting
    timeframes.

    It never calculates scores.
    """

    # -----------------------------------------
    # Frozen Priority
    # -----------------------------------------

    PRIORITY = {

        "D1": 1,

        "H4": 2,

        "H1": 3,

        "M15": 4,

        "M5": 5,

        "M1": 6,

    }

    # -----------------------------------------
    # Rank Analyses
    # -----------------------------------------

    def rank(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> list[
        TimeframeAnalysis
    ]:
        """
        Return analyses ordered
        by timeframe priority.
        """

        return sorted(

            analyses,

            key=lambda analysis:

            self.PRIORITY.get(

                analysis.timeframe,

                999,

            ),

        )
        
    # --------------------------------------------------
    # Highest Priority
    # --------------------------------------------------

    def highest_priority(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> TimeframeAnalysis | None:
        """
        Return the highest-priority
        timeframe.
        """

        ranked = self.rank(
            analyses,
        )

        if not ranked:

            return None

        return ranked[0]

    # --------------------------------------------------
    # Execution Timeframe
    # --------------------------------------------------

    def execution_timeframe(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> TimeframeAnalysis | None:
        """
        Return M1 analysis.
        """

        return self.get_timeframe(

            analyses,

            "M1",

        )

    # --------------------------------------------------
    # Entry Timeframe
    # --------------------------------------------------

    def entry_timeframe(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> TimeframeAnalysis | None:
        """
        Return M5 analysis.
        """

        return self.get_timeframe(

            analyses,

            "M5",

        )

    # --------------------------------------------------
    # Primary Strategy
    # --------------------------------------------------

    def primary_timeframe(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> TimeframeAnalysis | None:
        """
        Return M15 analysis.
        """

        return self.get_timeframe(

            analyses,

            "M15",

        )

    # --------------------------------------------------
    # Trend
    # --------------------------------------------------

    def trend_timeframe(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> TimeframeAnalysis | None:
        """
        Return H1 analysis.
        """

        return self.get_timeframe(

            analyses,

            "H1",

        )

    # --------------------------------------------------
    # Major Trend
    # --------------------------------------------------

    def major_trend_timeframe(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> TimeframeAnalysis | None:
        """
        Return H4 analysis.
        """

        return self.get_timeframe(

            analyses,

            "H4",

        )

    # --------------------------------------------------
    # Market Bias
    # --------------------------------------------------

    def market_bias_timeframe(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> TimeframeAnalysis | None:
        """
        Return D1 analysis.
        """

        return self.get_timeframe(

            analyses,

            "D1",

        )

    # --------------------------------------------------
    # Generic Finder
    # --------------------------------------------------

    def get_timeframe(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
        timeframe: str,
    ) -> TimeframeAnalysis | None:
        """
        Return analysis for the
        requested timeframe.
        """

        for analysis in analyses:

            if (
                analysis.timeframe
                == timeframe
            ):

                return analysis

        return None

    # --------------------------------------------------
    # Priority Lookup
    # --------------------------------------------------

    def get_priority(
        self,
        timeframe: str,
    ) -> int:
        """
        Return frozen priority.
        """

        return self.PRIORITY.get(

            timeframe,

            999,

        )        