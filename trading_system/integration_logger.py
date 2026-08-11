"""
=================================================
Project Phoenix
Integration Logger
M39
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class IntegrationLog:

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    level: str = "INFO"

    component: str = ""

    message: str = ""


class IntegrationLogger:
    """
    Central logger for Trading System integration.
    """

    def __init__(self) -> None:

        self.logs: list[IntegrationLog] = []

    def log(
        self,
        component: str,
        message: str,
        level: str = "INFO",
    ) -> None:
        """
        Store integration log.
        """

        self.logs.append(

            IntegrationLog(

                level=level,

                component=component,

                message=message,

            )

        )

    def info(
        self,
        component: str,
        message: str,
    ) -> None:

        self.log(

            component=component,

            message=message,

            level="INFO",

        )

    def warning(
        self,
        component: str,
        message: str,
    ) -> None:

        self.log(

            component=component,

            message=message,

            level="WARNING",

        )

    def error(
        self,
        component: str,
        message: str,
    ) -> None:

        self.log(

            component=component,

            message=message,

            level="ERROR",

        )

    def clear(self) -> None:
        """
        Remove all logs.
        """

        self.logs.clear()

    def count(self) -> int:
        """
        Number of stored logs.
        """

        return len(self.logs)

    def latest(self) -> IntegrationLog | None:
        """
        Latest log entry.
        """

        if not self.logs:

            return None

        return self.logs[-1]