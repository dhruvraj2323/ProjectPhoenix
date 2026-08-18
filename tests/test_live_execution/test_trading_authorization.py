"""
=================================================
Project Phoenix
Test Trading Authorization
M63.1 - Demo Trading Authorization Boundary
=================================================
"""

from unittest.mock import MagicMock

from deployment.trading_protection import (
    TradingProtection,
    TradingProtectionState,
)

from live_execution.trading_authorization import (
    TradingAuthorization,
    TradingAuthorizationState,
)


# =========================================================
# Test A
# Default State
# =========================================================

def test_default_state_is_blocked():

    authorization = TradingAuthorization(
        protection=MagicMock(),
        demo_guard=MagicMock(),
    )

    assert (
        authorization.state
        == TradingAuthorizationState.BLOCKED
    )

    assert (
        authorization.can_trade()
        is False
    )

    assert (
        authorization.is_blocked()
        is True
    )


# =========================================================
# Test B
# Demo + Protection Active
# =========================================================

def test_demo_account_and_active_protection_authorize():

    protection = MagicMock()

    protection.can_trade.return_value = True

    demo_guard = MagicMock()

    demo_guard.validate.return_value = True

    authorization = TradingAuthorization(
        protection=protection,
        demo_guard=demo_guard,
    )

    assert (
        authorization.authorize()
        is True
    )

    assert (
        authorization.state
        == TradingAuthorizationState.AUTHORIZED
    )

    assert (
        authorization.can_trade()
        is True
    )

    assert (
        authorization.is_blocked()
        is False
    )

    protection.can_trade.assert_called_once()

    demo_guard.validate.assert_called_once()


# =========================================================
# Test C
# Protection Paused Blocks Trading
# =========================================================

def test_paused_protection_blocks_trading():

    protection = MagicMock()

    protection.can_trade.return_value = False

    demo_guard = MagicMock()

    authorization = TradingAuthorization(
        protection=protection,
        demo_guard=demo_guard,
    )

    assert (
        authorization.authorize()
        is False
    )

    assert (
        authorization.state
        == TradingAuthorizationState.BLOCKED
    )

    assert (
        authorization.can_trade()
        is False
    )

    demo_guard.validate.assert_not_called()


# =========================================================
# Test D
# Real Account Blocks Trading
# =========================================================

def test_real_account_blocks_trading():

    protection = MagicMock()

    protection.can_trade.return_value = True

    demo_guard = MagicMock()

    demo_guard.validate.side_effect = RuntimeError(
        "Live account detected. Trading aborted."
    )

    authorization = TradingAuthorization(
        protection=protection,
        demo_guard=demo_guard,
    )

    assert (
        authorization.authorize()
        is False
    )

    assert (
        authorization.state
        == TradingAuthorizationState.BLOCKED
    )

    assert (
        authorization.can_trade()
        is False
    )


# =========================================================
# Test E
# Account Validation Failure Blocks Trading
# =========================================================

def test_account_validation_failure_blocks_trading():

    protection = MagicMock()

    protection.can_trade.return_value = True

    demo_guard = MagicMock()

    demo_guard.validate.side_effect = RuntimeError(
        "MT5 account not available."
    )

    authorization = TradingAuthorization(
        protection=protection,
        demo_guard=demo_guard,
    )

    assert (
        authorization.authorize()
        is False
    )

    assert (
        authorization.is_blocked()
        is True
    )


# =========================================================
# Test F
# Successful Authorization Is Observable
# =========================================================

def test_successful_authorization_is_observable():

    protection = MagicMock()

    protection.can_trade.return_value = True

    demo_guard = MagicMock()

    demo_guard.validate.return_value = True

    authorization = TradingAuthorization(
        protection=protection,
        demo_guard=demo_guard,
    )

    authorization.authorize()

    assert (
        authorization.state
        == TradingAuthorizationState.AUTHORIZED
    )

    assert (
        authorization.can_trade()
        is True
    )


# =========================================================
# Test G
# Failed Authorization Can Recover
# =========================================================

def test_authorization_recovers_after_failure():

    protection = MagicMock()

    protection.can_trade.side_effect = [
        False,
        True,
    ]

    demo_guard = MagicMock()

    demo_guard.validate.return_value = True

    authorization = TradingAuthorization(
        protection=protection,
        demo_guard=demo_guard,
    )

    assert (
        authorization.authorize()
        is False
    )

    assert (
        authorization.state
        == TradingAuthorizationState.BLOCKED
    )

    assert (
        authorization.authorize()
        is True
    )

    assert (
        authorization.state
        == TradingAuthorizationState.AUTHORIZED
    )


# =========================================================
# Test H
# Protection Object Is Not Modified
# =========================================================

def test_authorization_does_not_modify_protection():

    protection = MagicMock()

    protection.can_trade.return_value = True

    demo_guard = MagicMock()

    demo_guard.validate.return_value = True

    authorization = TradingAuthorization(
        protection=protection,
        demo_guard=demo_guard,
    )

    authorization.authorize()

    protection.update.assert_not_called()


# =========================================================
# Test I
# Authorization Does Not Execute Trades
# =========================================================

def test_authorization_has_no_execution_side_effect():

    protection = MagicMock()

    protection.can_trade.return_value = True

    demo_guard = MagicMock()

    demo_guard.validate.return_value = True

    authorization = TradingAuthorization(
        protection=protection,
        demo_guard=demo_guard,
    )

    assert (
        authorization.authorize()
        is True
    )