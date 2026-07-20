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


@dataclass
class AlertMessage:

    title: str
    message: str
    alert_type: str
    timestamp: str


# -------------------------------------------------
# Alert Channel
# -------------------------------------------------


@dataclass
class AlertChannel:

    name: str
    enabled: bool
    connected: bool


# -------------------------------------------------
# Alert Status
# -------------------------------------------------


@dataclass
class AlertStatus:

    running: bool
    alerts_sent: int
    connected_channels: int


# -------------------------------------------------
# Alert Result
# -------------------------------------------------


@dataclass
class AlertResult:

    approved: bool
    reason: str
    status: AlertStatus