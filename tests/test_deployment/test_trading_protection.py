"""
=================================================
Project Phoenix
Trading Protection Tests
M61.8.3 - Runtime Health Protection Policy
=================================================
"""

from deployment.runtime_watchdog import (
    WatchdogHealthState,
)

from deployment.trading_protection import (
    ProtectionTransition,
    TradingProtection,
    TradingProtectionState,
)


# =========================================================
# Test A
# Default State
# =========================================================

def test_trading_protection_default_state():

    protection = TradingProtection()

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )

    assert (
        protection.is_paused()
        is False
    )

    assert (
        protection.last_transition
        is None
    )


# =========================================================
# Test B
# Healthy Keeps Trading Active
# =========================================================

def test_trading_protection_healthy_active():

    protection = TradingProtection()

    result = protection.update(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        result
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )

    assert (
        protection.is_paused()
        is False
    )

    assert (
        protection.has_transitioned()
        is False
    )


# =========================================================
# Test C
# Healthy → Unhealthy
# =========================================================

def test_trading_protection_pauses_on_unhealthy():

    protection = TradingProtection()

    result = protection.update(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        result
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )

    assert (
        protection.is_paused()
        is True
    )

    assert (
        protection.has_transitioned()
        is True
    )

    assert (
        protection.last_transition
        == ProtectionTransition(
            previous_state=(
                TradingProtectionState.ACTIVE
            ),
            current_state=(
                TradingProtectionState.PAUSED
            ),
        )
    )


# =========================================================
# Test D
# Paused → Healthy Recovery
# =========================================================

def test_trading_protection_resumes_on_recovery():

    protection = TradingProtection()

    protection.update(
        WatchdogHealthState.UNHEALTHY,
    )

    protection.clear_transition()

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    result = protection.update(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        result
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )

    assert (
        protection.is_paused()
        is False
    )

    assert (
        protection.has_transitioned()
        is True
    )

    assert (
        protection.last_transition
        == ProtectionTransition(
            previous_state=(
                TradingProtectionState.PAUSED
            ),
            current_state=(
                TradingProtectionState.ACTIVE
            ),
        )
    )


# =========================================================
# Test E
# Repeated Unhealthy Does Not Create New Transition
# =========================================================

def test_trading_protection_repeated_unhealthy():

    protection = TradingProtection()

    protection.update(
        WatchdogHealthState.UNHEALTHY,
    )

    first_transition = (
        protection.last_transition
    )

    protection.update(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.last_transition
        is first_transition
    )

    assert (
        protection.can_trade()
        is False
    )


# =========================================================
# Test F
# Repeated Healthy Does Not Create New Transition
# =========================================================

def test_trading_protection_repeated_healthy():

    protection = TradingProtection()

    protection.update(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.last_transition
        is None
    )

    protection.update(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.last_transition
        is None
    )


# =========================================================
# Test G
# Clear Transition Does Not Change State
# =========================================================

def test_trading_protection_clear_transition():

    protection = TradingProtection()

    protection.update(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.last_transition
        is not None
    )

    protection.clear_transition()

    assert (
        protection.last_transition
        is None
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )


# =========================================================
# Test H
# Full Pause → Recovery Cycle
# =========================================================

def test_trading_protection_full_cycle():

    protection = TradingProtection()

    assert (
        protection.can_trade()
        is True
    )

    protection.update(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        protection.can_trade()
        is False
    )

    protection.clear_transition()

    protection.update(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        protection.can_trade()
        is True
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )