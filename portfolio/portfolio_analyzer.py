"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_analyzer.py

Purpose:
    Analyzes the current trading portfolio and
    generates portfolio metrics.
"""

from __future__ import annotations

from portfolio.portfolio_models import (
    PortfolioContext,
    PortfolioMetrics,
)


class PortfolioAnalyzer:
    """
    Analyzes portfolio statistics.
    """

    def analyze(
        self,
        context: PortfolioContext,
    ) -> PortfolioMetrics:
        """
        Analyze the current portfolio.
        """

        floating_profit = sum(

            position.floating_profit

            for position in context.positions

            if position.floating_profit > 0

        )

        floating_loss = sum(

            position.floating_profit

            for position in context.positions

            if position.floating_profit < 0

        )

        used_margin = sum(

            position.volume

            for position in context.positions

        )

        gross_exposure = used_margin

        free_margin = (

            context.account_equity
            -
            used_margin

        )

        if used_margin > 0:

            margin_level = (

                context.account_equity
                /
                used_margin

            ) * 100

        else:

            margin_level = 0.0

        portfolio_heat = (

            gross_exposure
            /
            context.account_balance

        ) * 100 if context.account_balance > 0 else 0.0
        return PortfolioMetrics(

            balance=context.account_balance,

            equity=context.account_equity,

            floating_profit=floating_profit,

            floating_loss=floating_loss,

            used_margin=used_margin,

            free_margin=free_margin,

            margin_level=margin_level,

            portfolio_heat=portfolio_heat,

            open_positions=len(
                context.positions
            ),

            daily_pnl=0.0,

            weekly_pnl=0.0,

            monthly_pnl=0.0,

        )