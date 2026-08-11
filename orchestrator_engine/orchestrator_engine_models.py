"""
=================================================
Project Phoenix
Orchestrator Models
M39
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


# -------------------------------------------------
# Orchestrator Status
# -------------------------------------------------


@dataclass(slots=True)
class OrchestratorStatus:
    """
    Runtime status of the Orchestrator Engine.
    """

    running: bool = False

    current_stage: str = ""

    completed_stages: int = 0

    total_stages: int = 0


# -------------------------------------------------
# Orchestrator Result
# -------------------------------------------------


@dataclass(slots=True)
class OrchestratorResult:
    """
    Final orchestration result.
    """

    approved: bool = False

    status: str = "PENDING"

    reason: str = ""

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    finished_at: datetime | None = None


# -------------------------------------------------
# Pipeline Stage
# -------------------------------------------------


@dataclass(slots=True)
class PipelineStage:
    """
    Represents one pipeline stage.
    """

    name: str

    completed: bool = False

    success: bool = False


# -------------------------------------------------
# Engine Health
# -------------------------------------------------


@dataclass(slots=True)
class EngineHealth:
    """
    Health information for one engine.
    """

    engine_name: str

    ready: bool = False

    running: bool = False

    failed: bool = False