"""
Project Phoenix
Milestone M18 - Configuration & Settings Engine

Module:
    config_models.py

Purpose:
    Defines all core data models used by the
    Configuration Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConfigurationStatus(Enum):
    """
    Final configuration status.
    """

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"


@dataclass
class ConfigurationItem:
    """
    Represents a single configuration item.
    """

    key: str

    value: Any

    category: str

    description: str


@dataclass
class ConfigurationContext:
    """
    Context supplied to the Configuration Engine.
    """

    application_name: str

    version: str

    environment: str

    configuration: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ConfigurationDecision:
    """
    Final output of the Configuration Engine.
    """

    status: ConfigurationStatus

    items: list[ConfigurationItem]

    approved: bool

    reason: str