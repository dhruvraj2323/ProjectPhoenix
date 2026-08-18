"""
=================================================
Project Phoenix
Test Execution Reliability
M63.5
=================================================
"""

from live_execution.execution_reliability import (
    ExecutionRecoveryReason,
    ExecutionReliability,
    ExecutionReliabilityState,
)

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_models import (
    ExecutionStatus,
    TradeResponse,
)


def _response(
    status,
    ticket=123456,
    volume=0.10,
    message="Executed",
):

    return TradeResponse(
        status=status,
        ticket=ticket,
        executed_price=1.1000,
        executed_volume=volume,
        broker_message=message,
        retcode=0,
    )


def _context(response):

    context = TradeContext(
        execution_id="EXEC-M63.5",
        symbol="EURUSDm",
        timeframe="M15",
    )

    context.trade_response = response

    return context


# =========================================================
# 1. Successful execution
# =========================================================

def test_executed_trade_is_reliable_success():

    result = (
        ExecutionReliability()
        .evaluate(
            _response(
                ExecutionStatus.EXECUTED
            )
        )
    )

    assert (
        result.state
        == ExecutionReliabilityState.SUCCESS
    )

    assert (
        result.reason
        == ExecutionRecoveryReason.NONE
    )

    assert result.is_success is True

    assert result.retry_allowed is False

    assert result.execution_ticket == 123456

    assert result.executed_volume == 0.10


# =========================================================
# 2. Rejected execution
# =========================================================

def test_rejected_trade_is_failure():

    result = (
        ExecutionReliability()
        .evaluate(
            _response(
                ExecutionStatus.REJECTED,
                message="Broker rejected",
            )
        )
    )

    assert (
        result.state
        == ExecutionReliabilityState.FAILURE
    )

    assert (
        result.reason
        == ExecutionRecoveryReason
        .EXECUTION_REJECTED
    )

    assert result.retry_allowed is False


# =========================================================
# 3. Failed execution
# =========================================================

def test_failed_trade_is_failure():

    result = (
        ExecutionReliability()
        .evaluate(
            _response(
                ExecutionStatus.FAILED,
                message="Execution failed",
            )
        )
    )

    assert (
        result.state
        == ExecutionReliabilityState.FAILURE
    )

    assert (
        result.reason
        == ExecutionRecoveryReason
        .EXECUTION_FAILED
    )

    assert result.retry_allowed is False


# =========================================================
# 4. Missing response
# =========================================================

def test_missing_response_blocks_execution():

    result = (
        ExecutionReliability()
        .evaluate(None)
    )

    assert (
        result.state
        == ExecutionReliabilityState.BLOCKED
    )

    assert (
        result.reason
        == ExecutionRecoveryReason
        .UNKNOWN_EXECUTION_STATE
    )

    assert result.is_blocked is True

    assert result.retry_allowed is False


# =========================================================
# 5. Pending response
# =========================================================

def test_pending_execution_is_blocked():

    result = (
        ExecutionReliability()
        .evaluate(
            _response(
                ExecutionStatus.PENDING
            )
        )
    )

    assert (
        result.state
        == ExecutionReliabilityState.BLOCKED
    )

    assert (
        result.reason
        == ExecutionRecoveryReason
        .UNKNOWN_EXECUTION_STATE
    )

    assert result.retry_allowed is False


# =========================================================
# 6. Successful execution without ticket
# =========================================================

def test_success_without_ticket_requires_recovery():

    result = (
        ExecutionReliability()
        .evaluate(
            _response(
                ExecutionStatus.EXECUTED,
                ticket=None,
                volume=0.10,
            )
        )
    )

    assert (
        result.state
        == ExecutionReliabilityState
        .RECOVERY_REQUIRED
    )

    assert (
        result.reason
        == ExecutionRecoveryReason
        .MISSING_TICKET
    )

    assert result.requires_recovery is True

    assert result.retry_allowed is False


# =========================================================
# 7. Successful execution with zero volume
# =========================================================

def test_success_with_zero_volume_requires_recovery():

    result = (
        ExecutionReliability()
        .evaluate(
            _response(
                ExecutionStatus.EXECUTED,
                ticket=123456,
                volume=0.0,
            )
        )
    )

    assert (
        result.state
        == ExecutionReliabilityState
        .RECOVERY_REQUIRED
    )

    assert (
        result.reason
        == ExecutionRecoveryReason
        .ZERO_EXECUTED_VOLUME
    )

    assert result.retry_allowed is False


# =========================================================
# 8. Context metadata integration
# =========================================================

def test_context_reliability_metadata():

    response = _response(
        ExecutionStatus.EXECUTED
    )

    context = _context(
        response
    )

    result = (
        ExecutionReliability()
        .evaluate_context(
            context
        )
    )

    assert result.is_success is True

    assert (
        context.metadata[
            "execution_reliability_state"
        ]
        == "SUCCESS"
    )

    assert (
        context.metadata[
            "execution_reliability_reason"
        ]
        == "NONE"
    )

    assert (
        context.metadata[
            "execution_retry_allowed"
        ]
        is False
    )

    assert (
        context.metadata[
            "execution_ticket"
        ]
        == 123456
    )


# =========================================================
# 9. Failed execution metadata
# =========================================================

def test_failed_execution_metadata():

    context = _context(
        _response(
            ExecutionStatus.FAILED,
            message="Broker failure",
        )
    )

    result = (
        ExecutionReliability()
        .evaluate_context(
            context
        )
    )

    assert (
        result.state
        == ExecutionReliabilityState.FAILURE
    )

    assert (
        context.metadata[
            "execution_reliability_state"
        ]
        == "FAILURE"
    )

    assert (
        context.metadata[
            "execution_retry_allowed"
        ]
        is False
    )


# =========================================================
# 10. Explicit recovery
# =========================================================

def test_recovery_can_be_marked_without_retry():

    context = _context(
        _response(
            ExecutionStatus.EXECUTED
        )
    )

    reliability = (
        ExecutionReliability()
    )

    result = reliability.mark_recovered(
        context
    )

    assert (
        result.state
        == ExecutionReliabilityState.SUCCESS
    )

    assert result.retry_allowed is False

    assert (
        context.metadata[
            "execution_recovery_completed"
        ]
        is True
    )

    assert (
        context.metadata[
            "execution_reliability_state"
        ]
        == "SUCCESS"
    )


# =========================================================
# 11. Rejected execution never permits retry
# =========================================================

def test_rejected_execution_never_allows_retry():

    result = (
        ExecutionReliability()
        .evaluate(
            _response(
                ExecutionStatus.REJECTED
            )
        )
    )

    assert result.retry_allowed is False


# =========================================================
# 12. Unknown state never permits retry
# =========================================================

def test_unknown_state_never_allows_retry():

    response = _response(
        ExecutionStatus.PENDING
    )

    result = (
        ExecutionReliability()
        .evaluate(response)
    )

    assert result.retry_allowed is False

    assert result.is_blocked is True