"""
=================================================
Project Phoenix
Paper Trading Engine
M54
=================================================
"""

from __future__ import annotations

from paper_trading.order_manager import (
    OrderManager,
)

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_logger import (
    PaperLogger,
)

from paper_trading.paper_validator import (
    PaperValidator,
)

from paper_trading.position_manager import (
    PositionManager,
)

from paper_trading.portfolio_sync import (
    PortfolioSync,
)

from paper_trading.trade_manager import (
    TradeManager,
)


class PaperTradingEngine:
    """
    Executes the complete
    Paper Trading workflow.
    """

    def __init__(
        self,
    ) -> None:

        self.validator = (
            PaperValidator()
        )

        self.order_manager = (
            OrderManager()
        )

        self.position_manager = (
            PositionManager()
        )

        self.trade_manager = (
            TradeManager()
        )

        self.portfolio_sync = (
            PortfolioSync()
        )

        self.logger = (
            PaperLogger()
        )

    # --------------------------------------------------
    # Run Engine
    # --------------------------------------------------

    def run(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Execute complete
        Paper Trading Engine.
        """

        self.logger.log_start(
            context,
        )

        if not self.validator.validate(
            context,
        ):

            self.logger.log_failure(
                context,
            )

            return context

        # ------------------------------------
        # Create Paper Order
        # ------------------------------------

        context = (
            self.order_manager.create_order(
                context,
            )
        )

        context = (
            self.order_manager.update_context(
                context,
            )
        )

        # ------------------------------------
        # Open Position
        # ------------------------------------

        context = (
            self.position_manager.open_position(
                context,
            )
        )

        context = (
            self.position_manager.update_context(
                context,
            )
        )

        # ------------------------------------
        # Close Trade
        # ------------------------------------

        context = (
            self.trade_manager.close_trade(
                context,
            )
        )

        context = (
            self.trade_manager.update_context(
                context,
            )
        )

        # ------------------------------------
        # Synchronize Portfolio
        # ------------------------------------

        context = (
            self.portfolio_sync.synchronize(
                context,
            )
        )

        context = (
            self.portfolio_sync.update_statistics(
                context,
            )
        )

        # ------------------------------------
        # Complete
        # ------------------------------------

        context.complete()

        self.logger.log_finish(
            context,
        )

        return context