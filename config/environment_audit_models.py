"""
Project Phoenix - Environment Audit Models
M62.2.2.1
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EnvironmentCheck:
    """
    Represents the result of a single environment configuration check.
    """

    name: str
    approved: bool
    required: bool
    message: str
    sensitive: bool = False


@dataclass(frozen=True)
class EnvironmentAuditResult:
    """
    Represents the complete environment configuration audit result.
    """

    approved: bool
    checks: tuple[EnvironmentCheck, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)

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