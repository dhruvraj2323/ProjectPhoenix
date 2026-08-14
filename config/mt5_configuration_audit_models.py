"""
Project Phoenix - MT5 Configuration Audit Models
M62.2.3.1
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MT5ConfigurationCheck:
    """
    Represents the result of a single MT5 configuration check.
    """

    name: str
    approved: bool
    required: bool
    message: str
    sensitive: bool = False


@dataclass(frozen=True)
class MT5ConfigurationAuditResult:
    """
    Represents the complete MT5 configuration audit result.
    """

    approved: bool
    credential_file_present: bool
    credential_file_valid: bool
    environment_valid: bool
    consistency_valid: bool
    checks: tuple[MT5ConfigurationCheck, ...] = field(
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
        """Return the number of approved checks."""
        return sum(
            check.approved
            for check in self.checks
        )

    @property
    def failed_checks(self) -> int:
        """Return the number of failed checks."""
        return sum(
            not check.approved
            for check in self.checks
        )