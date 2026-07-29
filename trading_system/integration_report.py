"""
=================================================
Project Phoenix
Integration Report
M39
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class IntegrationReport:
    """
    Final report of one trading integration run.
    """

    session_id: str = ""

    trading_id: str = ""

    symbol: str = ""

    timeframe: str = ""

    strategy_name: str = ""

    ai_decision: str = ""

    risk_passed: bool = False

    order_id: str = ""

    approved: bool = False

    rejected: bool = False

    decision: str = ""

    reason: str = ""

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    finished_at: datetime = field(
        default_factory=datetime.utcnow
    )

    processing_time_ms: float = 0.0

    def mark_completed(
        self,
        processing_time_ms: float,
    ) -> None:
        """
        Mark report as completed.
        """

        self.processing_time_ms = processing_time_ms

        self.finished_at = datetime.utcnow()

    def summary(
        self,
    ) -> dict:
        """
        Return report summary.
        """

        return {

            "session_id": self.session_id,

            "trading_id": self.trading_id,

            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "strategy_name": self.strategy_name,

            "ai_decision": self.ai_decision,

            "risk_passed": self.risk_passed,

            "order_id": self.order_id,

            "approved": self.approved,

            "rejected": self.rejected,

            "decision": self.decision,

            "reason": self.reason,

            "processing_time_ms": self.processing_time_ms,

        }