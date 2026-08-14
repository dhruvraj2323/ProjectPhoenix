"""
=================================================
Project Phoenix
Health Degradation Integration Tests
M62.4.2 - Health Degradation Integration
=================================================
"""

from unittest.mock import MagicMock

from deployment.health_degradation_policy import (
    HealthDegradationPolicy,
    HealthImpact,
)

from deployment.runtime_operational_state import (
    RuntimeOperationalState,
)

from deployment.runtime_watchdog import (
    RuntimeWatchdog,
    WatchdogHealthState,
)

from deployment.trading_protection import (
    TradingProtection,
    TradingProtectionState,
)


def _create_watchdog(
    health_sequence,
):
    monitor = MagicMock()

    monitor.is_healthy.side_effect = (
        health_sequence
    )

    return RuntimeWatchdog(
        health_monitor=monitor,
    )


# =========================================================
# Test A
# Healthy Watchdog Produces Healthy Policy
# =========================================================

def test_healthy_watchdog_produces_healthy_policy():

    watchdog = _create_watchdog(
        [True]
    )

    policy = HealthDegradationPolicy()

    health_state = watchdog.check()

    decision = policy.evaluate(
        health_state,
    )

    assert (
        health_state
        == WatchdogHealthState.HEALTHY
    )

    assert (
        decision.impact
        == HealthImpact.HEALTHY
    )

    assert (
        decision.runtime_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        decision.trading_paused
        is False
    )


# =========================================================
# Test B
# Unhealthy Watchdog Produces Degraded Policy
# =========================================================

def test_unhealthy_watchdog_produces_degraded_policy():

    watchdog = _create_watchdog(
        [False]
    )

    policy = HealthDegradationPolicy()

    health_state = watchdog.check()

    decision = policy.evaluate(
        health_state,
    )

    assert (
        health_state
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        decision.impact
        == HealthImpact.DEGRADED
    )

    assert (
        decision.runtime_state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        decision.trading_paused
        is True
    )


# =========================================================
# Test C
# Watchdog Unhealthy → Trading Protection Paused
# =========================================================

