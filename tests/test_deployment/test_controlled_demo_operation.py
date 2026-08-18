"""
=================================================
Project Phoenix
Controlled Demo Operation Tests
M63.9
=================================================
"""

from datetime import datetime, timedelta, timezone

from deployment.controlled_demo_operation import (
    ControlledDemoOperation,
    ControlledDemoOperationState,
)


# =========================================================
# Test Doubles
# =========================================================

class FakeGoLiveResult:

    def __init__(
        self,
        ready: bool,
    ) -> None:

        self.ready = ready


class FakeProtection:

    def __init__(
        self,
        state="ACTIVE",
    ) -> None:

        self.state = state

    def can_trade(
        self,
    ) -> bool:

        return self.state == "ACTIVE"


class FakeExecutionSummary:

    def __init__(
        self,
    ) -> None:

        self.status = "NO_TRADES"

        self.executed = ()

        self.no_trade = ()

        self.failed = ()


class FakeTradingCycle:

    def __init__(
        self,
    ) -> None:

        self.execution_summary = (
            FakeExecutionSummary()
        )

        self.trade_records = []

        self.last_error = ""

        self.connected = True


class FakeRunner:

    def __init__(
        self,
    ) -> None:

        self.trading_protection = (
            FakeProtection()
        )

        self.trading_cycle = (
            FakeTradingCycle()
        )

        self.calls = 0

    def run_once(
        self,
    ) -> bool:

        self.calls += 1

        return True


# =========================================================
# Clock Helper
# =========================================================

class FakeClock:

    def __init__(
        self,
        current: datetime,
    ) -> None:

        self.current = current

    def __call__(
        self,
    ) -> datetime:

        return self.current

    def advance(
        self,
        **kwargs,
    ) -> None:

        self.current += timedelta(
            **kwargs
        )


# =========================================================
# Healthy Operation Factory
# =========================================================

def _operation(
    tmp_path,
    *,
    ready=True,
    observation_days=7,
    clock=None,
):

    return ControlledDemoOperation(
        runner=FakeRunner(),
        go_live_result=(
            FakeGoLiveResult(
                ready=ready
            )
        ),
        observation_days=observation_days,
        ledger_path=(
            tmp_path
            / "demo.jsonl"
        ),
        clock=clock,
    )


# =========================================================
# Start
# =========================================================

def test_start_requires_m63_8_ready(tmp_path):

    operation = _operation(
        tmp_path,
        ready=False,
    )

    try:

        operation.start()

    except RuntimeError as exc:

        assert (
            "M63.8"
            in str(exc)
        )

    else:

        raise AssertionError(
            "M63.9 must not start without M63.8 READY."
        )

    assert (
        operation.status().state
        == ControlledDemoOperationState.BLOCKED
    )


def test_start_accepts_m63_8_ready(tmp_path):

    operation = _operation(
        tmp_path,
        ready=True,
    )

    status = operation.start()

    assert status.active is True

    assert (
        status.state
        == ControlledDemoOperationState.ACTIVE
    )

    assert status.started_at is not None

    assert status.expires_at is not None


# =========================================================
# Observation Duration
# =========================================================

def test_observation_duration_must_be_at_least_seven_days(
    tmp_path,
):

    operation = _operation(
        tmp_path,
        observation_days=6,
    )

    try:

        operation.start()

    except ValueError:

        pass

    else:

        raise AssertionError(
            "M63.9 must reject observation periods shorter than 7 days."
        )


def test_observation_duration_must_not_exceed_ten_days(
    tmp_path,
):

    operation = _operation(
        tmp_path,
        observation_days=11,
    )

    try:

        operation.start()

    except ValueError:

        pass

    else:

        raise AssertionError(
            "M63.9 must reject observation periods longer than 10 days."
        )


def test_ten_day_observation_is_allowed(tmp_path):

    operation = _operation(
        tmp_path,
        observation_days=10,
    )

    status = operation.start()

    assert (
        status.observation_days
        == 10
    )


# =========================================================
# Cycle Execution
# =========================================================

