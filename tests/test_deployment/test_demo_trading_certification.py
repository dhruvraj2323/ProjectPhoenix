"""
=================================================
Project Phoenix
Final Demo Trading Certification Tests
M63.10
=================================================
"""

from datetime import datetime, timedelta, timezone

from deployment.demo_trading_certification import (
    DemoCertificationEvidence,
    DemoCertificationState,
    DemoCertificationGateState,
    DemoTradingCertification,
    build_certification_evidence,
)


# =========================================================
# Test Data
# =========================================================

ALL_GATES = (
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


STARTED_AT = datetime(
    2026,
    8,
    1,
    tzinfo=timezone.utc,
)


EXPIRES_AT = (
    STARTED_AT
    + timedelta(
        days=7
    )
)


def _evidence(
    *,
    m63_8_ready=True,
    m63_9_state="EXPIRED",
    observation_days=7,
    event_count=1,
    checklist=ALL_GATES,
):
    return DemoCertificationEvidence(
        m63_8_ready=m63_8_ready,
        m63_9_state=m63_9_state,
        observation_days=observation_days,
        observation_started_at=STARTED_AT,
        observation_expires_at=EXPIRES_AT,
        observation_event_count=event_count,
        checklist=tuple(
            checklist
        ),
    )


# =========================================================
# Full Certification
# =========================================================

def test_full_m63_10_evidence_certifies():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence()
    )

    assert (
        result.state
        == DemoCertificationState.CERTIFIED
    )

    assert result.certified is True

    assert result.blocked is False

    assert result.reasons == ()

    assert result.failed_gates == ()


# =========================================================
# M63.8
# =========================================================

def test_m63_8_not_ready_blocks_certification():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            m63_8_ready=False,
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )

    assert any(
        gate.name == "M63.8_GO_LIVE"
        and gate.state
        == DemoCertificationGateState.FAIL
        for gate in result.gates
    )


# =========================================================
# M63.9 Observation Duration
# =========================================================

def test_less_than_seven_days_blocks_certification():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            observation_days=6,
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )

    assert any(
        gate.name
        == "M63.9_OBSERVATION_PERIOD"
        and not gate.passed
        for gate in result.gates
    )


def test_exactly_seven_days_is_accepted():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            observation_days=7,
        )
    )

    assert (
        result.state
        == DemoCertificationState.CERTIFIED
    )


def test_ten_days_is_accepted():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            observation_days=10,
        )
    )

    assert (
        result.state
        == DemoCertificationState.CERTIFIED
    )


# =========================================================
# M63.9 Lifecycle
# =========================================================

def test_active_m63_9_operation_blocks_certification():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            m63_9_state="ACTIVE",
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )

    assert any(
        gate.name
        == "M63.9_COMPLETED"
        and not gate.passed
        for gate in result.gates
    )


def test_stopped_m63_9_operation_blocks_certification():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            m63_9_state="STOPPED",
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )


def test_blocked_m63_9_operation_blocks_certification():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            m63_9_state="BLOCKED",
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )


# =========================================================
# Observation Evidence
# =========================================================

def test_zero_observation_events_blocks_certification():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            event_count=0,
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )

    assert any(
        gate.name
        == "OBSERVATION_EVIDENCE"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Observation Timestamps
# =========================================================

def test_missing_start_timestamp_blocks_certification():

    evidence = _evidence()

    evidence = DemoCertificationEvidence(
        m63_8_ready=evidence.m63_8_ready,
        m63_9_state=evidence.m63_9_state,
        observation_days=evidence.observation_days,
        observation_started_at=None,
        observation_expires_at=evidence.observation_expires_at,
        observation_event_count=evidence.observation_event_count,
        checklist=evidence.checklist,
    )

    validator = DemoTradingCertification()

    result = validator.certify(
        evidence
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )


def test_missing_expiration_timestamp_blocks_certification():

    evidence = _evidence()

    evidence = DemoCertificationEvidence(
        m63_8_ready=evidence.m63_8_ready,
        m63_9_state=evidence.m63_9_state,
        observation_days=evidence.observation_days,
        observation_started_at=evidence.observation_started_at,
        observation_expires_at=None,
        observation_event_count=evidence.observation_event_count,
        checklist=evidence.checklist,
    )

    validator = DemoTradingCertification()

    result = validator.certify(
        evidence
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )


# =========================================================
# Checklist
# =========================================================

def test_missing_runtime_gate_blocks_certification():

    checklist = tuple(
        gate
        for gate in ALL_GATES
        if gate != "RUNTIME"
    )

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            checklist=checklist,
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )

    assert any(
        gate.name == "RUNTIME"
        and not gate.passed
        for gate in result.gates
    )


