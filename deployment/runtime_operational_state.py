"""
=================================================
Project Phoenix
Runtime Operational State
M62.3.3.1 - Runtime Operational State Contract
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RuntimeOperationalState(Enum):
    """
    Operational state of the Project Phoenix runtime.

    This state is intentionally separate from:
    - configuration readiness
    - deployment health
    - deployment approval
    - trading permission
    """

    STARTING = "STARTING"
    READY = "READY"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class RuntimeOperationalStatus:
    """
    Structured runtime operational status.
    """

    state: RuntimeOperationalState
    reason: str

    @property
    def running(self) -> bool:
        """
        Return True only when runtime is actively running.
        """

        return (
            self.state
            == RuntimeOperationalState.RUNNING
        )

    @property
    def terminal(self) -> bool:
        """
        Return True when the runtime is in a terminal
        stopped or failed state.
        """

        return self.state in {
            RuntimeOperationalState.STOPPED,
            RuntimeOperationalState.FAILED,
        }