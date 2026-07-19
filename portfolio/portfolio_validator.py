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
    Validates portfolio state against configured limits and produces
    the final portfolio decision.

    Checks are ordered from most to least severe. The first violated
    rule determines the resulting decision.
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
        Validate the portfolio and return the resulting decision.
        """

        limits = context.limits

        # ----- 1. Margin safety (most severe -> EMERGENCY_EXIT) -----

        if (
            metrics.margin_level > 0.0
            and metrics.margin_level < limits.min_margin_level
        ):
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.EMERGENCY_EXIT,
                valid=False,
                reason=(
                    f"Margin level {metrics.margin_level:.2f}% is below "
                    f"the minimum safe level of "
                    f"{limits.min_margin_level:.2f}%."
                ),
            )

        # ----- 2. Floating drawdown -> EMERGENCY_EXIT -----

        drawdown_percent = (
            (abs(metrics.floating_loss) / metrics.balance * 100.0)
            if metrics.balance > 0
            else 0.0
        )

        if drawdown_percent >= limits.max_drawdown_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.EMERGENCY_EXIT,
                valid=False,
                reason=(
                    f"Floating drawdown {drawdown_percent:.2f}% has "
                    f"reached the maximum allowed "
                    f"{limits.max_drawdown_percent:.2f}%."
                ),
            )

        # ----- 3. Daily / Weekly / Monthly loss limits -> BLOCK_NEW_TRADE -----

        daily_loss_percent = self._loss_percent(
            metrics.daily_pnl, metrics.balance
        )

        if daily_loss_percent >= limits.daily_loss_limit_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.BLOCK_NEW_TRADE,
                valid=False,
                reason=(
                    f"Daily loss {daily_loss_percent:.2f}% has reached "
                    f"the daily loss limit of "
                    f"{limits.daily_loss_limit_percent:.2f}%."
                ),
            )

        weekly_loss_percent = self._loss_percent(
            metrics.weekly_pnl, metrics.balance
        )

        if weekly_loss_percent >= limits.weekly_loss_limit_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.BLOCK_NEW_TRADE,
                valid=False,
                reason=(
                    f"Weekly loss {weekly_loss_percent:.2f}% has reached "
                    f"the weekly loss limit of "
                    f"{limits.weekly_loss_limit_percent:.2f}%."
                ),
            )

        monthly_loss_percent = self._loss_percent(
            metrics.monthly_pnl, metrics.balance
        )

        if monthly_loss_percent >= limits.monthly_loss_limit_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.BLOCK_NEW_TRADE,
                valid=False,
                reason=(
                    f"Monthly loss {monthly_loss_percent:.2f}% has "
                    f"reached the monthly loss limit of "
                    f"{limits.monthly_loss_limit_percent:.2f}%."
                ),
            )

        # ----- 4. Open trade count / exposure -> REDUCE_POSITION -----

        if metrics.open_positions > limits.max_open_trades:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.REDUCE_POSITION,
                valid=False,
                reason=(
                    f"Open positions ({metrics.open_positions}) exceed "
                    f"the maximum allowed ({limits.max_open_trades})."
                ),
            )

        if metrics.portfolio_heat > limits.max_exposure_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.REDUCE_POSITION,
                valid=False,
                reason=(
                    f"Portfolio heat {metrics.portfolio_heat:.2f}% "
                    f"exceeds the maximum allowed "
                    f"{limits.max_exposure_percent:.2f}%."
                ),
            )

        # ----- 5. Correlation / capacity -> LIMIT_POSITION -----

        if correlation_risk >= limits.max_correlation_percent:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.LIMIT_POSITION,
                valid=False,
                reason=(
                    f"Correlation risk {correlation_risk:.2f}% has "
                    f"reached the maximum allowed "
                    f"{limits.max_correlation_percent:.2f}%. "
                    f"New trades are limited."
                ),
            )

        if metrics.open_positions == limits.max_open_trades:
            return PortfolioValidationResult(
                decision=PortfolioDecisionType.LIMIT_POSITION,
                valid=False,
                reason=(
                    "Portfolio is at maximum open trade capacity. "
                    "New trades are limited."
                ),
            )

        # ----- 6. All checks passed -----

        return PortfolioValidationResult(
            decision=PortfolioDecisionType.APPROVE,
            valid=True,
            reason="Portfolio validation passed.",
        )

    def _loss_percent(self, pnl: float, balance: float) -> float:
        """
        Convert a negative P/L figure into a positive loss percentage
        of account balance. Returns 0.0 when P/L is non-negative.
        """

        if balance <= 0 or pnl >= 0:
            return 0.0

        return abs(pnl) / balance * 100.0