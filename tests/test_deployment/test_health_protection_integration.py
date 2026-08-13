"""
=================================================
Project Phoenix
Health Protection Integration Tests
M61.8.6 - End-to-End Health Protection Validation
=================================================
"""

from unittest.mock import MagicMock

from deployment.continuous_runner import (
    ContinuousRunner,
)

from deployment.runtime_manager import (
    RuntimeManager,
)

from deployment.runtime_watchdog import (
    RuntimeWatchdog,
    WatchdogHealthState,
)

from deployment.trading_protection import (
    TradingProtection,
    TradingProtectionState,
)


# =========================================================
# Test A
# Healthy → Trading Allowed
# =========================================================

def test_health_protection_healthy_allows_trading():

    health_monitor = MagicMock()

    health_monitor.is_healthy.return_value = True

    watchdog = RuntimeWatchdog(
        health_monitor=health_monitor,
    )

    protection = TradingProtection()

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=protection,
    )

    health_state = manager.health_state()

    assert (
        health_state
        == WatchdogHealthState.HEALTHY
    )

    assert (
        manager.trading_protection_state()
        == TradingProtectionState.ACTIVE
    )

    assert (
        manager.can_trade()
        is True
    )


# =========================================================
# Test B
# Unhealthy → Trading Paused
# =========================================================

def test_health_protection_unhealthy_pauses_trading():

    health_monitor = MagicMock()

    health_monitor.is_healthy.return_value = False

    watchdog = RuntimeWatchdog(
        health_monitor=health_monitor,
    )

    protection = TradingProtection()

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=protection,
    )

    health_state = manager.health_state()

    assert (
        health_state
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        manager.trading_protection_state()
        == TradingProtectionState.PAUSED
    )

    assert (
        manager.can_trade()
        is False
    )


# =========================================================
# Test C
# Paused Protection Blocks TradingCycle
# =========================================================

def test_health_protection_paused_blocks_trading_cycle():

    protection = TradingProtection()

    protection.update(
        WatchdogHealthState.UNHEALTHY,
    )

    runner = ContinuousRunner(
        interval=0,
        trading_protection=protection,
    )

    runner.trading_cycle = MagicMock()

    runner.trading_cycle.execute.return_value = True

    result = runner.run_once()

    assert result is True

    assert (
        protection.state
        == TradingProtectionState.PAUSED
    )

    assert (
        protection.can_trade()
        is False
    )

    runner.trading_cycle.execute.assert_not_called()


# =========================================================
# Test D
# Health Recovery → Trading Resumes
# =========================================================

def test_health_protection_recovery_resumes_trading():

    health_monitor = MagicMock()

    health_monitor.is_healthy.side_effect = [
        False,
        True,
    ]

    watchdog = RuntimeWatchdog(
        health_monitor=health_monitor,
    )

    protection = TradingProtection()

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=protection,
    )

    # --------------------------------------------------
    # First health check
    # --------------------------------------------------

    first_state = (
        manager.health_state()
    )

    assert (
        first_state
        == WatchdogHealthState.UNHEALTHY
    )

    assert (
        manager.can_trade()
        is False
    )

    # --------------------------------------------------
    # Recovery health check
    # --------------------------------------------------

    second_state = (
        manager.health_state()
    )

    assert (
        second_state
        == WatchdogHealthState.HEALTHY
    )

    assert (
        manager.can_trade()
        is True
    )

    assert (
        manager.trading_protection_state()
        == TradingProtectionState.ACTIVE
    )


# =========================================================
# Test E
# Full End-to-End Pause → Recovery → Trading
# =========================================================

def test_health_protection_full_end_to_end_cycle():

    health_monitor = MagicMock()

    health_monitor.is_healthy.side_effect = [
        True,
        False,
        True,
    ]

    watchdog = RuntimeWatchdog(
        health_monitor=health_monitor,
    )

    protection = TradingProtection()

    manager = RuntimeManager(
        runtime=MagicMock(),
        watchdog=watchdog,
        trading_protection=protection,
    )

    runner = ContinuousRunner(
        interval=0,
        trading_protection=protection,
    )

    runner.trading_cycle = MagicMock()

    runner.trading_cycle.execute.return_value = True

    # --------------------------------------------------
    # Step 1
    # Healthy
    # --------------------------------------------------

    manager.health_state()

    assert (
        manager.can_trade()
        is True
    )

    result = runner.run_once()

    assert result is True

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )

    # --------------------------------------------------
    # Step 2
    # Health becomes unhealthy
    # --------------------------------------------------

    manager.health_state()

    assert (
        manager.can_trade()
        is False
    )

    result = runner.run_once()

    assert result is True

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )

    # --------------------------------------------------
    # Step 3
    # Health recovers
    # --------------------------------------------------

    manager.health_state()

    assert (
        manager.can_trade()
        is True
    )

    result = runner.run_once()

    assert result is True

    assert (
        runner.trading_cycle.execute.call_count
        == 2
    )