def test_unhealthy_watchdog_pauses_trading_protection():

    watchdog = _create_watchdog(
        [False]
    )

    policy = HealthDegradationPolicy()

    protection = TradingProtection()

    health_state = watchdog.check()

    decision = policy.evaluate(
        health_state,
    )

    protection.update(
        health_state,
    )

    assert (
        decision.degraded
        is True
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


# =========================================================
# Test D
# Healthy State Keeps Trading Active
# =========================================================

def test_healthy_watchdog_keeps_trading_active():

    watchdog = _create_watchdog(
        [True]
    )

    policy = HealthDegradationPolicy()

    protection = TradingProtection()

    health_state = watchdog.check()

    decision = policy.evaluate(
        health_state,
    )

    protection.update(
        health_state,
    )

    assert (
        decision.degraded
        is False
    )

    assert (
        decision.trading_paused
        is False
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )


# =========================================================
# Test E
# Full Unhealthy → Recovery Cycle
# =========================================================

def test_full_unhealthy_to_recovery_cycle():

    watchdog = _create_watchdog(
        [False, True]
    )

    policy = HealthDegradationPolicy()

    protection = TradingProtection()

    # ----------------------------------------------
    # Degradation
    # ----------------------------------------------

    first_health = watchdog.check()

    first_decision = policy.evaluate(
        first_health,
    )

    protection.update(
        first_health,
    )

    assert (
        first_health
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        first_decision.runtime_state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )

    # ----------------------------------------------
    # Clear old transitions
    # ----------------------------------------------

    watchdog.clear_transition()

    protection.clear_transition()

    # ----------------------------------------------
    # Recovery
    # ----------------------------------------------

    second_health = watchdog.check()

    second_decision = policy.evaluate(
        second_health,
    )

    protection.update(
        second_health,
    )

    assert (
        second_health
        == WatchdogHealthState.HEALTHY
    )

    assert (
        watchdog.has_recovered()
        is True
    )

    assert (
        second_decision.runtime_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        second_decision.degraded
        is False
    )

    assert (
        second_decision.recovered
        is True
    )

    assert (
        protection.state
        == TradingProtectionState.ACTIVE
    )

    assert (
        protection.can_trade()
        is True
    )


# =========================================================
# Test F
# Repeated Unhealthy Does Not Create New Watchdog
# Transition
# =========================================================

def test_repeated_unhealthy_preserves_watchdog_transition():

    watchdog = _create_watchdog(
        [False, False]
    )

    policy = HealthDegradationPolicy()

    first_health = watchdog.check()

    first_decision = policy.evaluate(
        first_health,
    )

    first_transition = (
        watchdog.last_transition
    )

    second_health = watchdog.check()

    second_decision = policy.evaluate(
        second_health,
    )

    assert (
        first_decision.runtime_state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        second_decision.runtime_state
        == RuntimeOperationalState.DEGRADED
    )

    assert (
        watchdog.last_transition
        is first_transition
    )

    assert (
        watchdog.has_recovered()
        is False
    )


# =========================================================
# Test G
# Repeated Unhealthy Keeps Trading Paused
# =========================================================

def test_repeated_unhealthy_keeps_trading_paused():

    watchdog = _create_watchdog(
        [False, False]
    )

    policy = HealthDegradationPolicy()

    protection = TradingProtection()

    first_health = watchdog.check()

    first_decision = policy.evaluate(
        first_health,
    )

    protection.update(
        first_health,
    )

    first_transition = (
        protection.last_transition
    )

    second_health = watchdog.check()

    second_decision = policy.evaluate(
        second_health,
    )

    protection.update(
        second_health,
    )

    assert (
        first_decision.trading_paused
        is True
    )

    assert (
        second_decision.trading_paused
        is True
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
        protection.last_transition
        is first_transition
    )


# =========================================================
# Test H
# Recovery Requires Healthy Watchdog State
# =========================================================

def test_recovery_requires_healthy_watchdog_state():

    watchdog = _create_watchdog(
        [False, False]
    )

    policy = HealthDegradationPolicy()

    protection = TradingProtection()

    first_health = watchdog.check()

    protection.update(
        first_health,
    )

    watchdog.clear_transition()

    second_health = watchdog.check()

    decision = policy.evaluate(
        second_health,
    )

    protection.update(
        second_health,
    )

    assert (
        second_health
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        decision.recovered
        is False
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
# Test I
# Policy Does Not Control TradingProtection Directly
# =========================================================

def test_policy_does_not_control_trading_protection_directly():

    watchdog = _create_watchdog(
        [False]
    )

    policy = HealthDegradationPolicy()

    protection = MagicMock()

    health_state = watchdog.check()

    decision = policy.evaluate(
        health_state,
    )

    assert (
        decision.trading_paused
        is True
    )

    protection.update.assert_not_called()


# =========================================================
# Test J
# Policy Does Not Control Watchdog
# =========================================================

def test_policy_does_not_control_watchdog():

    watchdog = _create_watchdog(
        [False]
    )

    policy = HealthDegradationPolicy()

    watchdog.check()

    watchdog.clear_transition = MagicMock()

    policy.evaluate(
        watchdog.state,
    )

    watchdog.clear_transition.assert_not_called()


# =========================================================
# Test K
# Policy Does Not Stop Runtime
# =========================================================

def test_policy_does_not_stop_runtime():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        decision.runtime_state
        == RuntimeOperationalState.DEGRADED
    )

    assert not hasattr(
        decision,
        "stop_runtime",
    )


# =========================================================
# Test L
# Policy Does Not Restart Runtime
# =========================================================

def test_policy_does_not_restart_runtime():

    policy = HealthDegradationPolicy()

    decision = policy.evaluate(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        decision.runtime_state
        == RuntimeOperationalState.RUNNING
    )

    assert not hasattr(
        decision,
        "restart_runtime",
    )


# =========================================================
# Test M
# Health State And Policy State Remain Explicit
# =========================================================

def test_health_and_policy_states_remain_explicit():

    watchdog = _create_watchdog(
        [False]
    )

    policy = HealthDegradationPolicy()

    health_state = watchdog.check()

    decision = policy.evaluate(
        health_state,
    )

    assert (
        health_state
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        decision.impact
        == HealthImpact.DEGRADED
    )

    assert (
        decision.runtime_state
        == RuntimeOperationalState.DEGRADED
    )


# =========================================================
# Test N
# Recovery Returns Runtime Policy To Running
# =========================================================

def test_recovery_returns_runtime_policy_to_running():

    watchdog = _create_watchdog(
        [False, True]
    )

    policy = HealthDegradationPolicy()

    degraded_health = watchdog.check()

    degraded_decision = policy.evaluate(
        degraded_health,
    )

    assert (
        degraded_decision.runtime_state
        == RuntimeOperationalState.DEGRADED
    )

    watchdog.clear_transition()

    recovered_health = watchdog.check()

    recovered_decision = policy.evaluate(
        recovered_health,
    )

    assert (
        recovered_decision.runtime_state
        == RuntimeOperationalState.RUNNING
    )

    assert (
        recovered_decision.impact
        == HealthImpact.HEALTHY
    )