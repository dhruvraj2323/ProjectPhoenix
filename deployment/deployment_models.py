"""
=================================================
Project Phoenix
Deployment Models
M61.10.2 - Runtime Protection Observability
=================================================
"""

from dataclasses import dataclass

from deployment.deployment_health import (
    DeploymentHealthState,
)

from deployment.trading_protection import (
    TradingProtectionState,
)


# -------------------------------------------------
# Deployment Status
# -------------------------------------------------

@dataclass
class DeploymentStatus:

    running: bool
    healthy: bool
    version: str
    environment: str


# -------------------------------------------------
# Runtime Status
# -------------------------------------------------

@dataclass
class RuntimeStatus:

    uptime: str
    cpu_usage: float
    memory_usage: float
    active_threads: int


# -------------------------------------------------
# Deployment Result
# -------------------------------------------------

@dataclass
class DeploymentResult:

    approved: bool
    reason: str
    status: DeploymentStatus

    health_report: dict | None = None

    health_state: DeploymentHealthState = (
        DeploymentHealthState.UNHEALTHY
    )

    trading_protection_state: (
        TradingProtectionState
    ) = TradingProtectionState.PAUSED