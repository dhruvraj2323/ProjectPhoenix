"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_logger.py

Purpose:
    Logs portfolio management decisions.
"""

from __future__ import annotations

from portfolio.portfolio_models import (
    PortfolioDecision,
)


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
            f"Open Positions    : "
            f"{decision.metrics.open_positions}"
        )

        print(
            f"Portfolio Heat    : "
            f"{decision.metrics.portfolio_heat:.2f}%"
        )

        print(
            f"Margin Level      : "
            f"{decision.metrics.margin_level:.2f}%"
        )

        print(
            f"Gross Exposure    : "
            f"{decision.exposure.gross_exposure}"
        )

        print(
            f"Net Exposure      : "
            f"{decision.exposure.net_exposure}"
        )

        print(
            f"Capital Used      : "
            f"{decision.allocation.capital_used}"
        )

        print(
            f"Capital Available : "
            f"{decision.allocation.capital_available}"
        )

        print(
            f"Allocation %      : "
            f"{decision.allocation.allocation_percent:.2f}%"
        )