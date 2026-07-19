"""
=================================================
Project Phoenix
System Integration Models
=================================================

Defines the core data models used by the
System Integration & Validation Engine.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# -------------------------------------------------
# Pipeline Stage
# -------------------------------------------------


@dataclass(slots=True)
class PipelineStage:
    """
    Represents one stage of the complete
    Project Phoenix execution pipeline.
    """

    name: str
    completed: bool = False
    execution_time_ms: float = 0.0
    message: str = ""


# -------------------------------------------------
# Validation Result
# -------------------------------------------------


@dataclass(slots=True)
class ValidationResult:
    """
    Validation status for the
    complete integration pipeline.
    """

    valid: bool
    reason: str


# -------------------------------------------------
# System Health
# -------------------------------------------------


@dataclass(slots=True)
class SystemHealth:
    """
    Overall health of the trading system.
    """

    healthy: bool = True
    total_modules: int = 0
    completed_modules: int = 0
    failed_modules: int = 0


# -------------------------------------------------
# Execution Summary
# -------------------------------------------------


@dataclass(slots=True)
class ExecutionSummary:
    """
    Summary of pipeline execution.
    """

    execution_time_ms: float = 0.0
    completed_stages: int = 0
    failed_stages: int = 0


# -------------------------------------------------
# Integration Status
# -------------------------------------------------


@dataclass(slots=True)
class IntegrationStatus:
    """
    Current status of system integration.
    """

    approved: bool = False
    pipeline_completed: bool = False

    stages: List[PipelineStage] = field(default_factory=list)

    validation: Optional[ValidationResult] = None

    health: Optional[SystemHealth] = None

    summary: Optional[ExecutionSummary] = None


# -------------------------------------------------
# Final Integration Result
# -------------------------------------------------


@dataclass(slots=True)
class IntegrationResult:
    """
    Final result returned by the
    Integration Engine.
    """

    status: str

    approved: bool

    validation: ValidationResult

    health: SystemHealth

    summary: ExecutionSummary

    stages: Dict[str, bool]