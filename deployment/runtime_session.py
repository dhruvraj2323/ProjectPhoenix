"""
=================================================
Project Phoenix
Runtime Session
M62.7.2 - Runtime Session Control
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class RuntimeSession:
    """
    Immutable metadata describing one runtime session.

    A RuntimeSession represents the identity and timing
    metadata of a single runtime execution session.

    This class does not:
    - control lifecycle transitions
    - start the runtime
    - stop the runtime
    - execute trades
    - control TradingProtection
    - execute strategies
    - modify risk
    - send alerts
    """

    session_id: str
    started_at: datetime | None
    stopped_at: datetime | None
    active: bool
    terminal: bool

    @classmethod
    def create(cls) -> "RuntimeSession":
        """
        Create a new inactive runtime session.

        The session receives a unique identifier at creation.
        """

        return cls(
            session_id=str(uuid4()),
            started_at=None,
            stopped_at=None,
            active=False,
            terminal=False,
        )

    def start(self) -> "RuntimeSession":
        """
        Mark the session as active.

        A session may only be started once.
        """

        if self.active:
            raise RuntimeError(
                "Runtime session is already active."
            )

        if self.terminal:
            raise RuntimeError(
                "Runtime session is already terminal."
            )

        now = datetime.now(
            timezone.utc
        )

        return RuntimeSession(
            session_id=self.session_id,
            started_at=now,
            stopped_at=None,
            active=True,
            terminal=False,
        )

    def stop(self) -> "RuntimeSession":
        """
        Mark the active session as stopped and terminal.

        A session may only be stopped once.
        """

        if not self.active:
            raise RuntimeError(
                "Runtime session is not active."
            )

        if self.terminal:
            raise RuntimeError(
                "Runtime session is already terminal."
            )

        now = datetime.now(
            timezone.utc
        )

        return RuntimeSession(
            session_id=self.session_id,
            started_at=self.started_at,
            stopped_at=now,
            active=False,
            terminal=True,
        )