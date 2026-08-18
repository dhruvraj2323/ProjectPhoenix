"""
=================================================
Project Phoenix
Controlled Demo Operation
M63.9
=================================================

Purpose
-------
Provide the controlled operational boundary for the
Project Phoenix DEMO observation period.

M63.9 responsibilities:

- Require a successful M63.8 go-live validation.
- Enforce a controlled 7-10 day observation window.
- Use the existing ContinuousRunner.
- Preserve the existing TradingProtection boundary.
- Record cycle-level operational evidence.
- Persist observation events in JSON Lines format.

M63.9 does NOT:

- modify strategies.
- modify AI decisions.
- modify Risk Engine decisions.
- modify Portfolio Engine decisions.
- execute orders directly.
- modify positions.
- bypass TradingProtection.
- replace ReportingEngine.
- replace ContinuousRunner.
- automatically change trading parameters.

Important
---------
M63.9 is an observation controller.

It is intentionally NOT connected to main.py.

DEMO operation must be explicitly started through this
controller after M63.8 has produced a READY result.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any


# =========================================================
# Operation State
# =========================================================

class ControlledDemoOperationState(str, Enum):
    """
    Lifecycle state of the M63.9 observation operation.
    """

    NOT_STARTED = "NOT_STARTED"

    ACTIVE = "ACTIVE"

    EXPIRED = "EXPIRED"

    STOPPED = "STOPPED"

    BLOCKED = "BLOCKED"


# =========================================================
# Observation Event
# =========================================================

@dataclass(frozen=True, slots=True)
class DemoObservationEvent:
    """
    Immutable persisted observation event.
    """

    event_id: int

    timestamp: str

    cycle_number: int

    runtime_state: str

    trading_protection_state: str

    cycle_status: str

    executed_symbols: tuple[str, ...]

    no_trade_symbols: tuple[str, ...]

    failed_symbols: tuple[str, ...]

    trade_ids: tuple[str, ...]

    errors: tuple[str, ...]

    success: bool


# =========================================================
# Operation Status
# =========================================================

@dataclass(frozen=True, slots=True)
class ControlledDemoOperationStatus:
    """
    Immutable M63.9 operation status snapshot.
    """

    state: ControlledDemoOperationState

    observation_days: int

    started_at: datetime | None

    expires_at: datetime | None

    cycle_count: int

    event_count: int

    last_error: str = ""

    @property
    def active(self) -> bool:
        """
        Return True when the observation operation is active.
        """

        return (
            self.state
            == ControlledDemoOperationState.ACTIVE
        )

    @property
    def expired(self) -> bool:
        """
        Return True when the observation window expired.
        """

        return (
            self.state
            == ControlledDemoOperationState.EXPIRED
        )


# =========================================================
# Controlled Demo Operation
# =========================================================

class ControlledDemoOperation:
    """
    M63.9 controlled DEMO observation controller.

    The controller requires an already completed M63.8
    validation result.

    It does not perform the go-live validation itself.
    M63.8 remains the authoritative technical gate.
    """

    MIN_OBSERVATION_DAYS = 7

    MAX_OBSERVATION_DAYS = 10

    def __init__(
        self,
        *,
        runner,
        go_live_result,
        observation_days: int = 7,
        ledger_path: str | Path = (
            "logs/demo_observation/m63_9_observation.jsonl"
        ),
        clock=None,
    ) -> None:

        self.runner = runner

        self.go_live_result = (
            go_live_result
        )

        self.observation_days = (
            observation_days
        )

        self.ledger_path = Path(
            ledger_path
        )

        self.clock = (
            clock
            if clock is not None
            else lambda: datetime.now(
                timezone.utc
            )
        )

        self._state = (
            ControlledDemoOperationState.NOT_STARTED
        )

        self._started_at: datetime | None = None

        self._expires_at: datetime | None = None

        self._cycle_count = 0

        self._event_count = 0

        self._last_error = ""

    # =====================================================
    # Start
    # =====================================================

    def start(self) -> ControlledDemoOperationStatus:
        """
        Start the M63.9 controlled observation window.

        M63.8 must already be READY.

        Observation duration must be between 7 and 10 days.
        """

        if self._state == (
            ControlledDemoOperationState.ACTIVE
        ):

            raise RuntimeError(
                "M63.9 operation is already active."
            )

        if not self._valid_observation_days():

            self._state = (
                ControlledDemoOperationState.BLOCKED
            )

            self._last_error = (
                "Observation duration must be "
                "between 7 and 10 days."
            )

            raise ValueError(
                self._last_error
            )

        if not self._go_live_ready():

            self._state = (
                ControlledDemoOperationState.BLOCKED
            )

            self._last_error = (
                "M63.8 DEMO go-live validation "
                "is not READY."
            )

            raise RuntimeError(
                self._last_error
            )

        now = self._now()

        self._started_at = now

        self._expires_at = (
            now
            + timedelta(
                days=self.observation_days
            )
        )

        self._cycle_count = 0

        self._event_count = 0

        self._last_error = ""

        self._state = (
            ControlledDemoOperationState.ACTIVE
        )

        return self.status()

    # =====================================================
    # Stop
    # =====================================================

    def stop(
        self,
    ) -> ControlledDemoOperationStatus:
        """
        Stop the controlled observation operation.

        Stopping the observation controller does not directly
        modify TradingProtection or positions.
        """

        if self._state == (
            ControlledDemoOperationState.ACTIVE
        ):

            self._state = (
                ControlledDemoOperationState.STOPPED
            )

        return self.status()

    # =====================================================
    # Run One Observation Cycle
    # =====================================================

    def run_cycle(self) -> DemoObservationEvent:
        """
        Execute exactly one controlled observation cycle.

        The existing ContinuousRunner remains responsible
        for executing the Phoenix trading cycle.

        M63.9 only controls whether that cycle is allowed
        to run and records the resulting evidence.
        """

        self._ensure_active()

        self._refresh_expiration()

        if self._state != (
            ControlledDemoOperationState.ACTIVE
        ):

            raise RuntimeError(
                "M63.9 observation window is not active."
            )

        # -------------------------------------------------
        # Explicitly verify current TradingProtection.
        # -------------------------------------------------

        protection = getattr(
            self.runner,
            "trading_protection",
            None,
        )

        if protection is None:

            self._last_error = (
                "ContinuousRunner does not expose "
                "TradingProtection."
            )

            raise RuntimeError(
                self._last_error
            )

        self._cycle_count += 1

        cycle_success = False

        errors: list[str] = []

        try:

            cycle_success = bool(
                self.runner.run_once()
            )

        except Exception as exc:

            cycle_success = False

            errors.append(
                str(exc)
            )

        # -------------------------------------------------
        # Collect Cycle Summary
        # -------------------------------------------------

        trading_cycle = getattr(
            self.runner,
            "trading_cycle",
            None,
        )

        execution_summary = getattr(
            trading_cycle,
            "execution_summary",
            None,
        )

        executed_symbols: tuple[str, ...] = ()

        no_trade_symbols: tuple[str, ...] = ()

        failed_symbols: tuple[str, ...] = ()

        trade_ids: tuple[str, ...] = ()

        cycle_status = (
            "UNKNOWN"
        )

        if execution_summary is not None:

            cycle_status = self._enum_value(
                getattr(
                    execution_summary,
                    "status",
                    "UNKNOWN",
                )
            )

            executed_symbols = (
                self._symbol_names(
                    getattr(
                        execution_summary,
                        "executed",
                        (),
                    )
                )
            )

            no_trade_symbols = (
                self._symbol_names(
                    getattr(
                        execution_summary,
                        "no_trade",
                        (),
                    )
                )
            )

            failed_symbols = (
                self._symbol_names(
                    getattr(
                        execution_summary,
                        "failed",
                        (),
                    )
                )
            )

            trade_ids = (
                self._trade_ids(
                    getattr(
                        trading_cycle,
                        "trade_records",
                        (),
                    )
                )
            )

        # -------------------------------------------------
        # Preserve Last Error
        # -------------------------------------------------

        cycle_error = getattr(
            trading_cycle,
            "last_error",
            "",
        )

        if cycle_error:

            errors.append(
                str(cycle_error)
            )

        # -------------------------------------------------
        # Current Protection State
        # -------------------------------------------------

        protection_state = self._enum_value(
            getattr(
                protection,
                "state",
                "UNKNOWN",
            )
        )

        # -------------------------------------------------
        # Runtime State
        #
        # Runtime state is obtained from the runner when
        # available. This avoids creating another runtime
        # state store.
        # -------------------------------------------------

        runtime_state = self._runtime_state()

        event = DemoObservationEvent(
            event_id=(
                self._event_count + 1
            ),
            timestamp=(
                self._now().isoformat()
            ),
            cycle_number=self._cycle_count,
            runtime_state=runtime_state,
            trading_protection_state=(
                protection_state
            ),
            cycle_status=cycle_status,
            executed_symbols=(
                executed_symbols
            ),
            no_trade_symbols=(
                no_trade_symbols
            ),
            failed_symbols=(
                failed_symbols
            ),
            trade_ids=trade_ids,
            errors=tuple(
                self._deduplicate(
                    errors
                )
            ),
            success=cycle_success,
        )

        self._persist_event(
            event
        )

        self._event_count += 1

        return event

    # =====================================================
    # Status
    # =====================================================

    def status(
        self,
    ) -> ControlledDemoOperationStatus:
        """
        Return the current M63.9 operation status.
        """

        self._refresh_expiration()

        return ControlledDemoOperationStatus(
            state=self._state,
            observation_days=(
                self.observation_days
            ),
            started_at=self._started_at,
            expires_at=self._expires_at,
            cycle_count=self._cycle_count,
            event_count=self._event_count,
            last_error=self._last_error,
        )

    # =====================================================
    # Go-Live Result
    # =====================================================

    def go_live_ready(self) -> bool:
        """
        Return the original M63.8 decision.

        M63.9 never changes that decision.
        """

        return self._go_live_ready()

    # =====================================================
    # Internal Helpers
    # =====================================================

    def _ensure_active(
        self,
    ) -> None:

        if self._state == (
            ControlledDemoOperationState.NOT_STARTED
        ):

            raise RuntimeError(
                "M63.9 operation has not been started."
            )

        if self._state == (
            ControlledDemoOperationState.BLOCKED
        ):

            raise RuntimeError(
                "M63.9 operation is blocked."
            )

        if self._state == (
            ControlledDemoOperationState.STOPPED
        ):

            raise RuntimeError(
                "M63.9 operation has been stopped."
            )

        if self._state == (
            ControlledDemoOperationState.EXPIRED
        ):

            raise RuntimeError(
                "M63.9 observation window has expired."
            )

    # -----------------------------------------------------

    def _refresh_expiration(
        self,
    ) -> None:

        if self._state != (
            ControlledDemoOperationState.ACTIVE
        ):

            return

        if self._expires_at is None:

            return

        if self._now() >= self._expires_at:

            self._state = (
                ControlledDemoOperationState.EXPIRED
            )

    # -----------------------------------------------------

    def _valid_observation_days(
        self,
    ) -> bool:

        return (
            self.MIN_OBSERVATION_DAYS
            <= self.observation_days
            <= self.MAX_OBSERVATION_DAYS
        )

    # -----------------------------------------------------

    def _go_live_ready(
        self,
    ) -> bool:

        return bool(
            getattr(
                self.go_live_result,
                "ready",
                False,
            )
        )

    # -----------------------------------------------------

    def _now(
        self,
    ) -> datetime:

        value = self.clock()

        if value.tzinfo is None:

            return value.replace(
                tzinfo=timezone.utc
            )

        return value

    # -----------------------------------------------------

    def _runtime_state(
        self,
    ) -> str:

        runtime = getattr(
            self.runner,
            "runtime",
            None,
        )

        if runtime is not None:

            try:

                status_snapshot = (
                    runtime.status_snapshot()
                )

                return self._enum_value(
                    getattr(
                        status_snapshot,
                        "operational_state",
                        "UNKNOWN",
                    )
                )

            except Exception:
                pass

        trading_cycle = getattr(
            self.runner,
            "trading_cycle",
            None,
        )

        if trading_cycle is not None:

            if getattr(
                trading_cycle,
                "connected",
                False,
            ):

                return "RUNNING"

        return "UNKNOWN"

    # -----------------------------------------------------

    @staticmethod
    def _enum_value(
        value: Any,
    ) -> str:

        raw = getattr(
            value,
            "value",
            value,
        )

        return str(
            raw
        )

    # -----------------------------------------------------

    @staticmethod
    def _symbol_names(
        values,
    ) -> tuple[str, ...]:

        names: list[str] = []

        if values is None:

            return ()

        for item in values:

            if isinstance(
                item,
                str,
            ):

                name = item

            else:

                name = getattr(
                    item,
                    "symbol",
                    "",
                )

            if name:

                names.append(
                    str(name)
                )

        return tuple(
            names
        )

    # -----------------------------------------------------

    @staticmethod
    def _trade_ids(
        records,
    ) -> tuple[str, ...]:

        result: list[str] = []

        if records is None:

            return ()

        for record in records:

            trade_id = getattr(
                record,
                "trade_id",
                "",
            )

            if trade_id:

                result.append(
                    str(trade_id)
                )

        return tuple(
            result
        )

    # -----------------------------------------------------

    @staticmethod
    def _deduplicate(
        values,
    ) -> list[str]:

        result: list[str] = []

        for value in values:

            if value and value not in result:

                result.append(
                    value
                )

        return result

    # -----------------------------------------------------

    def _persist_event(
        self,
        event: DemoObservationEvent,
    ) -> None:

        self.ledger_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = asdict(
            event
        )

        payload[
            "executed_symbols"
        ] = list(
            event.executed_symbols
        )

        payload[
            "no_trade_symbols"
        ] = list(
            event.no_trade_symbols
        )

        payload[
            "failed_symbols"
        ] = list(
            event.failed_symbols
        )

        payload[
            "trade_ids"
        ] = list(
            event.trade_ids
        )

        payload[
            "errors"
        ] = list(
            event.errors
        )

        with self.ledger_path.open(
            "a",
            encoding="utf-8",
        ) as handle:

            handle.write(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                )
                + "\n"
            )