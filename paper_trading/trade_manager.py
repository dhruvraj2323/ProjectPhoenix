"""
=================================================
Project Phoenix
Trade Manager
M54
=================================================
"""

from __future__ import annotations

from uuid import uuid4

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_models import (
    PaperTrade,
    TradeStatus,
)


class TradeManager:
    """
    Creates and manages
    completed paper trades.
    """

    # --------------------------------------------------
    # Close Trade
    # --------------------------------------------------

    def close_trade(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Create completed trade
        from an open position.
        """

        if context.position is None:

            return context

        profit = (
            context.market_price
            - context.position.entry_price
        ) * context.position.volume

        trade = PaperTrade(

            trade_id=(
                self._generate_trade_id()
            ),

            position_id=(
                context.position.position_id
            ),

            symbol=(
                context.position.symbol
            ),

            direction=(
                context.position.direction
            ),

            volume=(
                context.position.volume
            ),

            entry_price=(
                context.position.entry_price
            ),

            exit_price=(
                context.market_price
            ),

            profit_loss=profit,

            win=profit >= 0.0,

            status=TradeStatus.COMPLETED,

        )

        context.trade = trade

        return context

    # --------------------------------------------------
    # Generate Trade ID
    # --------------------------------------------------

    def _generate_trade_id(
        self,
    ) -> str:
        """
        Generate unique paper
        trade ID.
        """

        return (
            f"TRADE-{uuid4().hex[:12].upper()}"
        )

    # --------------------------------------------------
    # Update Context
    # --------------------------------------------------

    def update_context(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Synchronize completed trade
        into PaperContext.
        """

        if context.trade is not None:

            context.result.trade = (
                context.trade
            )

            stats = context.statistics

            stats.total_trades += 1

            if context.trade.win:

                stats.winning_trades += 1

            else:

                stats.losing_trades += 1

            stats.net_profit += (
                context.trade.profit_loss
            )

            total = stats.total_trades

            if total > 0:

                stats.win_rate = (
                    stats.winning_trades
                    / total
                ) * 100.0

            context.set_metadata(
                "trade_id",
                context.trade.trade_id,
            )

            context.set_metadata(
                "trade_status",
                context.trade.status.value,
            )

        return context        