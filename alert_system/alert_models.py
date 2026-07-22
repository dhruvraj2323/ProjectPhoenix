"""
=================================================
Project Phoenix
Alert Models
=================================================

Standard alert models.
"""

from dataclasses import dataclass


# -------------------------------------------------
# Alert Message
# -------------------------------------------------


@dataclass(slots=True)
class AlertMessage:

    title: str
    message: str
    alert_type: str
    timestamp: str


# -------------------------------------------------
# Alert Channel
# -------------------------------------------------


@dataclass(slots=True)
class AlertChannel:

    name: str
    enabled: bool
    connected: bool


# -------------------------------------------------
# Alert Status
# -------------------------------------------------


@dataclass(slots=True)
class AlertStatus:

    running: bool
    alerts_sent: int
    connected_channels: int


# -------------------------------------------------
# Alert Result
# -------------------------------------------------


@dataclass(slots=True)
class AlertResult:

    approved: bool
    reason: str
    status: AlertStatus
    delivered_channels: list[str]