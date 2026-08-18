"""
=================================================
Project Phoenix
Demo Go-Live Validation Tests
M63.8
=================================================
"""

from dataclasses import replace

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.trading_protection import (
    TradingProtectionState,
)

from live_execution.demo_go_live_validation import (
    DemoGoLiveGateState,
    DemoGoLiveValidationSnapshot,
    DemoGoLiveValidationState,
    DemoGoLiveValidator,
)


# =========================================================
# Helpers
# =========================================================

def _ready_snapshot() -> DemoGoLiveValidationSnapshot:
    """
    Build a completely healthy M63.8 snapshot.
    """

    return DemoGoLiveValidationSnapshot(
        mt5_connected=True,
        account_available=True,
        demo_account_confirmed=True,
        configured_symbols=(
            "EURUSDm",
            "XAUUSDm",
            "BTCUSDm",
        ),
        healthy_symbols=(
            "EURUSDm",
            "XAUUSDm",
            "BTCUSDm",
        ),
        market_data_healthy=True,
        runtime_state=(
            RuntimeOperationalState.RUNNING
        ),
        trading_protection_state=(
            TradingProtectionState.ACTIVE
        ),
        risk_approved=True,
        execution_healthy=True,
        reconciliation_healthy=True,
        reporting_healthy=True,
    )


# =========================================================
# All Gates Pass
# =========================================================

def test_all_gates_pass_for_healthy_demo_snapshot():

    validator = DemoGoLiveValidator()

    result = validator.validate(
        _ready_snapshot()
    )

    assert (
        result.state
        == DemoGoLiveValidationState.READY
    )

    assert result.ready is True

    assert result.blocked is False

    assert result.reasons == ()

    assert len(result.gates) == 11

    assert all(
        gate.state
        == DemoGoLiveGateState.PASS
        for gate in result.gates
    )


# =========================================================
# MT5 Connection
# =========================================================

def test_mt5_connection_failure_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        mt5_connected=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "MT5_CONNECTION"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Account
# =========================================================

def test_missing_account_information_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        account_available=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "ACCOUNT"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Critical Real Account Safety Boundary
# =========================================================

def test_real_account_always_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        demo_account_confirmed=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.state == (
        DemoGoLiveValidationState.BLOCKED
    )

    assert result.blocked is True

    demo_gate = next(
        gate
        for gate in result.gates
        if gate.name == "DEMO_ACCOUNT"
    )

    assert demo_gate.passed is False

    assert (
        "DEMO trading is blocked"
        in demo_gate.reason
    )


# =========================================================
# Missing Symbols
# =========================================================

def test_missing_required_symbol_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        healthy_symbols=(
            "EURUSDm",
            "XAUUSDm",
        ),
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "SYMBOLS"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Market Data
# =========================================================

def test_unhealthy_market_data_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        market_data_healthy=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "MARKET_DATA"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Runtime
# =========================================================

def test_degraded_runtime_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        runtime_state=(
            RuntimeOperationalState.DEGRADED
        ),
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "RUNTIME"
        and not gate.passed
        for gate in result.gates
    )


def test_stopped_runtime_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        runtime_state=(
            RuntimeOperationalState.STOPPED
        ),
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True


# =========================================================
# Trading Protection
# =========================================================

def test_paused_trading_protection_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        trading_protection_state=(
            TradingProtectionState.PAUSED
        ),
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "TRADING_PROTECTION"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Risk
# =========================================================

def test_risk_rejection_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        risk_approved=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "RISK"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Execution
# =========================================================

def test_unhealthy_execution_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        execution_healthy=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "EXECUTION"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Reconciliation
# =========================================================

def test_unhealthy_reconciliation_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        reconciliation_healthy=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "RECONCILIATION"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Reporting
# =========================================================

def test_unhealthy_reporting_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        reporting_healthy=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    assert any(
        gate.name == "REPORTING"
        and not gate.passed
        for gate in result.gates
    )


# =========================================================
# Multiple Failures
# =========================================================

def test_multiple_failed_gates_are_preserved():

    snapshot = replace(
        _ready_snapshot(),
        mt5_connected=False,
        risk_approved=False,
        reporting_healthy=False,
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True

    failed_names = {
        gate.name
        for gate in result.failed_gates
    }

    assert "MT5_CONNECTION" in failed_names

    assert "RISK" in failed_names

    assert "REPORTING" in failed_names

    assert len(result.reasons) == 3


# =========================================================
# Empty Symbols
# =========================================================

def test_empty_symbol_configuration_blocks_go_live():

    snapshot = replace(
        _ready_snapshot(),
        configured_symbols=(),
        healthy_symbols=(),
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.blocked is True


# =========================================================
# Duplicate Symbols
# =========================================================

def test_duplicate_symbols_do_not_create_duplicate_gate_failure():

    snapshot = replace(
        _ready_snapshot(),
        configured_symbols=(
            "EURUSDm",
            "EURUSDm",
            "XAUUSDm",
            "BTCUSDm",
        ),
        healthy_symbols=(
            "EURUSDm",
            "XAUUSDm",
            "BTCUSDm",
        ),
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.ready is True


# =========================================================
# Validation Result Immutability
# =========================================================

def test_validation_result_is_immutable():

    result = DemoGoLiveValidator().validate(
        _ready_snapshot()
    )

    try:

        result.state = (
            DemoGoLiveValidationState.BLOCKED
        )

    except (
        AttributeError,
        TypeError,
    ):

        pass

    else:

        raise AssertionError(
            "Validation result must be immutable."
        )


# =========================================================
# Snapshot Immutability
# =========================================================

def test_validation_snapshot_is_immutable():

    snapshot = _ready_snapshot()

    try:

        snapshot.mt5_connected = False

    except (
        AttributeError,
        TypeError,
    ):

        pass

    else:

        raise AssertionError(
            "Validation snapshot must be immutable."
        )


# =========================================================
# No Trading Execution API
# =========================================================

def test_validator_result_does_not_create_trade_execution_api():

    result = DemoGoLiveValidator().validate(
        _ready_snapshot()
    )

    assert not hasattr(
        result,
        "execute_trade",
    )

    assert not hasattr(
        result,
        "send_order",
    )

    assert not hasattr(
        result,
        "modify_position",
    )

    assert not hasattr(
        result,
        "close_position",
    )


# =========================================================
# Degraded Runtime Must Never Be Ready
# =========================================================

def test_degraded_runtime_is_never_treated_as_go_live_ready():

    snapshot = replace(
        _ready_snapshot(),
        runtime_state=(
            RuntimeOperationalState.DEGRADED
        ),
    )

    result = DemoGoLiveValidator().validate(
        snapshot
    )

    assert result.ready is False

    assert result.blocked is True