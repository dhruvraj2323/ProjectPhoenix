"""
Project Phoenix
Milestone M15 - Trading Orchestrator Engine

Module:
    orchestrator_models.py

Purpose:
    Defines all data models used by the
    Trading Orchestrator Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class OrchestratorStatus(Enum):
    """
    Final pipeline status.
    """

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"


@dataclass
class TradingStage:
    """
    Represents one completed pipeline stage.
    """

    name: str

    completed: bool

    reason: str = ""


@dataclass
class ExecutionMetadata:
    """
    Execution metadata.
    """

    execution_time_ms: float = 0.0

    completed_stages: int = 0

    failed_stage: Optional[str] = None


@dataclass
class TradingContext:
    """
    Context supplied to the
    Trading Orchestrator.
    """

    symbol: str

    timeframe: str

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class TradingResult:
    """
    Pipeline execution summary.
    """

    stages: List[TradingStage]

    metadata: ExecutionMetadata


@dataclass
class TradingDecision:
    """
    Final Trading Orchestrator decision.
    """

    status: OrchestratorStatus

    approved: bool

    result: TradingResult

    reason: Optional[str] = None