def test_run_cycle_executes_existing_runner(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.start()

    event = operation.run_cycle()

    assert event.cycle_number == 1

    assert event.success is True

    assert (
        operation.runner.calls
        == 1
    )


def test_multiple_cycles_are_numbered_sequentially(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.start()

    first = operation.run_cycle()

    second = operation.run_cycle()

    assert first.cycle_number == 1

    assert second.cycle_number == 2

    assert (
        operation.status().cycle_count
        == 2
    )


# =========================================================
# Protection
# =========================================================

def test_cycle_records_trading_protection_state(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.start()

    event = operation.run_cycle()

    assert (
        event.trading_protection_state
        == "ACTIVE"
    )


def test_cycle_records_paused_protection_state(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.start()

    operation.runner.trading_protection.state = (
        "PAUSED"
    )

    event = operation.run_cycle()

    assert (
        event.trading_protection_state
        == "PAUSED"
    )


# =========================================================
# Execution Summary
# =========================================================

def test_cycle_records_execution_summary(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.runner.trading_cycle.execution_summary.status = (
        "ALL_EXECUTED"
    )

    operation.runner.trading_cycle.execution_summary.executed = (
        "EURUSDm",
        "XAUUSDm",
    )

    operation.runner.trading_cycle.trade_records = [
        type(
            "Trade",
            (),
            {
                "trade_id": "M63-001"
            },
        )()
    ]

    operation.start()

    event = operation.run_cycle()

    assert (
        event.cycle_status
        == "ALL_EXECUTED"
    )

    assert (
        event.executed_symbols
        == (
            "EURUSDm",
            "XAUUSDm",
        )
    )

    assert (
        event.trade_ids
        == (
            "M63-001",
        )
    )


# =========================================================
# Error Capture
# =========================================================

def test_cycle_records_cycle_error(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.runner.trading_cycle.last_error = (
        "EURUSDm: execution failed"
    )

    operation.start()

    event = operation.run_cycle()

    assert (
        "EURUSDm: execution failed"
        in event.errors
    )


# =========================================================
# Persistence
# =========================================================

def test_observation_event_is_persisted(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.start()

    operation.run_cycle()

    ledger = (
        tmp_path
        / "demo.jsonl"
    )

    assert ledger.exists()

    content = (
        ledger.read_text(
            encoding="utf-8"
        )
    )

    assert (
        '"cycle_number": 1'
        in content
    )

    assert (
        '"success": true'
        in content
    )


# =========================================================
# Expiration
# =========================================================

def test_operation_expires_after_observation_window(
    tmp_path,
):

    start_time = datetime(
        2026,
        8,
        18,
        tzinfo=timezone.utc,
    )

    clock = FakeClock(
        start_time
    )

    operation = _operation(
        tmp_path,
        observation_days=7,
        clock=clock,
    )

    operation.start()

    clock.advance(
        days=7
    )

    status = operation.status()

    assert (
        status.state
        == ControlledDemoOperationState.EXPIRED
    )

    assert status.expired is True


def test_expired_operation_cannot_run_cycle(
    tmp_path,
):

    start_time = datetime(
        2026,
        8,
        18,
        tzinfo=timezone.utc,
    )

    clock = FakeClock(
        start_time
    )

    operation = _operation(
        tmp_path,
        clock=clock,
    )

    operation.start()

    clock.advance(
        days=7
    )

    try:

        operation.run_cycle()

    except RuntimeError:

        pass

    else:

        raise AssertionError(
            "Expired M63.9 operation must not execute a cycle."
        )


# =========================================================
# Stop
# =========================================================

def test_stop_changes_operation_state(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.start()

    status = operation.stop()

    assert (
        status.state
        == ControlledDemoOperationState.STOPPED
    )


def test_stopped_operation_cannot_run_cycle(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    operation.start()

    operation.stop()

    try:

        operation.run_cycle()

    except RuntimeError:

        pass

    else:

        raise AssertionError(
            "Stopped M63.9 operation must not execute a cycle."
        )


# =========================================================
# Go-Live Result Preservation
# =========================================================

def test_go_live_result_is_preserved(
    tmp_path,
):

    operation = _operation(
        tmp_path,
        ready=True,
    )

    assert (
        operation.go_live_ready()
        is True
    )


def test_blocked_go_live_result_is_never_changed(
    tmp_path,
):

    operation = _operation(
        tmp_path,
        ready=False,
    )

    assert (
        operation.go_live_ready()
        is False
    )


# =========================================================
# No Strategy Mutation
# =========================================================

def test_operation_does_not_expose_strategy_mutation_api(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    assert not hasattr(
        operation,
        "modify_strategy",
    )

    assert not hasattr(
        operation,
        "update_strategy",
    )

    assert not hasattr(
        operation,
        "optimize_strategy",
    )


# =========================================================
# No AI Mutation
# =========================================================

def test_operation_does_not_expose_ai_mutation_api(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    assert not hasattr(
        operation,
        "modify_ai",
    )

    assert not hasattr(
        operation,
        "train_and_deploy",
    )


# =========================================================
# Status
# =========================================================

def test_initial_status_is_not_started(
    tmp_path,
):

    operation = _operation(
        tmp_path,
    )

    status = operation.status()

    assert (
        status.state
        == ControlledDemoOperationState.NOT_STARTED
    )

    assert status.cycle_count == 0

    assert status.event_count == 0