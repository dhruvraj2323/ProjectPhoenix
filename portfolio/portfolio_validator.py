"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_validator.py

Purpose:
    Validates the current portfolio against configured risk limits
    and determines the appropriate portfolio-level decision.
"""

from __future__ import annotations

from dataclasses import dataclass

from portfolio.portfolio_models import (
    AllocationInfo,
    ExposureInfo,
    PortfolioContext,
    PortfolioDecisionType,
    PortfolioMetrics,
)


@dataclass
class PortfolioValidationResult:
    """
    Result returned by the Portfolio Validator.
    """

    decision: PortfolioDecisionType

    valid: bool

    reason: str


class PortfolioValidator:
    """
    Validates portfolio state against configured limits.
    """

    def validate(
        self,
        context: PortfolioContext,
        metrics: PortfolioMetrics,
        exposure: ExposureInfo,
        allocation: AllocationInfo,
        correlation_risk: float,
    ) -> PortfolioValidationResult:
        """
        Validate the portfolio.
        """

        limits = context.limits

        # --------------------------------------------------
        # Margin Protection
        # --------------------------------------------------

        if (
            metrics.margin_level > 0.0
            and metrics.margin_level < limits.min_margin_level
        ):
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.EMERGENCY_EXIT,
                valid=False,
                reason=(
                    f"Margin level {metrics.margin_level:.2f}% "
                    f"is below minimum "
                    f"{limits.min_margin_level:.2f}%."
                ),
            )

        # --------------------------------------------------
        # Drawdown Protection
        # --------------------------------------------------

        drawdown_percent = (
            abs(metrics.floating_loss)
            / metrics.balance
            * 100.0
            if metrics.balance > 0
            else 0.0
        )

        if drawdown_percent >= limits.max_drawdown_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.EMERGENCY_EXIT,
                valid=False,
                reason=(
                    f"Drawdown {drawdown_percent:.2f}% "
                    "exceeded allowed limit."
                ),
            )

        # --------------------------------------------------
        # Daily / Weekly / Monthly Loss
        # --------------------------------------------------

        daily_loss = self._loss_percent(
            metrics.daily_pnl,
            metrics.balance,
        )

        if daily_loss >= limits.daily_loss_limit_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.BLOCK_NEW_TRADE,
                valid=False,
                reason="Daily loss limit reached.",
            )

        weekly_loss = self._loss_percent(
            metrics.weekly_pnl,
            metrics.balance,
        )

        if weekly_loss >= limits.weekly_loss_limit_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.BLOCK_NEW_TRADE,
                valid=False,
                reason="Weekly loss limit reached.",
            )

        monthly_loss = self._loss_percent(
            metrics.monthly_pnl,
            metrics.balance,
        )

        if monthly_loss >= limits.monthly_loss_limit_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.BLOCK_NEW_TRADE,
                valid=False,
                reason="Monthly loss limit reached.",
            )

        # --------------------------------------------------
        # Open Positions
        # --------------------------------------------------

        if metrics.open_positions > limits.max_open_trades:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.REDUCE_POSITION,
                valid=False,
                reason="Too many open positions.",
            )

        # --------------------------------------------------
        # Portfolio Heat
        # --------------------------------------------------

        if metrics.portfolio_heat > limits.max_exposure_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.REDUCE_POSITION,
                valid=False,
                reason="Portfolio exposure too high.",
            )

        # --------------------------------------------------
        # Correlation
        # --------------------------------------------------

        if correlation_risk >= limits.max_correlation_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.LIMIT_POSITION,
                valid=False,
                reason="Correlation risk too high.",
            )

        # --------------------------------------------------
        # Capacity
        # --------------------------------------------------

        if metrics.open_positions == limits.max_open_trades:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.LIMIT_POSITION,
                valid=False,
                reason="Maximum open trades reached.",
            )

        # --------------------------------------------------
        # Approved
        # --------------------------------------------------

        return PortfolioValidationResult(
            decision=PortfolioDecisionType.APPROVE,
            valid=True,
            reason="Portfolio validation passed.",
        )

    @staticmethod
    def _loss_percent(
        pnl: float,
        balance: float,
    ) -> float:
        """
        Convert negative P/L to percentage.
        """

        if balance <= 0:
            return 0.0

        if pnl >= 0:
            return 0.0

        return abs(pnl) / balance * 100.0