"""
Project Phoenix - Configuration Readiness Models
M62.2.6.1
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ConfigurationReadinessCheck:
    """
    Represents one configuration readiness check.
    """

    name: str
    passed: bool
    required: bool
    message: str


@dataclass(frozen=True)
class ConfigurationReadinessResult:
    """
    Represents the aggregated configuration readiness result.

    This result represents configuration readiness only.
    It does not represent deployment approval, MT5
    connection status, or live-trading authorization.
    """

    ready: bool
    environment_ready: bool
    mt5_ready: bool
    runtime_ready: bool
    secrets_safe: bool
    checks: tuple[ConfigurationReadinessCheck, ...] = field(
        default_factory=tuple
    )
    errors: tuple[str, ...] = field(
        default_factory=tuple
    )
    warnings: tuple[str, ...] = field(
        default_factory=tuple
    )

    @property
    def passed_checks(self) -> int:
        """Return the number of passed readiness checks."""
        return sum(
            check.passed
            for check in self.checks
        )

    @property
    def failed_checks(self) -> int:
        """Return the number of failed readiness checks."""
        return sum(
            not check.passed
            for check in self.checks
        )