"""
=================================================
Project Phoenix
Pattern Logger
M33
=================================================
"""

from __future__ import annotations

import logging

from pattern_engine.pattern_context import (
    PatternContext,
)


class PatternLogger:
    """
    Logs Pattern Engine execution.
    """

    def __init__(self):

        self.logger = logging.getLogger(
            "PatternEngine"
        )

    def log_start(
        self,
        context: PatternContext,
    ) -> None:

        self.logger.info(
            "Pattern Engine Started | "
            "ID=%s Symbol=%s Timeframe=%s",
            context.engine_id,
            context.symbol,
            context.timeframe,
        )

    def log_complete(
        self,
        context: PatternContext,
    ) -> None:

        self.logger.info(
            "Pattern Engine Completed | "
            "Patterns=%d",
            len(context.patterns),
        )