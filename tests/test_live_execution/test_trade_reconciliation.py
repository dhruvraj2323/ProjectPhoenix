"""
=================================================
Project Phoenix
Test Trade Reconciliation
M63.4
=================================================
"""

from types import SimpleNamespace

from live_execution.trade_models import (
    ExecutionStatus,
)

from live_execution.trade_reconciliation import (
    ReconciliationStatus,
    TradeReconciler,
)


def _broker_object(
    ticket,
    volume,
):

    return SimpleNamespace(
        ticket=ticket,
        volume=volume,
    )


def _reconciler():

    return TradeReconciler()


# =========================================================
# Matching State
# =========================================================

def test_matching_order_position_state():

    result = _reconciler().reconcile(
        expected_ticket=1001,
        expected_volume=0.10,
        orders=[
            _broker_object(1001, 0.10),
        ],
        positions=[
            _broker_object(1001, 0.10),
        ],
        history=[],
    )

    assert result.status == (
        ReconciliationStatus.MATCHED
    )

    assert result.matched is True


# =========================================================
# Missing Order
# =========================================================

def test_missing_order_ticket():

    result = _reconciler().reconcile(
        expected_ticket=None,
        expected_volume=0.10,
        orders=[],
        positions=[],
        history=[],
    )

    assert result.status == (
        ReconciliationStatus.MISSING_ORDER
    )


# =========================================================
# Unexpected / Missing Position
# =========================================================

def test_expected_position_missing():

    result = _reconciler().reconcile(
        expected_ticket=1002,
        expected_volume=0.10,
        orders=[
            _broker_object(1002, 0.10),
        ],
        positions=[],
        history=[],
    )

    assert result.status == (
        ReconciliationStatus.UNEXPECTED_POSITION
    )


# =========================================================
# Duplicate Order
# =========================================================

def test_duplicate_order_detected():

    result = _reconciler().reconcile(
        expected_ticket=1003,
        expected_volume=0.10,
        orders=[
            _broker_object(1003, 0.10),
            _broker_object(1003, 0.10),
        ],
        positions=[
            _broker_object(1003, 0.10),
        ],
        history=[],
    )

    assert result.status == (
        ReconciliationStatus.DUPLICATE_ORDER
    )

    assert result.observed_volume == 0.20


# =========================================================
# Rejected Order
# =========================================================

def test_rejected_execution_detected():

    result = _reconciler().reconcile(
        expected_ticket=1004,
        expected_volume=0.10,
        orders=[],
        positions=[],
        history=[],
        execution_status=ExecutionStatus.REJECTED,
    )

    assert result.status == (
        ReconciliationStatus.REJECTED_ORDER
    )


# =========================================================
# Failed Execution
# =========================================================

def test_failed_execution_detected():

    result = _reconciler().reconcile(
        expected_ticket=1005,
        expected_volume=0.10,
        orders=[],
        positions=[],
        history=[],
        execution_status=ExecutionStatus.FAILED,
    )

    assert result.status == (
        ReconciliationStatus.REJECTED_ORDER
    )


# =========================================================
# Partial Execution
# =========================================================

def test_partial_execution_detected():

    result = _reconciler().reconcile(
        expected_ticket=1006,
        expected_volume=1.00,
        orders=[
            _broker_object(1006, 0.50),
        ],
        positions=[
            _broker_object(1006, 0.50),
        ],
        history=[],
    )

    assert result.status == (
        ReconciliationStatus.PARTIAL_EXECUTION
    )

    assert result.expected_volume == 1.00
    assert result.observed_volume == 0.50


# =========================================================
# Execution Volume Mismatch
# =========================================================

def test_execution_volume_mismatch_detected():

    result = _reconciler().reconcile(
        expected_ticket=1007,
        expected_volume=0.10,
        orders=[
            _broker_object(1007, 0.20),
        ],
        positions=[
            _broker_object(1007, 0.20),
        ],
        history=[],
    )

    assert result.status == (
        ReconciliationStatus.EXECUTION_MISMATCH
    )


# =========================================================
# Stale State
# =========================================================

def test_stale_state_detected():

    result = _reconciler().reconcile(
        expected_ticket=1008,
        expected_volume=0.10,
        orders=[],
        positions=[],
        history=[
            _broker_object(1008, 0.10),
        ],
    )

    assert result.status == (
        ReconciliationStatus.STALE_STATE
    )


# =========================================================
# Ticket Isolation
# =========================================================

def test_unrelated_ticket_does_not_match():

    result = _reconciler().reconcile(
        expected_ticket=1009,
        expected_volume=0.10,
        orders=[
            _broker_object(9999, 0.10),
        ],
        positions=[
            _broker_object(9999, 0.10),
        ],
        history=[],
    )

    assert result.status == (
        ReconciliationStatus.UNEXPECTED_POSITION
    )


# =========================================================
# Matching Volume
# =========================================================

def test_matching_volume_is_preserved():

    result = _reconciler().reconcile(
        expected_ticket=1010,
        expected_volume=0.30,
        orders=[
            _broker_object(1010, 0.30),
        ],
        positions=[
            _broker_object(1010, 0.30),
        ],
        history=[
            _broker_object(1010, 0.30),
        ],
    )

    assert result.status == (
        ReconciliationStatus.MATCHED
    )

    assert result.expected_ticket == 1010

    assert result.expected_volume == 0.30

    assert result.observed_volume == 0.30

    assert result.observed_order_count == 1

    assert result.observed_position_count == 1

    assert result.observed_history_count == 1