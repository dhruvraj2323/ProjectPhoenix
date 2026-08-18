"""
=================================================
Project Phoenix
Demo Go-Live Validation
M63.8
=================================================

Purpose
-------
Provide the final technical validation gate before
Phoenix is permitted to operate against an MT5 DEMO
account.

This module is a pure validation boundary.

It DOES NOT:

- connect to MT5
- send orders
- modify positions
- close positions
- modify risk
- modify portfolio decisions
- modify TradingProtection
- start Runtime
- stop Runtime
- restart Runtime
- generate trading signals
- modify strategies

It evaluates authoritative subsystem snapshots supplied
by the caller.

Critical safety rule
--------------------
A real account MUST always block DEMO go-live.

M63.8 is a validation snapshot, not a permanent trading
authorization token.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable


# =========================================================
# Validation State
# =========================================================

class DemoGoLiveValidationState(str, Enum):
    """
    Final M63.8 validation state.
    """

    READY = "READY"

    BLOCKED = "BLOCKED"


# =========================================================
# Gate State
# =========================================================

class DemoGoLiveGateState(str, Enum):
    """
    State of one individual M63.8 validation gate.
    """

    PASS = "PASS"

    FAIL = "FAIL"


# =========================================================
# Individual Gate Result
# =========================================================

@dataclass(frozen=True, slots=True)
class DemoGoLiveGateResult:
    """
    Immutable result for one M63.8 gate.
    """

    name: str

    state: DemoGoLiveGateState

    reason: str

    @property
    def passed(self) -> bool:
        """
        Return True when this gate passed.
        """

        return (
            self.state
            == DemoGoLiveGateState.PASS
        )


# =========================================================
# Validation Snapshot
# =========================================================

@dataclass(frozen=True, slots=True)
class DemoGoLiveValidationSnapshot:
    """
    Authoritative subsystem observations supplied to
    the M63.8 validator.

    These values represent an observation snapshot.

    M63.8 does not obtain or mutate these values.
    """

    mt5_connected: bool

    account_available: bool

    demo_account_confirmed: bool

    configured_symbols: tuple[str, ...]

    healthy_symbols: tuple[str, ...]

    market_data_healthy: bool

    runtime_state: Any

    trading_protection_state: Any

    risk_approved: bool

    execution_healthy: bool

    reconciliation_healthy: bool

    reporting_healthy: bool


# =========================================================
# Final Validation Result
# =========================================================

@dataclass(frozen=True, slots=True)
class DemoGoLiveValidationResult:
    """
    Immutable final M63.8 validation result.
    """

    state: DemoGoLiveValidationState

    gates: tuple[DemoGoLiveGateResult, ...]

    reasons: tuple[str, ...]

    validated_at: datetime

    @property
    def ready(self) -> bool:
        """
        Return True only when every required gate passed.
        """

        return (
            self.state
            == DemoGoLiveValidationState.READY
        )

    @property
    def blocked(self) -> bool:
        """
        Return True when DEMO go-live is blocked.
        """

        return (
            self.state
            == DemoGoLiveValidationState.BLOCKED
        )

    @property
    def failed_gates(self) -> tuple[
        DemoGoLiveGateResult,
        ...,
    ]:
        """
        Return all failed validation gates.
        """

        return tuple(
            gate
            for gate in self.gates
            if not gate.passed
        )


# =========================================================
# Validator
# =========================================================

class DemoGoLiveValidator:
    """
    Final technical DEMO go-live validation boundary.

    The validator consumes existing subsystem results
    and determines whether Phoenix is technically ready
    for controlled DEMO operation.

    It never performs trading actions.
    """

    REQUIRED_GATES = (
        "MT5_CONNECTION",
        "ACCOUNT",
        "DEMO_ACCOUNT",
        "SYMBOLS",
        "MARKET_DATA",
        "RUNTIME",
        "TRADING_PROTECTION",
        "RISK",
        "EXECUTION",
        "RECONCILIATION",
        "REPORTING",
    )

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def validate(
        self,
        snapshot: DemoGoLiveValidationSnapshot,
    ) -> DemoGoLiveValidationResult:
        """
        Evaluate the complete M63.8 validation snapshot.

        All gates must pass before the result can become
        READY.

        A real-account condition always produces a failed
        DEMO_ACCOUNT gate.
        """

        gates: list[
            DemoGoLiveGateResult
        ] = []

        # -------------------------------------------------
        # 1. MT5 Connection
        # -------------------------------------------------

        gates.append(
            self._gate(
                name="MT5_CONNECTION",
                condition=snapshot.mt5_connected,
                passed_reason=(
                    "MT5 connection is healthy."
                ),
                failed_reason=(
                    "MT5 connection is unavailable."
                ),
            )
        )

        # -------------------------------------------------
        # 2. Account
        # -------------------------------------------------

        gates.append(
            self._gate(
                name="ACCOUNT",
                condition=snapshot.account_available,
                passed_reason=(
                    "MT5 account information is available."
                ),
                failed_reason=(
                    "MT5 account information is unavailable."
                ),
            )
        )

        # -------------------------------------------------
        # 3. DEMO Account
        #
        # This is a hard safety boundary.
        # -------------------------------------------------

        if not snapshot.account_available:

            demo_account_gate = (
                self._fail(
                    name="DEMO_ACCOUNT",
                    reason=(
                        "DEMO account cannot be confirmed "
                        "because account information is unavailable."
                    ),
                )
            )

        elif not snapshot.demo_account_confirmed:

            demo_account_gate = (
                self._fail(
                    name="DEMO_ACCOUNT",
                    reason=(
                        "Live account detected or DEMO "
                        "account could not be confirmed. "
                        "DEMO trading is blocked."
                    ),
                )
            )

        else:

            demo_account_gate = (
                self._pass(
                    name="DEMO_ACCOUNT",
                    reason=(
                        "MT5 DEMO account confirmed."
                    ),
                )
            )

        gates.append(demo_account_gate)

        # -------------------------------------------------
        # 4. Symbols
        # -------------------------------------------------

        configured_symbols = self._normalize_symbols(
            snapshot.configured_symbols
        )

        healthy_symbols = self._normalize_symbols(
            snapshot.healthy_symbols
        )

        missing_symbols = tuple(
            symbol
            for symbol in configured_symbols
            if symbol not in healthy_symbols
        )

        symbols_pass = (
            bool(configured_symbols)
            and not missing_symbols
        )

        if symbols_pass:

            symbol_reason = (
                "All configured symbols are healthy: "
                + ", ".join(configured_symbols)
                + "."
            )

        elif not configured_symbols:

            symbol_reason = (
                "No configured trading symbols are available."
            )

        else:

            symbol_reason = (
                "Required symbols are not healthy: "
                + ", ".join(missing_symbols)
                + "."
            )

        gates.append(
            self._gate(
                name="SYMBOLS",
                condition=symbols_pass,
                passed_reason=symbol_reason,
                failed_reason=symbol_reason,
            )
        )

        # -------------------------------------------------
        # 5. Market Data
        # -------------------------------------------------

        gates.append(
            self._gate(
                name="MARKET_DATA",
                condition=snapshot.market_data_healthy,
                passed_reason=(
                    "Market data is healthy."
                ),
                failed_reason=(
                    "Market data is not healthy."
                ),
            )
        )

        # -------------------------------------------------
        # 6. Runtime
        # -------------------------------------------------

        runtime_healthy = self._runtime_is_healthy(
            snapshot.runtime_state
        )

        gates.append(
            self._gate(
                name="RUNTIME",
                condition=runtime_healthy,
                passed_reason=(
                    "Runtime is operational and healthy."
                ),
                failed_reason=(
                    "Runtime is not in a safe operational "
                    "state for DEMO trading."
                ),
            )
        )

        # -------------------------------------------------
        # 7. Trading Protection
        # -------------------------------------------------

        protection_active = (
            self._state_value(
                snapshot.trading_protection_state
            )
            == "ACTIVE"
        )

        gates.append(
            self._gate(
                name="TRADING_PROTECTION",
                condition=protection_active,
                passed_reason=(
                    "TradingProtection is ACTIVE."
                ),
                failed_reason=(
                    "TradingProtection is not ACTIVE."
                ),
            )
        )

        # -------------------------------------------------
        # 8. Risk
        # -------------------------------------------------

        gates.append(
            self._gate(
                name="RISK",
                condition=snapshot.risk_approved,
                passed_reason=(
                    "Risk governance is approved."
                ),
                failed_reason=(
                    "Risk governance is not approved."
                ),
            )
        )

        # -------------------------------------------------
        # 9. Execution
        # -------------------------------------------------

        gates.append(
            self._gate(
                name="EXECUTION",
                condition=snapshot.execution_healthy,
                passed_reason=(
                    "Execution reliability is healthy."
                ),
                failed_reason=(
                    "Execution reliability is not healthy."
                ),
            )
        )

        # -------------------------------------------------
        # 10. Reconciliation
        # -------------------------------------------------

        gates.append(
            self._gate(
                name="RECONCILIATION",
                condition=snapshot.reconciliation_healthy,
                passed_reason=(
                    "Order and position reconciliation "
                    "is healthy."
                ),
                failed_reason=(
                    "Order and position reconciliation "
                    "is not healthy."
                ),
            )
        )

        # -------------------------------------------------
        # 11. Reporting
        # -------------------------------------------------

        gates.append(
            self._gate(
                name="REPORTING",
                condition=snapshot.reporting_healthy,
                passed_reason=(
                    "Reporting infrastructure is healthy."
                ),
                failed_reason=(
                    "Reporting infrastructure is not healthy."
                ),
            )
        )

        # -------------------------------------------------
        # Final Decision
        # -------------------------------------------------

        failed_gates = tuple(
            gate
            for gate in gates
            if not gate.passed
        )

        reasons = tuple(
            gate.reason
            for gate in failed_gates
        )

        state = (
            DemoGoLiveValidationState.READY
            if not failed_gates
            else DemoGoLiveValidationState.BLOCKED
        )

        return DemoGoLiveValidationResult(
            state=state,
            gates=tuple(gates),
            reasons=reasons,
            validated_at=datetime.now(
                timezone.utc
            ),
        )

    # -----------------------------------------------------
    # Gate Builder
    # -----------------------------------------------------

    @staticmethod
    def _gate(
        name: str,
        condition: bool,
        passed_reason: str,
        failed_reason: str,
    ) -> DemoGoLiveGateResult:
        """
        Build one deterministic gate result.
        """

        if condition:

            return DemoGoLiveValidator._pass(
                name=name,
                reason=passed_reason,
            )

        return DemoGoLiveValidator._fail(
            name=name,
            reason=failed_reason,
        )

    # -----------------------------------------------------
    # PASS
    # -----------------------------------------------------

    @staticmethod
    def _pass(
        name: str,
        reason: str,
    ) -> DemoGoLiveGateResult:
        """
        Create a successful gate result.
        """

        return DemoGoLiveGateResult(
            name=name,
            state=DemoGoLiveGateState.PASS,
            reason=reason,
        )

    # -----------------------------------------------------
    # FAIL
    # -----------------------------------------------------

    @staticmethod
    def _fail(
        name: str,
        reason: str,
    ) -> DemoGoLiveGateResult:
        """
        Create a failed gate result.
        """

        return DemoGoLiveGateResult(
            name=name,
            state=DemoGoLiveGateState.FAIL,
            reason=reason,
        )

    # -----------------------------------------------------
    # Runtime State
    # -----------------------------------------------------

    @staticmethod
    def _runtime_is_healthy(
        state: Any,
    ) -> bool:
        """
        Determine whether the supplied runtime state is
        safe for DEMO go-live.

        Only RUNNING is accepted.

        DEGRADED is intentionally rejected because the
        existing health policy requires trading to remain
        paused while degraded.
        """

        return (
            DemoGoLiveValidator._state_value(
                state
            )
            == "RUNNING"
        )

    # -----------------------------------------------------
    # State Value
    # -----------------------------------------------------

    @staticmethod
    def _state_value(
        value: Any,
    ) -> str:
        """
        Normalize Enum-like or string state values.
        """

        if value is None:

            return ""

        raw_value = getattr(
            value,
            "value",
            value,
        )

        return str(
            raw_value
        ).strip().upper()

    # -----------------------------------------------------
    # Symbol Normalization
    # -----------------------------------------------------

    @staticmethod
    def _normalize_symbols(
        symbols: Iterable[str] | None,
    ) -> tuple[str, ...]:
        """
        Normalize symbol collections while preserving
        input order and removing duplicates.
        """

        if symbols is None:

            return ()

        normalized: list[str] = []

        for symbol in symbols:

            if symbol is None:
                continue

            value = str(symbol).strip()

            if not value:
                continue

            if value not in normalized:

                normalized.append(value)

        return tuple(normalized)