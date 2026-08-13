"""
=================================================
Project Phoenix
Runtime Manager Tests
M61.8.4 - Trading Protection Integration
=================================================
"""

from unittest.mock import MagicMock

from deployment.runtime_manager import (
    RuntimeManager,
)

from deployment.runtime_watchdog import (
    HealthTransition,
    WatchdogHealthState,
)

from deployment.trading_protection import (
    ProtectionTransition,
    TradingProtectionState,
)


# =========================================================
# Test A
# Runtime Manager Start
# =========================================================

def test_runtime_manager_start():

    runtime = MagicMock()

    runtime.start.return_value = True
    runtime.running = False

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is True

    runtime.start.assert_called_once_with(
        cycles=1,
    )

    assert manager.running is False


# =========================================================
# Test B
# Readiness Failure
# =========================================================

def test_runtime_manager_start_blocked():

    runtime = MagicMock()

    runtime.start.return_value = False
    runtime.running = False

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is False

    assert manager.running is False


# =========================================================
# Test C
# Runtime Running State
# =========================================================

def test_runtime_manager_running_state():

    runtime = MagicMock()

    runtime.start.return_value = True
    runtime.running = True

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.start(
        cycles=1,
    )

    assert result is True

    assert manager.running is True

    assert manager.status() is True


# =========================================================
# Test D
# Stop
# =========================================================

def test_runtime_manager_stop():

    runtime = MagicMock()

    runtime.running = True

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.stop()

    assert result is True

    runtime.stop.assert_called_once()

    assert manager.running is True


# =========================================================
# Test E
# Restart
# =========================================================

def test_runtime_manager_restart():

    runtime = MagicMock()

    runtime.start.return_value = True
    runtime.running = False

    manager = RuntimeManager(
        runtime=runtime,
    )

    result = manager.restart(
        cycles=1,
    )

    assert result is True

    runtime.stop.assert_called_once()

    runtime.start.assert_called_once_with(
        cycles=1,
    )


# =========================================================
# Test F
# Healthy Health State → Active Trading
# =========================================================

def test_runtime_manager_health_active():

    watchdog = MagicMock()

    watchdog.check.return_value = (
        WatchdogHealthState.HEALTHY
    )

    protection = MagicMock()

    protection.state = (
        TradingProtectionState.ACTIVE
    )

    protection.can_trade.return_value = True
    protection.is_paused.return_value = False

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=protection,
    )

    result = manager.health_state()

    assert (
        result
        == WatchdogHealthState.HEALTHY
    )

    watchdog.check.assert_called_once()

    protection.update.assert_called_once_with(
        WatchdogHealthState.HEALTHY,
    )

    assert (
        manager.trading_protection_state()
        == TradingProtectionState.ACTIVE
    )

    assert (
        manager.can_trade()
        is True
    )

    assert (
        manager.trading_paused()
        is False
    )


# =========================================================
# Test G
# Unhealthy Health → Paused Trading
# =========================================================

def test_runtime_manager_health_pauses_trading():

    watchdog = MagicMock()

    watchdog.check.return_value = (
        WatchdogHealthState.UNHEALTHY
    )

    protection = MagicMock()

    protection.state = (
        TradingProtectionState.PAUSED
    )

    protection.can_trade.return_value = False
    protection.is_paused.return_value = True

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=protection,
    )

    result = manager.health_state()

    assert (
        result
        == WatchdogHealthState.UNHEALTHY
    )

    protection.update.assert_called_once_with(
        WatchdogHealthState.UNHEALTHY,
    )

    assert (
        manager.trading_protection_state()
        == TradingProtectionState.PAUSED
    )

    assert (
        manager.can_trade()
        is False
    )

    assert (
        manager.trading_paused()
        is True
    )


# =========================================================
# Test H
# Health Transition
# =========================================================

def test_runtime_manager_health_transition():

    watchdog = MagicMock()

    transition = HealthTransition(
        previous_state=(
            WatchdogHealthState.HEALTHY
        ),
        current_state=(
            WatchdogHealthState.UNHEALTHY
        ),
    )

    watchdog.last_transition = transition

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=MagicMock(),
    )

    assert (
        manager.health_transition()
        == transition
    )


# =========================================================
# Test I
# Health Transition Detection
# =========================================================

def test_runtime_manager_health_transition_detected():

    watchdog = MagicMock()

    watchdog.has_transitioned.return_value = True

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=MagicMock(),
    )

    assert (
        manager.health_transition_detected()
        is True
    )

    watchdog.has_transitioned.assert_called_once()


# =========================================================
# Test J
# Health Recovery
# =========================================================

def test_runtime_manager_health_recovered():

    watchdog = MagicMock()

    watchdog.has_recovered.return_value = True

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=MagicMock(),
    )

    assert (
        manager.health_recovered()
        is True
    )

    watchdog.has_recovered.assert_called_once()


# =========================================================
# Test K
# Clear Health Transition
# =========================================================

def test_runtime_manager_clear_health_transition():

    watchdog = MagicMock()

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=MagicMock(),
    )

    manager.clear_health_transition()

    watchdog.clear_transition.assert_called_once()


# =========================================================
# Test L
# Trading Protection Transition
# =========================================================

def test_runtime_manager_trading_protection_transition():

    protection = MagicMock()

    transition = ProtectionTransition(
        previous_state=(
            TradingProtectionState.ACTIVE
        ),
        current_state=(
            TradingProtectionState.PAUSED
        ),
    )

    protection.last_transition = transition

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=MagicMock(),
        trading_protection=protection,
    )

    assert (
        manager.trading_protection_transition()
        == transition
    )


# =========================================================
# Test M
# Clear Trading Protection Transition
# =========================================================

def test_runtime_manager_clear_trading_protection_transition():

    protection = MagicMock()

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=MagicMock(),
        trading_protection=protection,
    )

    manager.clear_trading_protection_transition()

    protection.clear_transition.assert_called_once()


# =========================================================
# Test N
# Unhealthy Does Not Stop Runtime
# =========================================================

def test_runtime_manager_unhealthy_does_not_stop_runtime():

    runtime = MagicMock()

    runtime.running = True

    watchdog = MagicMock()

    watchdog.check.return_value = (
        WatchdogHealthState.UNHEALTHY
    )

    protection = MagicMock()

    protection.state = (
        TradingProtectionState.PAUSED
    )

    protection.can_trade.return_value = False
    protection.is_paused.return_value = True

    manager = RuntimeManager(
        runtime=runtime,
        watchdog=watchdog,
        trading_protection=protection,
    )

    result = manager.health_state()

    assert (
        result
        == WatchdogHealthState.UNHEALTHY
    )

    assert manager.status() is True

    assert (
        manager.can_trade()
        is False
    )

    runtime.stop.assert_not_called()