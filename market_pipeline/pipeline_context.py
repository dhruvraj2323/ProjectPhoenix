"""
=================================================
Project Phoenix
Market Pipeline Context
M31 — Integration Pipeline
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class PipelineContext:
    """
    Shared runtime context passed through every stage
    of the Project Phoenix Market Pipeline.
    """

    # --------------------------------------------------
    # Pipeline Information
    # --------------------------------------------------

    pipeline_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    current_stage: Any = None

    # --------------------------------------------------
    # Market Information
    # --------------------------------------------------

    symbol: str = ""
    timeframe: str = ""

    # --------------------------------------------------
    # Raw Market Data
    # --------------------------------------------------

    raw_data: Any = None

    # --------------------------------------------------
    # Historical Data
    # --------------------------------------------------

    candles: list = field(default_factory=list)

    # --------------------------------------------------
    # Indicator Results
    # --------------------------------------------------

    indicators: dict = field(default_factory=dict)

    # --------------------------------------------------
    # Pattern Recognition
    # --------------------------------------------------

    patterns: list = field(default_factory=list)

    # --------------------------------------------------
    # Generated Signal
    # --------------------------------------------------

    signal: Any = None

    # --------------------------------------------------
    # Risk Engine
    # --------------------------------------------------

    risk_result: Any = None

    # --------------------------------------------------
    # Portfolio Engine
    # --------------------------------------------------

    portfolio_result: Any = None

    # --------------------------------------------------
    # AI Decision
    # --------------------------------------------------

    ai_result: Any = None

    # --------------------------------------------------
    # Execution Decision
    # --------------------------------------------------

    execution_result: Any = None

    # --------------------------------------------------
    # Final Decision
    # --------------------------------------------------

    approved: bool = False
    decision: str = ""
    reason: str = ""

    # --------------------------------------------------
    # Runtime Metadata
    # --------------------------------------------------

    metadata: dict = field(default_factory=dict)

    # --------------------------------------------------
    # Pipeline Flags
    # --------------------------------------------------

    completed: bool = False
    failed: bool = False

    # --------------------------------------------------
    # Utility Functions
    # --------------------------------------------------

    def set_metadata(self, key: str, value: Any) -> None:
        """
        Store runtime metadata.
        """
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Retrieve runtime metadata.
        """
        return self.metadata.get(key, default)

    def approve(self, decision: str, reason: str) -> None:
        """
        Approve pipeline execution.
        """
        self.approved = True
        self.completed = True
        self.decision = decision
        self.reason = reason

    def reject(self, decision: str, reason: str) -> None:
        """
        Reject pipeline execution.
        """
        self.approved = False
        self.failed = True
        self.decision = decision
        self.reason = reason

    def reset(self) -> None:
        """
        Reset pipeline state while preserving identity.
        """
        self.raw_data = None
        self.candles.clear()
        self.indicators.clear()
        self.patterns.clear()
        self.signal = None
        self.risk_result = None
        self.portfolio_result = None
        self.ai_result = None
        self.execution_result = None
        self.metadata.clear()

        self.approved = False
        self.completed = False
        self.failed = False
        self.decision = ""
        self.reason = ""