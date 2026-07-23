"""
=================================================
Project Phoenix
Signal Logger
M34
=================================================
"""

from __future__ import annotations

import logging

from signal_engine.signal_context import (
    SignalContext,
)


class SignalLogger:
    """
    Logs Signal Engine execution.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            "SignalEngine"
        )

    def log_start(
        self,
        context: SignalContext,
    ) -> None:

        self.logger.info(
            "Signal Engine Started | "
            "Engine=%s Symbol=%s Timeframe=%s",
            context.engine_id,
            context.symbol,
            context.timeframe,
        )

    def log_finish(
        self,
        context: SignalContext,
    ) -> None:

        self.logger.info(
            "Signal Engine Finished | "
            "Signals=%d Completed=%s Failed=%s",
            context.get_signal_count(),
            context.completed,
            context.failed,
        )

    def log_failure(
        self,
        context: SignalContext,
    ) -> None:

        self.logger.error(
            "Signal Engine Failed | %s",
            context.reason,
        )