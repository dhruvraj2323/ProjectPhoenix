"""
=================================================
Project Phoenix
Market Pipeline Models
M31
=================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class PipelineStage(Enum):
    INITIALIZED = "INITIALIZED"
    MARKET_DATA = "MARKET_DATA"
    INDICATORS = "INDICATORS"
    PATTERNS = "PATTERNS"
    SIGNAL = "SIGNAL"
    RISK = "RISK"
    PORTFOLIO = "PORTFOLIO"
    AI = "AI"
    EXECUTION = "EXECUTION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class PipelineStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass(slots=True)
class PipelineResult:
    """
    Result returned by every pipeline stage.
    """

    stage: PipelineStage

    status: PipelineStatus

    approved: bool

    reason: str = ""

    data: Dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class PipelineStatistics:
    """
    Runtime statistics.
    """

    started_at: datetime = field(default_factory=datetime.utcnow)

    finished_at: Optional[datetime] = None

    stages_completed: int = 0

    stages_failed: int = 0

    execution_time_ms: float = 0.0


@dataclass(slots=True)
class PipelineState:
    """
    Shared pipeline state.
    """

    symbol: str

    timeframe: str

    mode: str

    current_stage: PipelineStage = PipelineStage.INITIALIZED

    approved: bool = True

    completed: bool = False

    reason: str = ""

    statistics: PipelineStatistics = field(default_factory=PipelineStatistics)

    context: Dict[str, Any] = field(default_factory=dict)

    results: List[PipelineResult] = field(default_factory=list)