def test_missing_demo_guard_blocks_certification():

    checklist = tuple(
        gate
        for gate in ALL_GATES
        if gate != "MT5_DEMO_GUARD"
    )

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            checklist=checklist,
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )


def test_missing_reporting_gate_blocks_certification():

    checklist = tuple(
        gate
        for gate in ALL_GATES
        if gate != "REPORTING"
    )

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            checklist=checklist,
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )


def test_missing_recovery_gate_blocks_certification():

    checklist = tuple(
        gate
        for gate in ALL_GATES
        if gate != "RECOVERY"
    )

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            checklist=checklist,
        )
    )

    assert (
        result.state
        == DemoCertificationState.BLOCKED
    )


def test_all_required_gates_are_checked():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence()
    )

    gate_names = {
        gate.name
        for gate in result.gates
    }

    for required in ALL_GATES:

        assert required in gate_names


# =========================================================
# Case Normalization
# =========================================================

def test_checklist_values_are_case_insensitive():

    checklist = tuple(
        gate.lower()
        for gate in ALL_GATES
    )

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            checklist=checklist,
        )
    )

    assert (
        result.state
        == DemoCertificationState.CERTIFIED
    )


def test_blank_checklist_entries_are_ignored():

    checklist = (
        "",
        " ",
        *ALL_GATES,
    )

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            checklist=checklist,
        )
    )

    assert (
        result.state
        == DemoCertificationState.CERTIFIED
    )


# =========================================================
# Result Properties
# =========================================================

def test_certified_result_properties():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence()
    )

    assert result.certified is True

    assert result.blocked is False


def test_blocked_result_properties():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            m63_8_ready=False,
        )
    )

    assert result.certified is False

    assert result.blocked is True


def test_failed_gates_contains_only_failed_gates():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence(
            m63_8_ready=False,
        )
    )

    assert all(
        not gate.passed
        for gate in result.failed_gates
    )


# =========================================================
# Immutability
# =========================================================

def test_certification_result_is_immutable():

    validator = DemoTradingCertification()

    result = validator.certify(
        _evidence()
    )

    try:

        result.state = (
            DemoCertificationState.BLOCKED
        )

    except Exception:

        pass

    else:

        raise AssertionError(
            "Certification result must be immutable."
        )


# =========================================================
# No Operational APIs
# =========================================================

def test_certification_has_no_trading_api():

    validator = DemoTradingCertification()

    forbidden = (
        "send_order",
        "submit_order",
        "close_position",
        "modify_position",
        "start_runtime",
        "stop_runtime",
    )

    for name in forbidden:

        assert not hasattr(
            validator,
            name,
        )


# =========================================================
# M63.8 / M63.9 Evidence Builder
# =========================================================

class FakeM638Result:

    ready = True


class FakeM639Status:

    state = "EXPIRED"

    observation_days = 7

    started_at = STARTED_AT

    expires_at = EXPIRES_AT


def test_build_certification_evidence():

    evidence = build_certification_evidence(
        m63_8_result=FakeM638Result(),
        m63_9_status=FakeM639Status(),
        observation_event_count=5,
        checklist=ALL_GATES,
    )

    assert (
        evidence.m63_8_ready
        is True
    )

    assert (
        evidence.m63_9_state
        == "EXPIRED"
    )

    assert (
        evidence.observation_days
        == 7
    )

    assert (
        evidence.observation_event_count
        == 5
    )

    assert (
        evidence.checklist
        == ALL_GATES
    )


def test_build_evidence_with_blocked_m638():

    class BlockedResult:

        ready = False

    evidence = build_certification_evidence(
        m63_8_result=BlockedResult(),
        m63_9_status=FakeM639Status(),
        observation_event_count=5,
        checklist=ALL_GATES,
    )

    assert (
        evidence.m63_8_ready
        is False
    )


# =========================================================
# Final Safety Boundary
# =========================================================

def test_certification_does_not_modify_input_evidence():

    evidence = _evidence()

    original_checklist = evidence.checklist

    validator = DemoTradingCertification()

    validator.certify(
        evidence
    )

    assert (
        evidence.checklist
        == original_checklist
    )