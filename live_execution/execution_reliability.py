"""
=================================================
Project Phoenix
Execution Reliability
M63.5
=================================================

Purpose
-------
Provide a deterministic reliability boundary around
the existing M59 live execution result.

This module DOES NOT:

- submit orders
- retry orders
- modify positions
- close positions
- call MT5 order_send()
- replace TradeExecutor

It evaluates execution state and determines whether
Phoenix may consider the execution successful,
failed, or requiring recovery.

Safety principle
----------------
Unknown execution state is NEVER treated as success.

No automatic retry is performed.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from live_execution.trade_models import (
    ExecutionStatus,
    TradeResponse,
)


# =========================================================
# Reliability State
# =========================================================

class ExecutionReliabilityState(Enum):
    """
    Operational reliability state of an execution.
    """

    SUCCESS = "SUCCESS"

    FAILURE = "FAILURE"

    RECOVERY_REQUIRED = (
        "RECOVERY_REQUIRED"
    )

    BLOCKED = "BLOCKED"


# =========================================================
# Recovery Reason
# =========================================================

class ExecutionRecoveryReason(Enum):
    """
    Reason why execution cannot safely be treated
    as a completed and reconciled trade.
    """

    NONE = "NONE"

    EXECUTION_REJECTED = (
        "EXECUTION_REJECTED"
    )

    EXECUTION_FAILED = (
        "EXECUTION_FAILED"
    )

    UNKNOWN_EXECUTION_STATE = (
        "UNKNOWN_EXECUTION_STATE"
    )

    MISSING_TICKET = (
        "MISSING_TICKET"
    )

    ZERO_EXECUTED_VOLUME = (
        "ZERO_EXECUTED_VOLUME"
    )

    RECONCILIATION_REQUIRED = (
        "RECONCILIATION_REQUIRED"
    )


# =========================================================
# Reliability Result
# =========================================================

@dataclass(frozen=True)
class ExecutionReliabilityResult:
    """
    Immutable reliability decision.
    """

    state: ExecutionReliabilityState

    reason: ExecutionRecoveryReason

    message: str

    retry_allowed: bool = False

    execution_ticket: int | None = None

    executed_volume: float = 0.0

    @property
    def is_success(self) -> bool:

        return (
            self.state
            == ExecutionReliabilityState.SUCCESS
        )

    @property
    def requires_recovery(self) -> bool:

        return (
            self.state
            == ExecutionReliabilityState.RECOVERY_REQUIRED
        )

    @property
    def is_blocked(self) -> bool:

        return (
            self.state
            == ExecutionReliabilityState.BLOCKED
        )


# =========================================================
# Execution Reliability Evaluator
# =========================================================

class ExecutionReliability:
    """
    Evaluates an existing Phoenix TradeResponse.

    This is intentionally a pure decision boundary.

    It never retries execution.
    """

    def evaluate(
        self,
        response: TradeResponse | None,
    ) -> ExecutionReliabilityResult:

        # -------------------------------------------------
        # No response
        #
        # We cannot know whether MT5 accepted the order.
        # Therefore this is an unsafe unknown state.
        # -------------------------------------------------

        if response is None:

            return (
                self._blocked(
                    reason=(
                        ExecutionRecoveryReason
                        .UNKNOWN_EXECUTION_STATE
                    ),
                    message=(
                        "No TradeResponse was returned. "
                        "Execution state is unknown. "
                        "Further execution is blocked."
                    ),
                )
            )

        status = response.status

        # -------------------------------------------------
        # Explicit successful execution
        # -------------------------------------------------

        if status == ExecutionStatus.EXECUTED:

            # A successful execution without a broker
            # ticket cannot safely be reconciled.

            if response.ticket is None:

                return (
                    self._recovery_required(
                        reason=(
                            ExecutionRecoveryReason
                            .MISSING_TICKET
                        ),
                        message=(
                            "Execution reported success "
                            "but broker ticket is missing. "
                            "Reconciliation is required."
                        ),
                        response=response,
                    )
                )

            # Successful execution with zero volume is
            # not a trustworthy completed trade.

            if response.executed_volume <= 0:

                return (
                    self._recovery_required(
                        reason=(
                            ExecutionRecoveryReason
                            .ZERO_EXECUTED_VOLUME
                        ),
                        message=(
                            "Execution reported success "
                            "but executed volume is zero. "
                            "Reconciliation is required."
                        ),
                        response=response,
                    )
                )

            return (
                ExecutionReliabilityResult(
                    state=(
                        ExecutionReliabilityState.SUCCESS
                    ),
                    reason=(
                        ExecutionRecoveryReason.NONE
                    ),
                    message=(
                        "Execution completed successfully. "
                        "Broker ticket and executed volume "
                        "are present."
                    ),
                    retry_allowed=False,
                    execution_ticket=response.ticket,
                    executed_volume=(
                        response.executed_volume
                    ),
                )
            )

        # -------------------------------------------------
        # Explicit rejection
        # -------------------------------------------------

        if status == ExecutionStatus.REJECTED:

            return (
                self._failure(
                    reason=(
                        ExecutionRecoveryReason
                        .EXECUTION_REJECTED
                    ),
                    message=(
                        response.broker_message
                        or
                        "Broker rejected the execution."
                    ),
                    response=response,
                )
            )

        # -------------------------------------------------
        # Explicit failure
        # -------------------------------------------------

        if status == ExecutionStatus.FAILED:

            return (
                self._failure(
                    reason=(
                        ExecutionRecoveryReason
                        .EXECUTION_FAILED
                    ),
                    message=(
                        response.broker_message
                        or
                        "Execution failed."
                    ),
                    response=response,
                )
            )

        # -------------------------------------------------
        # PENDING / unknown
        #
        # NEVER retry automatically.
        # -------------------------------------------------

        return (
            self._blocked(
                reason=(
                    ExecutionRecoveryReason
                    .UNKNOWN_EXECUTION_STATE
                ),
                message=(
                    f"Execution status "
                    f"{status!s} is not a confirmed "
                    "terminal state. Further execution "
                    "is blocked."
                ),
                response=response,
            )
        )

    # =====================================================
    # Context Integration
    # =====================================================

    def evaluate_context(
        self,
        context,
    ) -> ExecutionReliabilityResult:
        """
        Evaluate context.trade_response and store the
        reliability decision in context.metadata.

        Metadata failure must never replace the
        reliability decision itself.
        """

        result = self.evaluate(
            context.trade_response
        )

        try:

            context.metadata[
                "execution_reliability_state"
            ] = result.state.value

            context.metadata[
                "execution_reliability_reason"
            ] = result.reason.value

            context.metadata[
                "execution_reliability_message"
            ] = result.message

            context.metadata[
                "execution_retry_allowed"
            ] = result.retry_allowed

            context.metadata[
                "execution_recovery_required"
            ] = result.requires_recovery

            context.metadata[
                "execution_ticket"
            ] = result.execution_ticket

        except Exception:
            # Metadata is diagnostic only.
            pass

        return result

    # =====================================================
    # Explicit Recovery Completion
    # =====================================================

    def mark_recovered(
        self,
        context,
        message: str = (
            "Execution recovery completed."
        ),
    ) -> ExecutionReliabilityResult:
        """
        Mark a previously unsafe execution boundary as
        recovered.

        This method does NOT retry or submit an order.

        The caller must have independently established
        the broker state, normally through reconciliation.
        """

        result = ExecutionReliabilityResult(
            state=(
                ExecutionReliabilityState.SUCCESS
            ),
            reason=(
                ExecutionRecoveryReason.NONE
            ),
            message=message,
            retry_allowed=False,
            execution_ticket=(
                getattr(
                    context.trade_response,
                    "ticket",
                    None,
                )
                if context.trade_response
                else None
            ),
            executed_volume=(
                getattr(
                    context.trade_response,
                    "executed_volume",
                    0.0,
                )
                if context.trade_response
                else 0.0
            ),
        )

        try:

            context.metadata[
                "execution_recovery_completed"
            ] = True

            context.metadata[
                "execution_recovery_message"
            ] = message

            context.metadata[
                "execution_reliability_state"
            ] = result.state.value

        except Exception:
            pass

        return result

    # =====================================================
    # Internal Builders
    # =====================================================

    @staticmethod
    def _failure(
        reason: ExecutionRecoveryReason,
        message: str,
        response: TradeResponse,
    ) -> ExecutionReliabilityResult:

        return ExecutionReliabilityResult(
            state=(
                ExecutionReliabilityState.FAILURE
            ),
            reason=reason,
            message=message,
            retry_allowed=False,
            execution_ticket=response.ticket,
            executed_volume=(
                response.executed_volume
            ),
        )

    @staticmethod
    def _recovery_required(
        reason: ExecutionRecoveryReason,
        message: str,
        response: TradeResponse,
    ) -> ExecutionReliabilityResult:

        return ExecutionReliabilityResult(
            state=(
                ExecutionReliabilityState
                .RECOVERY_REQUIRED
            ),
            reason=reason,
            message=message,
            retry_allowed=False,
            execution_ticket=response.ticket,
            executed_volume=(
                response.executed_volume
            ),
        )

    @staticmethod
    def _blocked(
        reason: ExecutionRecoveryReason,
        message: str,
        response: TradeResponse | None = None,
    ) -> ExecutionReliabilityResult:

        return ExecutionReliabilityResult(
            state=(
                ExecutionReliabilityState.BLOCKED
            ),
            reason=reason,
            message=message,
            retry_allowed=False,
            execution_ticket=(
                response.ticket
                if response is not None
                else None
            ),
            executed_volume=(
                response.executed_volume
                if response is not None
                else 0.0
            ),
        )