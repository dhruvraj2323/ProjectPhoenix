"""
=================================================
Project Phoenix
Trade Logger
M59.1.6
=================================================
"""

from __future__ import annotations

import logging

from live_execution.trade_context import (
    TradeContext,
)


class TradeLogger:
    """
    Logs Live Trade Execution.
    """

    def __init__(
        self,
    ) -> None:

        self.logger = logging.getLogger(
            "ProjectPhoenix.LiveExecution"
        )

        if not self.logger.handlers:

            handler = logging.StreamHandler()

            formatter = logging.Formatter(

                "[%(levelname)s] %(message)s"

            )

            handler.setFormatter(
                formatter,
            )

            self.logger.addHandler(
                handler,
            )

            self.logger.setLevel(
                logging.INFO,
            )

    # --------------------------------------------------

    def log_request(
        self,
        context: TradeContext,
    ) -> None:
        """
        Log outgoing trade request.
        """

        request = context.trade_request

        if request is None:

            self.logger.warning(
                "Trade request is empty."
            )

            return

        self.logger.info(

            "Trade Request | "
            "Symbol=%s "
            "Side=%s "
            "Volume=%.2f",

            request.symbol,

            request.side.value,

            request.volume,

        )

    # --------------------------------------------------

    def log_response(
        self,
        context: TradeContext,
    ) -> None:
        """
        Log broker response.
        """

        response = context.trade_response

        if response is None:

            self.logger.warning(
                "Trade response is empty."
            )

            return

        self.logger.info(

            "Trade Response | "
            "Status=%s "
            "Ticket=%s "
            "Price=%.5f",

            response.status.value,

            response.ticket,

            response.executed_price,

        )

    # --------------------------------------------------

    def log_error(
        self,
        message: str,
    ) -> None:
        """
        Log execution error.
        """

        self.logger.error(
            message,
        )