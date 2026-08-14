"""
=================================================
Project Phoenix
Health Degradation Policy
M62.4.1 - Runtime Health Degradation Policy
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_watchdog import (
    WatchdogHealthState,
)


# =========================================================
# Health Impact
# =========================================================

class HealthImpact(Enum):
    """
    Runtime impact produced by observed health.

    HEALTHY
        Runtime may remain operational.

    DEGRADED
        Runtime health is not safe enough for normal
        operation, but the runtime lifecycle itself is
        not automatically stopped.

    """

    HEALTHY = "HEALTHY"

    DEGRADED = "DEGRADED"


# =========================================================
# Health Degradation Decision
# =========================================================

@dataclass(frozen=True)
class HealthDegradationDecision:
    """
    Immutable result of health degradation policy
    evaluation.
    """

    health_state: WatchdogHealthState

    impact: HealthImpact

    runtime_state: RuntimeOperationalState

    trading_paused: bool

    reason: str

    @property
    def degraded(self) -> bool:
        """
        Return True when runtime health requires
        degraded operational handling.
        """

        return (
            self.impact
            == HealthImpact.DEGRADED
        )

    @property
    def recovered(self) -> bool:
        """
        Return True when observed health is healthy.
        """

        return (
            self.health_state
            == WatchdogHealthState.HEALTHY
        )


# =========================================================
# Health Degradation Policy
# =========================================================

class HealthDegradationPolicy:
    """
    Translate watchdog health into runtime degradation
    semantics.

    Responsibilities:
    - Translate HEALTHY into healthy runtime impact.
    - Translate UNHEALTHY into degraded runtime impact.
    - Define DEGRADED as a runtime operational state.
    - Require trading protection while degraded.
    - Preserve runtime lifecycle ownership outside this
      policy.

    This policy does NOT:
    - stop Runtime
    - restart Runtime
    - pause ContinuousRunner
    - close positions
    - cancel orders
    - execute trades
    - modify HealthMonitor
    - modify RuntimeWatchdog
    - directly modify TradingProtection
    """

    # --------------------------------------------------
    # Evaluate
    # --------------------------------------------------

    def evaluate(
        self,
        health_state: WatchdogHealthState,
    ) -> HealthDegradationDecision:
        """
        Evaluate the observed watchdog health state.
        """

        if (
            health_state
            == WatchdogHealthState.HEALTHY
        ):

            return HealthDegradationDecision(
                health_state=health_state,
                impact=HealthImpact.HEALTHY,
                runtime_state=(
                    RuntimeOperationalState.RUNNING
                ),
                trading_paused=False,
                reason=(
                    "Runtime health is healthy."
                ),
            )

        return HealthDegradationDecision(
            health_state=health_state,
            impact=HealthImpact.DEGRADED,
            runtime_state=(
                RuntimeOperationalState.DEGRADED
            ),
            trading_paused=True,
            reason=(
                "Runtime health is degraded; "
                "new trading activity must remain paused."
            ),
        )