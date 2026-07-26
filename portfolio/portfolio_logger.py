"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_logger.py

Purpose:
    Logs portfolio management decisions.
"""

from __future__ import annotations

from portfolio.portfolio_models import PortfolioDecision


class PortfolioLogger:
    """
    Logs Portfolio Engine decisions.
    """

    def log(
        self,
        decision: PortfolioDecision,
    ) -> None:
        """
        Log portfolio decision.
        """

        print("===== Portfolio Decision =====")

        print(
            f"Decision          : {decision.decision.value}"
        )

        print(
            f"Approved          : {decision.approved}"
        )

        print(
            f"Reason            : {decision.reason}"
        )

        print(
            f"Open Positions    : {decision.metrics.open_positions}"
        )

        print(
            f"Portfolio Heat    : {decision.metrics.portfolio_heat:.2f}%"
        )

        print(
            f"Margin Level      : {decision.metrics.margin_level:.2f}%"
        )

        print(
            f"Gross Exposure    : {decision.exposure.gross_exposure}"
        )

        print(
            f"Net Exposure      : {decision.exposure.net_exposure}"
        )

        print(
            f"Long Exposure     : {decision.exposure.long_exposure}"
        )

        print(
            f"Short Exposure    : {decision.exposure.short_exposure}"
        )

        print(
            f"Capital Used      : {decision.allocation.capital_used}"
        )

        print(
            f"Capital Available : {decision.allocation.capital_available}"
        )

        print(
            f"Allocation %      : {decision.allocation.allocation_percent:.2f}%"
        )

        print(
            f"Risk Used         : {decision.allocation.risk_used:.2f}%"
        )

        print(
            f"Risk Available    : {decision.allocation.risk_available:.2f}%"
        )

        print(
            f"Risk Score        : {decision.risk.risk_score:.2f}"
        )

        print(
            f"Drawdown          : {decision.risk.drawdown:.2f}%"
        )

        print(
            f"Margin Risk       : {decision.risk.margin_risk:.2f}%"
        )

        print(
            f"Correlation Risk  : {decision.risk.correlation_risk:.2f}%"
        )

        print(
            f"Concentration     : {decision.risk.concentration_risk:.2f}%"
        )