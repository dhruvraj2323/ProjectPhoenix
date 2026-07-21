"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_engine.py

Purpose:
    Coordinates the complete Portfolio
    Management Engine.
"""

from __future__ import annotations

from portfolio.portfolio_analyzer import (
    PortfolioAnalyzer,
)
from portfolio.portfolio_allocator import (
    PortfolioAllocator,
)
from portfolio.portfolio_exposure import (
    PortfolioExposure,
)
from portfolio.portfolio_correlation import (
    PortfolioCorrelation,
)
from portfolio.portfolio_logger import (
    PortfolioLogger,
)
from portfolio.portfolio_models import (
    PortfolioContext,
    PortfolioDecision,
    PortfolioRisk,
)
from portfolio.portfolio_validator import (
    PortfolioValidator,
)


class PortfolioEngine:
    """
    Coordinates the complete Portfolio
    Management Engine.
    """

    def __init__(self) -> None:

        self.analyzer = PortfolioAnalyzer()

        self.allocator = PortfolioAllocator()

        self.exposure = PortfolioExposure()

        self.correlation = PortfolioCorrelation()

        self.validator = PortfolioValidator()

        self.logger = PortfolioLogger()

    def evaluate(
        self,
        context: PortfolioContext,
    ) -> PortfolioDecision:
        """
        Execute complete portfolio workflow.
        """

        metrics = self.analyzer.analyze(
            context
        )

        allocation = self.allocator.allocate(

            total_capital=context.account_balance,

            positions=context.positions,

            free_margin=metrics.free_margin,

        )

        exposure = self.exposure.calculate(
            context
        )

        correlation_risk = self.correlation.calculate(
            context
        )

        validation = self.validator.validate(
            context=context,
            metrics=metrics,
            exposure=exposure,
            allocation=allocation,
            correlation_risk=correlation_risk,
        )

        drawdown_percent = (
            (abs(metrics.floating_loss) / metrics.balance * 100.0)
            if metrics.balance > 0
            else 0.0
        )

        margin_risk = (
            max(0.0, context.limits.min_margin_level - metrics.margin_level)
            if metrics.margin_level > 0
            else 0.0
        )

        total_symbol_exposure = sum(exposure.symbol_exposure.values())

        concentration_risk = (
            (max(exposure.symbol_exposure.values()) / total_symbol_exposure * 100.0)
            if total_symbol_exposure > 0
            else 0.0
        )

        risk = PortfolioRisk(
            risk_score=(
                drawdown_percent
                + margin_risk
                + correlation_risk
                + concentration_risk
            ) / 4.0,
            drawdown=drawdown_percent,
            margin_risk=margin_risk,
            correlation_risk=correlation_risk,
            concentration_risk=concentration_risk,
        )

        decision = PortfolioDecision(

            decision=validation.decision,

            metrics=metrics,

            exposure=exposure,

            allocation=allocation,

            risk=risk,

            approved=validation.valid,

            reason=validation.reason,
        )

        self.logger.log(
            decision
        )

        return decision