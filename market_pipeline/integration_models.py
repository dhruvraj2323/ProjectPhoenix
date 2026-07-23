"""
=================================================
Project Phoenix
Integration Models
M31
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# Pipeline Status
# ==========================================================

@dataclass(slots=True)
class PipelineStatus:
    """
    Overall pipeline execution status.
    """

    completed: bool = False
    validation_passed: bool = False
    stage: str = "INITIALIZED"


# ==========================================================
# Processing Statistics
# ==========================================================

@dataclass(slots=True)
class ProcessingStatistics:
    """
    Pipeline processing statistics.
    """

    total_candles: int = 0
    indicators_calculated: int = 0
    patterns_detected: int = 0
    processing_time: float = 0.0


# ==========================================================
# Validation Summary
# ==========================================================

@dataclass(slots=True)
class ValidationSummary:
    """
    Validation summary.
    """

    passed: bool = False
    errors: int = 0
    warnings: int = 0


# ==========================================================
# Final Pipeline Result
# ==========================================================

@dataclass(slots=True)
class PipelineResult:
    """
    Final object returned by Market Pipeline.
    """

    approved: bool = False
    reason: str = ""

    status: PipelineStatus = field(
        default_factory=PipelineStatus
    )

    statistics: ProcessingStatistics = field(
        default_factory=ProcessingStatistics
    )

    validation: ValidationSummary = field(
        default_factory=ValidationSummary
    )

    payload: Any = None


# ==========================================================
# Factory
# ==========================================================

class IntegrationModels:
    """
    Creates standardized integration objects.
    """

    def create_pipeline_result(
        self,
        *,
        approved: bool,
        reason: str,
        payload: Any = None,
        status: PipelineStatus | None = None,
        statistics: ProcessingStatistics | None = None,
        validation: ValidationSummary | None = None,
    ) -> PipelineResult:

        return PipelineResult(
            approved=approved,
            reason=reason,
            payload=payload,
            status=status or PipelineStatus(),
            statistics=statistics or ProcessingStatistics(),
            validation=validation or ValidationSummary(),
        )