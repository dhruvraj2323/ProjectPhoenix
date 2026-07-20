"""
=================================================
Project Phoenix
Deployment Models
=================================================

Standard deployment models.
"""

from dataclasses import dataclass


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