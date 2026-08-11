"""
=================================================
Project Phoenix
Risk Models
M36
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# --------------------------------------------------
# Risk Decision
# --------------------------------------------------


class RiskDecision(str, Enum):
    """
    Final risk decision.
    """

    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# --------------------------------------------------
# Risk Metrics
# --------------------------------------------------


@dataclass(slots=True)
class RiskMetrics:
    """
    Risk calculation metrics.
    """

    risk_percent: float = 0.0

    position_size: float = 0.0

    exposure: float = 0.0

    margin_required: float = 0.0

    drawdown: float = 0.0

    # ---------------------------------------------
    # Dynamic Risk Management (M59.7)
    # ---------------------------------------------

    stop_loss: float = 0.0

    take_profit: float = 0.0

    risk_reward: float = 2.0

    swing_high: float = 0.0

    swing_low: float = 0.0

# --------------------------------------------------
# Risk Result
# --------------------------------------------------


@dataclass(slots=True)
class RiskResult:
    """
    Final output of Risk Engine.
    """

    decision: RiskDecision = (
        RiskDecision.REJECTED
    )

    reason: str = ""

    metrics: RiskMetrics = field(
        default_factory=RiskMetrics,
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )   