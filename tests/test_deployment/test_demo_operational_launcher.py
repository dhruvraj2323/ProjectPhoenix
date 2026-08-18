"""
=================================================
Project Phoenix
Demo Operational Launcher Tests
Post-M63 Operational Bridge
=================================================
"""
from dataclasses import dataclass
from types import SimpleNamespace
import pytest
from deployment.demo_operational_launcher import (
    DemoOperationalLauncher,
)
from deployment.runtime_watchdog import (
    WatchdogHealthState,
)
# =========================================================
# Fake MT5
# =========================================================
@dataclass
class FakeTick:
    bid: float = 100.0
    ask: float = 100.2
@dataclass
class FakeSymbol:
    name: str
@dataclass
class FakeAccount:
    login: int = 123456
    server: str = "Phoenix-Demo"
    trade_mode: int = 0
    balance: float = 10000.0
    equity: float = 10000.0
    margin_free: float = 9000.0
    trade_allowed: bool = True
    trade_expert: bool = True
class FakeMT5:
    ACCOUNT_TRADE_MODE_DEMO = 0
    ACCOUNT_TRADE_MODE_CONTEST = 1
    ACCOUNT_TRADE_MODE_REAL = 2
    def __init__(
        self,
        *,
        demo: bool = True,
        connected: bool = True,
        healthy_symbols=None,
    ):
        self.demo = demo
        self.connected = connected
        self.healthy_symbols = (
            set(
                healthy_symbols
                if healthy_symbols is not None
                else {
                    "EURUSDm",
                    "XAUUSDm",
                    "BTCUSDm",
                }
            )
        )
        self.account = FakeAccount(
            trade_mode=(
                self.ACCOUNT_TRADE_MODE_DEMO
                if demo
                else self.ACCOUNT_TRADE_MODE_REAL
            )
        )
        self.initialize_calls = 0
        self.shutdown_calls = 0
    def initialize(self):
        self.initialize_calls += 1
        return self.connected
    def shutdown(self):
        self.shutdown_calls += 1
    def account_info(self):
        if not self.connected:
            return None
        return self.account
    def symbol_select(
        self,
        symbol,
        selected,
    ):
        return (
            symbol
            in self.healthy_symbols
        )
    def symbol_info(
        self,
        symbol,
    ):
        if (
            symbol
            not in self.healthy_symbols
        ):
            return None
        return FakeSymbol(
            name=symbol
        )
    def symbol_info_tick(
        self,
        symbol,
    ):
        if (
            symbol
            not in self.healthy_symbols
        ):
            return None
        return FakeTick()
    def order_check(self, *args, **kwargs):
        return SimpleNamespace(retcode=0)
    def order_send(self, *args, **kwargs):
        return SimpleNamespace(retcode=10009)
    def positions_get(self):
        return ()
    def orders_get(self):
        return ()
    def history_deals_get(self):
        return ()
# =========================================================
# Fake Runtime
# =========================================================
class FakeProtection:
    def __init__(self):
        self.state = SimpleNamespace(
            value="ACTIVE"
        )
    def can_trade(self):
        return (
            self.state.value
            == "ACTIVE"
        )
    def update(self, health_state):
        if (
            health_state
            == WatchdogHealthState.HEALTHY
        ):
            self.state = SimpleNamespace(
                value="ACTIVE"
            )
        else:
            self.state = SimpleNamespace(
                value="PAUSED"
            )
        return self.state
class FakeRuntime:
    def __init__(
        self,
        interval,
        protection,
    ):
        self.interval = interval
        self.trading_protection = (
            protection
        )
        self.running = False
        self._status = (
            SimpleNamespace(
                operational_state=(
                    SimpleNamespace(
                        value="STOPPED"
                    )
                )
            )
        )
        self.continuous_runner = (
            SimpleNamespace(
                trading_protection=(
                    protection
                ),
                trading_cycle=(
                    SimpleNamespace(
                        connected=True,
                        execution_summary=None,
                        trade_records=[],
                        last_error="",
                    )
                ),
                run_once=lambda: True,
            )
        )
    def start(
        self,
        cycles=1,
    ):
        self.running = True
        self._status = (
            SimpleNamespace(
                operational_state=(
                    SimpleNamespace(
                        value="RUNNING"
                    )
                )
            )
        )
        return True
    def check_watchdog(self):
        return (
            WatchdogHealthState.HEALTHY
        )
    def apply_health_state(
        self,
        health_state,
    ):
        self.trading_protection.update(
            health_state
        )
        return True
    def status_snapshot(self):
        return self._status
    def stop(self):
        self.running = False
# =========================================================
# Helpers
# =========================================================
def _runtime_factory(
    interval,
    protection,
):
    return FakeRuntime(
        interval,
        protection,
    )
def _launcher(
    mt5,
    *,
    validator=None,
):
    return DemoOperationalLauncher(
        observation_days=7,
        ledger_path=(
            "logs/test_demo_launcher.jsonl"
        ),
        mt5_module=mt5,
        runtime_factory=_runtime_factory,
        validator=validator,
    )
# =========================================================
# MT5 / Account Tests
# =========================================================
def test_demo_account_is_accepted():
    launcher = _launcher(
        FakeMT5(
            demo=True
        )
    )
    account = (
        launcher.mt5.account_info()
    )
    assert (
        launcher._is_demo_account(
            account
        )
        is True
    )
def test_real_account_is_rejected():
    launcher = _launcher(
        FakeMT5(
            demo=False
        )
    )
    account = (
        launcher.mt5.account_info()
    )
    assert (
        launcher._is_demo_account(
            account
        )
        is False
    )
def test_missing_account_is_rejected():
    launcher = _launcher(
        FakeMT5(
            connected=False
        )
    )
    assert (
        launcher._is_demo_account(
            None
        )
        is False
    )
def test_account_trade_mode_is_demo():
    launcher = _launcher(
        FakeMT5(
            demo=True
        )
    )
    account = (
        launcher.mt5.account_info()
    )
    assert (
        launcher._account_trade_mode(
            account
        )
        == "DEMO"
    )
def test_account_trade_mode_is_real():
    launcher = _launcher(
        FakeMT5(
            demo=False
        )
    )
    account = (
        launcher.mt5.account_info()
    )
    assert (
        launcher._account_trade_mode(
            account
        )
        == "REAL"
    )
# =========================================================
# Symbol Tests
# =========================================================
def test_configured_symbols_are_unique():
    launcher = _launcher(
        FakeMT5()
    )
    launcher.config.data[
        "market"
    ][
        "symbols"
    ] = [
        "EURUSDm",
        "EURUSDm",
        "XAUUSDm",
    ]
    assert (
        launcher._configured_symbols()
        == [
            "EURUSDm",
            "XAUUSDm",
        ]
    )
def test_healthy_symbols_are_detected():
    launcher = _launcher(
        FakeMT5(
            healthy_symbols={
                "EURUSDm",
                "XAUUSDm",
            }
        )
    )
    symbols = (
        "EURUSDm",
        "XAUUSDm",
    )
    assert (
        launcher._healthy_symbols(
            symbols
        )
        == [
            "EURUSDm",
            "XAUUSDm",
        ]
    )
def test_missing_symbol_is_not_healthy():
    launcher = _launcher(
        FakeMT5(
            healthy_symbols={
                "EURUSDm",
            }
        )
    )
    symbols = (
        "EURUSDm",
        "XAUUSDm",
    )
    assert (
        launcher._healthy_symbols(
            symbols
        )
        == [
            "EURUSDm",
        ]
    )
# =========================================================
# Technical Health Tests
# =========================================================
def test_risk_preflight_passes_for_healthy_account():
    launcher = _launcher(
        FakeMT5()
    )
    launcher.account_info = (
        launcher.mt5.account_info()
    )
    assert (
        launcher._risk_preflight()
        is True
    )
def test_risk_preflight_fails_for_zero_equity():
    launcher = _launcher(
        FakeMT5()
    )
    account = (
        launcher.mt5.account_info()
    )
    account.equity = 0.0
    launcher.account_info = account
    assert (
        launcher._risk_preflight()
        is False
    )
def test_execution_preflight_passes():
    launcher = _launcher(
        FakeMT5()
    )
    launcher.account_info = (
        launcher.mt5.account_info()
    )
    assert (
        launcher._execution_preflight()
        is True
    )
def test_execution_preflight_fails_when_trade_not_allowed():
    launcher = _launcher(
        FakeMT5()
    )
    account = (
        launcher.mt5.account_info()
    )
    account.trade_allowed = False
    launcher.account_info = account
    assert (
        launcher._execution_preflight()
        is False
    )
def test_reconciliation_preflight_passes():
    launcher = _launcher(
        FakeMT5()
    )
    assert (
        launcher._reconciliation_preflight()
        is True
    )
def test_reporting_preflight_passes():
    launcher = _launcher(
        FakeMT5()
    )
    assert (
        launcher._reporting_preflight()
        is True
    )
# =========================================================
# Configuration Safety
# =========================================================
def test_paper_trading_enabled_blocks_configuration():
    launcher = _launcher(
        FakeMT5()
    )
    launcher.config.data[
        "paper_trading"
    ][
        "enabled"
    ] = True
    with pytest.raises(
        RuntimeError,
        match="paper_trading.enabled",
    ):
        launcher._validate_configuration()
def test_paper_trading_disabled_allows_configuration():
    launcher = _launcher(
        FakeMT5()
    )
    launcher.config.data[
        "paper_trading"
    ][
        "enabled"
    ] = False
    launcher._validate_configuration()
def test_empty_symbols_block_configuration():
    launcher = _launcher(
        FakeMT5()
    )
    launcher.config.data[
        "market"
    ][
        "symbols"
    ] = []
    with pytest.raises(
        RuntimeError,
        match="No configured",
    ):
        launcher._validate_configuration()
