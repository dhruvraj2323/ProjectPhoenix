"""
=================================================
Project Phoenix
Final Demo Trading Certification
M63.10
=================================================

Purpose
-------
Provide the final certification boundary for the
Project Phoenix Controlled Demo Trading V1.0 program.

M63.10 consumes evidence produced by:

    M63.8 - Demo Go-Live Validation
    M63.9 - Controlled Demo Operation

M63.10 does NOT:

- connect to MT5
- submit orders
- modify positions
- modify TradingProtection
- modify Risk Engine decisions
- modify Portfolio Engine decisions
- modify strategies
- modify AI decisions
- start Runtime
- stop Runtime
- replace ReportingEngine
- replace M63.8 validation
- replace M63.9 observation control

Certification is evidence-based.

The final certification can only become CERTIFIED when:

1. M63.8 is READY.
2. M63.9 completed its minimum observation period.
3. M63.9 observation evidence exists.
4. Every required certification gate passes.

Important
---------
A CERTIFIED result is a program-level certification result.
It is not a permanent MT5 authorization token.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable


# =========================================================
# Certification State
# =========================================================


class DemoCertificationState(str, Enum):
    """
    Final M63.10 certification state.
    """

    NOT_READY = "NOT_READY"

    BLOCKED = "BLOCKED"

    CERTIFIED = "CERTIFIED"


# =========================================================
# Certification Gate State
# =========================================================


class DemoCertificationGateState(str, Enum):
    """
    State of one M63.10 certification gate.
    """

    PASS = "PASS"

    FAIL = "FAIL"


# =========================================================
# Certification Gate
# =========================================================


@dataclass(frozen=True, slots=True)
class DemoCertificationGate:
    """
    Immutable result for one M63.10 certification gate.
    """

    name: str

    state: DemoCertificationGateState

    reason: str

    @property
    def passed(self) -> bool:
        """
        Return True when the gate passed.
        """

        return (
            self.state
            == DemoCertificationGateState.PASS
        )


# =========================================================
# Certification Evidence
# =========================================================


@dataclass(frozen=True, slots=True)
class DemoCertificationEvidence:
    """
    Evidence supplied to the final certification boundary.

    The evidence is intentionally supplied by the caller.
    M63.10 does not inspect or mutate external systems.
    """

    m63_8_ready: bool

    m63_9_state: Any

    observation_days: int

    observation_started_at: datetime | None

    observation_expires_at: datetime | None

    observation_event_count: int

    checklist: tuple[str, ...]


# =========================================================
# Final Certification Result
# =========================================================


@dataclass(frozen=True, slots=True)
class DemoCertificationResult:
    """
    Immutable final M63.10 certification result.
    """

    state: DemoCertificationState

    gates: tuple[
        DemoCertificationGate,
        ...,
    ]

    reasons: tuple[str, ...]

    certified_at: datetime

    @property
    def certified(self) -> bool:
        """
        Return True only when M63.10 is certified.
        """

        return (
            self.state
            == DemoCertificationState.CERTIFIED
        )

    @property
    def blocked(self) -> bool:
        """
        Return True when certification is blocked.
        """

        return (
            self.state
            == DemoCertificationState.BLOCKED
        )

    @property
    def failed_gates(
        self,
    ) -> tuple[
        DemoCertificationGate,
        ...,
    ]:
        """
        Return all failed certification gates.
        """

        return tuple(
            gate
            for gate in self.gates
            if not gate.passed
        )


# =========================================================
# Certification Validator
# =========================================================


class DemoTradingCertification:
    """
    M63.10 final certification boundary.

    The validator evaluates evidence from M63.8 and M63.9
    plus the final certification checklist.

    It does not perform operational actions.
    """

    MIN_OBSERVATION_DAYS = 7

    REQUIRED_GATES = (
        "RUNTIME",
        "CONFIGURATION",
        "DEPLOYMENT",
        "WATCHDOG",
        "PROTECTION",
        "STRATEGY",
        "RISK",
        "EXECUTION",
        "MT5_DEMO_GUARD",
        "ORDERS",
        "POSITIONS",
        "RECONCILIATION",
        "MULTI_SYMBOL",
        "REPORTING",
        "ALERTS",
        "RECOVERY",
        "DEMO_OPERATION",
    )

    # =====================================================
    # Public API
    # =====================================================

    def certify(
        self,
        evidence: DemoCertificationEvidence,
    ) -> DemoCertificationResult:
        """
        Evaluate final M63.10 certification evidence.

        Every required gate must pass.

        M63.8 READY is mandatory.

        M63.9 must have completed at least the minimum
        seven-day observation period.

        At least one observation event must exist.
        """

        gates: list[
            DemoCertificationGate
        ] = []

        reasons: list[str] = []

        # -------------------------------------------------
        # M63.8 prerequisite
        # -------------------------------------------------

        m63_8_gate = self._gate(
            name="M63.8_GO_LIVE",
            passed=evidence.m63_8_ready,
            passed_reason=(
                "M63.8 go-live validation is READY."
            ),
            failed_reason=(
                "M63.8 go-live validation is not READY."
            ),
        )

        gates.append(
            m63_8_gate
        )

        if not m63_8_gate.passed:

            reasons.append(
                m63_8_gate.reason
            )

        # -------------------------------------------------
        # M63.9 observation period
        # -------------------------------------------------

        observation_days_gate = self._gate(
            name="M63.9_OBSERVATION_PERIOD",
            passed=(
                evidence.observation_days
                >= self.MIN_OBSERVATION_DAYS
            ),
            passed_reason=(
                "M63.9 observation period meets "
                "the minimum seven-day requirement."
            ),
            failed_reason=(
                "M63.9 observation period is shorter "
                "than the required seven days."
            ),
        )

        gates.append(
            observation_days_gate
        )

        if not observation_days_gate.passed:

            reasons.append(
                observation_days_gate.reason
            )

        # -------------------------------------------------
        # M63.9 lifecycle state
        # -------------------------------------------------

        observation_state_passed = (
            self._is_completed_observation_state(
                evidence.m63_9_state
            )
        )

        observation_state_gate = self._gate(
            name="M63.9_COMPLETED",
            passed=observation_state_passed,
            passed_reason=(
                "M63.9 observation operation has "
                "completed its controlled lifecycle."
            ),
            failed_reason=(
                "M63.9 observation operation has not "
                "completed its controlled lifecycle."
            ),
        )

        gates.append(
            observation_state_gate
        )

        if not observation_state_gate.passed:

            reasons.append(
                observation_state_gate.reason
            )

        # -------------------------------------------------
        # Observation evidence
        # -------------------------------------------------

        evidence_gate = self._gate(
            name="OBSERVATION_EVIDENCE",
            passed=(
                evidence.observation_event_count
                > 0
            ),
            passed_reason=(
                "M63.9 observation evidence is present."
            ),
            failed_reason=(
                "No M63.9 observation evidence is present."
            ),
        )

        gates.append(
            evidence_gate
        )

        if not evidence_gate.passed:

            reasons.append(
                evidence_gate.reason
            )

        # -------------------------------------------------
        # Observation timestamps
        # -------------------------------------------------

        timestamps_gate = self._gate(
            name="OBSERVATION_TIMESTAMPS",
            passed=(
                evidence.observation_started_at
                is not None
                and
                evidence.observation_expires_at
                is not None
            ),
            passed_reason=(
                "M63.9 observation start and expiration "
                "timestamps are present."
            ),
            failed_reason=(
                "M63.9 observation timestamps are incomplete."
            ),
        )

        gates.append(
            timestamps_gate
        )

        if not timestamps_gate.passed:

            reasons.append(
                timestamps_gate.reason
            )

        # -------------------------------------------------
        # Required certification checklist
        # -------------------------------------------------

        checklist_values = {
            str(item).strip().upper()
            for item in evidence.checklist
            if str(item).strip()
        }

        for gate_name in self.REQUIRED_GATES:

            passed = (
                gate_name
                in checklist_values
            )

            gate = self._gate(
                name=gate_name,
                passed=passed,
                passed_reason=(
                    f"{gate_name} certification "
                    "evidence is present."
                ),
                failed_reason=(
                    f"{gate_name} certification "
                    "evidence is missing."
                ),
            )

            gates.append(
                gate
            )

            if not gate.passed:

                reasons.append(
                    gate.reason
                )

        # -------------------------------------------------
        # Final state
        # -------------------------------------------------

        all_passed = all(
            gate.passed
            for gate in gates
        )

        if all_passed:

            state = (
                DemoCertificationState.CERTIFIED
            )

        else:

            state = (
                DemoCertificationState.BLOCKED
            )

        return DemoCertificationResult(
            state=state,
            gates=tuple(gates),
            reasons=tuple(reasons),
            certified_at=datetime.now(
                timezone.utc
            ),
        )

    # =====================================================
    # Gate Helper
    # =====================================================

    @staticmethod
    def _gate(
        *,
        name: str,
        passed: bool,
        passed_reason: str,
        failed_reason: str,
    ) -> DemoCertificationGate:
        """
        Create one immutable certification gate.
        """

        if passed:

            return DemoCertificationGate(
                name=name,
                state=(
                    DemoCertificationGateState.PASS
                ),
                reason=passed_reason,
            )

        return DemoCertificationGate(
            name=name,
            state=(
                DemoCertificationGateState.FAIL
            ),
            reason=failed_reason,
        )

    # =====================================================
    # Observation State
    # =====================================================

    @staticmethod
    def _is_completed_observation_state(
        value: Any,
    ) -> bool:
        """
        Determine whether M63.9 has completed its controlled
        observation lifecycle.

        M63.9 currently reaches completion through EXPIRED.

        String values are accepted so certification remains
        decoupled from the M63.9 implementation class.
        """

        raw = getattr(
            value,
            "value",
            value,
        )

        normalized = str(
            raw
        ).strip().upper()

        return normalized == "EXPIRED"


# =========================================================
# Convenience Factory
# =========================================================


def build_certification_evidence(
    *,
    m63_8_result,
    m63_9_status,
    observation_event_count: int,
    checklist: Iterable[str],
) -> DemoCertificationEvidence:
    """
    Build M63.10 evidence from existing M63.8 and M63.9
    result/status objects.

    This helper performs no external I/O.
    """

    return DemoCertificationEvidence(
        m63_8_ready=bool(
            getattr(
                m63_8_result,
                "ready",
                False,
            )
        ),
        m63_9_state=getattr(
            m63_9_status,
            "state",
            "UNKNOWN",
        ),
        observation_days=int(
            getattr(
                m63_9_status,
                "observation_days",
                0,
            )
        ),
        observation_started_at=getattr(
            m63_9_status,
            "started_at",
            None,
        ),
        observation_expires_at=getattr(
            m63_9_status,
            "expires_at",
            None,
        ),
        observation_event_count=int(
            observation_event_count
        ),
        checklist=tuple(
            checklist
        ),
    )