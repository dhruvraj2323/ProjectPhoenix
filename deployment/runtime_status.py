"""
=================================================
Project Phoenix
Runtime Status
M62.3.4.1 - Runtime Operational Status Model
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)


@dataclass(frozen=True)
class RuntimeStatus:
    """
    Immutable runtime observability snapshot.

    This model exposes operational readiness and health
    information without exposing credentials, trading
    decisions, or live-trading approval.
    """

    operational_state: RuntimeOperationalState

    configuration_ready: bool

    deployment_healthy: bool

    runtime_running: bool

    reason: str

    timestamp: datetime

    @property
    def ready(self) -> bool:
        """
        Return True when configuration and deployment
        health are both ready.
        """

        return (
            self.configuration_ready
            and self.deployment_healthy
        )

    @property
    def healthy(self) -> bool:
        """
        Return True when deployment health is healthy.
        """

        return self.deployment_healthy

    @property
    def operational(self) -> bool:
        """
        Return True only when the runtime is actively
        running.
        """

        return (
            self.runtime_running
            and (
                self.operational_state
                == RuntimeOperationalState.RUNNING
            )
        )