# =========================================================
# Observation Duration
# =========================================================
@pytest.mark.parametrize(
    "days",
    [
        7,
        8,
        9,
        10,
    ],
)
def test_valid_observation_days(
    days,
):
    launcher = _launcher(
        FakeMT5()
    )
    launcher.observation_days = days
    launcher._validate_observation_days()
@pytest.mark.parametrize(
    "days",
    [
        0,
        1,
        6,
        11,
        30,
    ],
)
def test_invalid_observation_days(
    days,
):
    launcher = _launcher(
        FakeMT5()
    )
    launcher.observation_days = days
    with pytest.raises(
        ValueError
    ):
        launcher._validate_observation_days()
# =========================================================
# Runtime Protection Boundary
# =========================================================
def test_runtime_bootstrap_starts_with_protection_paused():
    launcher = _launcher(
        FakeMT5()
    )
    launcher._bootstrap_runtime()
    assert (
        launcher.protection
        is not None
    )
    assert (
        launcher.protection.can_trade()
        is False
    )
    launcher._safe_shutdown_runtime()
def test_runtime_protection_can_be_activated():
    launcher = _launcher(
        FakeMT5()
    )
    launcher._bootstrap_runtime()
    assert (
        launcher._activate_trading_protection()
        is True
    )
    assert (
        launcher.protection.can_trade()
        is True
    )
    launcher._safe_shutdown_runtime()
# =========================================================
# Bootstrap Safety
# =========================================================
def test_bootstrap_blocks_real_account():
    launcher = _launcher(
        FakeMT5(
            demo=False
        )
    )
    launcher.config.data[
        "paper_trading"
    ][
        "enabled"
    ] = False
    result = (
        launcher.bootstrap()
    )
    assert (
        result.ready
        is False
    )
    assert (
        "REAL or UNKNOWN"
        in result.reason
    )
def test_bootstrap_blocks_missing_mt5():
    launcher = _launcher(
        FakeMT5(
            connected=False
        )
    )
    launcher.config.data[
        "paper_trading"
    ][
        "enabled"
    ] = False
    result = (
        launcher.bootstrap()
    )
    assert (
        result.ready
        is False
    )
def test_bootstrap_blocks_missing_symbol():
    launcher = _launcher(
        FakeMT5(
            healthy_symbols={
                "EURUSDm"
            }
        )
    )
    launcher.config.data[
        "paper_trading"
    ][
        "enabled"
    ] = False
    launcher.config.data[
        "market"
    ][
        "symbols"
    ] = [
        "EURUSDm",
        "XAUUSDm",
    ]
    result = (
        launcher.bootstrap()
    )
    assert (
        result.ready
        is False
    )
# =========================================================
# M63.8 Integration With Healthy Fake Environment
# =========================================================
class AlwaysReadyValidator:
    def validate(
        self,
        snapshot,
    ):
        return SimpleNamespace(
            ready=True,
            blocked=False,
            state=SimpleNamespace(
                value="READY"
            ),
            gates=(),
            reasons=(),
            failed_gates=(),
        )
def test_healthy_bootstrap_reaches_ready():
    launcher = _launcher(
        FakeMT5(),
        validator=(
            AlwaysReadyValidator()
        ),
    )
    launcher.config.data[
        "paper_trading"
    ][
        "enabled"
    ] = False
    launcher.config.data[
        "market"
    ][
        "symbols"
    ] = [
        "EURUSDm",
        "XAUUSDm",
        "BTCUSDm",
    ]
    result = (
        launcher.bootstrap()
    )
    try:
        assert (
            result.ready
            is True
        )
        assert (
            result.configured_symbols
            == (
                "EURUSDm",
                "XAUUSDm",
                "BTCUSDm",
            )
        )
        assert (
            result.healthy_symbols
            == (
                "EURUSDm",
                "XAUUSDm",
                "BTCUSDm",
            )
        )
        assert (
            launcher.protection.can_trade()
            is True
        )
    finally:
        launcher._safe_shutdown_runtime()
# =========================================================
# Real Account Hard Block
# =========================================================
def test_real_account_never_passes_demo_guard():
    launcher = _launcher(
        FakeMT5(
            demo=False
        )
    )
    launcher.account_info = (
        launcher.mt5.account_info()
    )
    assert (
        launcher._is_demo_account(
            launcher.account_info
        )
        is False
    )
    result = (
        launcher._blocked_result(
            reason=(
                "REAL account detected."
            )
        )
    )
    assert (
        result.ready
        is False
    )
# =========================================================
# Runtime State
# =========================================================
def test_runtime_state_is_exposed():
    launcher = _launcher(
        FakeMT5()
    )
    launcher._bootstrap_runtime()
    try:
        state = (
            launcher._runtime_state()
        )
        assert (
            getattr(
                state,
                "value",
                state,
            )
            == "RUNNING"
        )
    finally:
        launcher._safe_shutdown_runtime()
