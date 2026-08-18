"""
=================================================
Project Phoenix
Demo Operational Launcher
Post-M63 Operational Bridge
=================================================
Purpose
-------
Safely connect the frozen M63.8 validation boundary
to the frozen M63.9 controlled DEMO operation.
Safety principles
-----------------
1. MT5 must be connected.
2. Account information must be available.
3. Account must explicitly be DEMO.
4. Real/unknown accounts are always blocked.
5. Configured symbols must exist and have healthy ticks.
6. Paper-trading mode must be disabled.
7. Runtime starts with TradingProtection PAUSED.
8. The first runtime cycle is therefore protected.
9. TradingProtection becomes ACTIVE only after the
   protected runtime bootstrap is healthy.
10. M63.8 must return READY.
11. M63.9 remains the authoritative observation controller.
12. Existing ContinuousRunner remains unchanged.
13. Account DEMO status is rechecked before every
    observation cycle.
14. A real-account detection immediately blocks operation.
15. No strategy, risk, execution, or reporting logic
    is reimplemented here.
This module does NOT:
- implement strategy
- calculate signals
- submit MT5 orders directly
- modify positions
- modify risk decisions
- replace ContinuousRunner
- replace M63.8
- replace M63.9
- automatically modify strategy parameters
"""
from __future__ import annotations
import argparse
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
import MetaTrader5 as mt5
from deployment.controlled_demo_operation import (
    ControlledDemoOperation,
)
from deployment.runtime import (
    Runtime,
)
from deployment.runtime_config import (
    RuntimeConfig,
)
from deployment.trading_protection import (
    TradingProtection,
)
from deployment.runtime_watchdog import (
    WatchdogHealthState,
)
from live_execution.demo_go_live_validation import (
    DemoGoLiveValidationSnapshot,
    DemoGoLiveValidationResult,
    DemoGoLiveValidator,
)
from reporting.report_generator import (
    ReportGenerator,
)
# =========================================================
# Configuration
# =========================================================
DEFAULT_OBSERVATION_DAYS = 7
DEFAULT_LEDGER_PATH = (
    Path("logs")
    / "demo_observation"
    / "m63_9_observation.jsonl"
)
# =========================================================
# Launch Result
# =========================================================
@dataclass(frozen=True)
class DemoOperationalLaunchResult:
    """
    Immutable result of the launcher bootstrap.
    """
    ready: bool
    validation_result: (
        DemoGoLiveValidationResult | None
    )
    configured_symbols: tuple[str, ...]
    healthy_symbols: tuple[str, ...]
    account_login: int | None
    account_server: str
    account_trade_mode: str
    reason: str = ""
# =========================================================
# Continuous Runner Adapter
# =========================================================
class DemoOperationRunnerAdapter:
    """
    Adapts the existing Runtime/ContinuousRunner structure
    to the M63.9 ControlledDemoOperation contract.
    M63.9 expects:
        - run_once()
        - trading_protection
        - trading_cycle
        - runtime
    The existing ContinuousRunner already provides the
    first three, while Runtime provides the authoritative
    runtime state.
    """
    def __init__(
        self,
        runtime: Runtime,
    ) -> None:
        self.runtime = runtime
        self.runner = (
            runtime.continuous_runner
        )
        self.trading_protection = (
            self.runner.trading_protection
        )
        self.trading_cycle = (
            self.runner.trading_cycle
        )
    def run_once(
        self,
    ) -> bool:
        """
        Execute exactly one existing Phoenix cycle.
        No new trading logic is introduced here.
        """
        return bool(
            self.runner.run_once()
        )
# =========================================================
# Demo Operational Launcher
# =========================================================
class DemoOperationalLauncher:
    """
    Operational bridge between M63.8 and M63.9.
    The launcher is intentionally fail-closed.
    """
    def __init__(
        self,
        *,
        observation_days: int = (
            DEFAULT_OBSERVATION_DAYS
        ),
        ledger_path: str | Path = (
            DEFAULT_LEDGER_PATH
        ),
        mt5_module: Any = mt5,
        runtime_factory: Callable[
            [int, TradingProtection],
            Runtime,
        ] | None = None,
        validator: (
            DemoGoLiveValidator | None
        ) = None,
    ) -> None:
        self.observation_days = (
            observation_days
        )
        self.ledger_path = Path(
            ledger_path
        )
        self.mt5 = mt5_module
        self.validator = (
            validator
            if validator is not None
            else DemoGoLiveValidator()
        )
        self.config = RuntimeConfig()
        self.runtime: Runtime | None = None
        self.operation: (
            ControlledDemoOperation | None
        ) = None
        self.adapter: (
            DemoOperationRunnerAdapter | None
        ) = None
        self.protection: (
            TradingProtection | None
        ) = None
        self.account_info: Any = None
        self.runtime_factory = (
            runtime_factory
            if runtime_factory is not None
            else self._default_runtime_factory
        )
    # =====================================================
    # Public Bootstrap
    # =====================================================
    def bootstrap(
        self,
    ) -> DemoOperationalLaunchResult:
        """
        Perform the complete M63.8 technical bootstrap.
        No DEMO trading cycle is permitted until the
        returned validation result is READY.
        """
        print()
        print("=" * 70)
        print(
            "PROJECT PHOENIX - DEMO OPERATIONAL LAUNCHER"
        )
        print("=" * 70)
        # -------------------------------------------------
        # 1. Observation Duration
        # -------------------------------------------------
        self._validate_observation_days()
        # -------------------------------------------------
        # 2. Configuration Safety
        # -------------------------------------------------
        self._validate_configuration()
        # -------------------------------------------------
        # 3. MT5 Connection
        # -------------------------------------------------
        connected = (
            self._connect_mt5()
        )
        if not connected:
            return self._blocked_result(
                reason=(
                    "MT5 initialization failed."
                )
            )
        # -------------------------------------------------
        # 4. Account
        # -------------------------------------------------
        account = (
            self._read_account()
        )
        if account is None:
            return self._blocked_result(
                reason=(
                    "MT5 account information is unavailable."
                )
            )
        # -------------------------------------------------
        # 5. HARD DEMO ACCOUNT GUARD
        # -------------------------------------------------
        if not self._is_demo_account(
            account
        ):
            return self._blocked_result(
                reason=(
                    "REAL or UNKNOWN MT5 account detected. "
                    "DEMO operation is BLOCKED."
                )
            )
        # -------------------------------------------------
        # 6. Symbols
        # -------------------------------------------------
        configured_symbols = tuple(
            self._configured_symbols()
        )
        healthy_symbols = tuple(
            self._healthy_symbols(
                configured_symbols
            )
        )
        # -------------------------------------------------
        # 7. Runtime
        #
        # Runtime starts with TradingProtection PAUSED.
        # Its first cycle therefore cannot trade.
        # -------------------------------------------------
        try:
            self._bootstrap_runtime()
        except Exception as exc:
            return self._blocked_result(
                reason=(
                    "Runtime bootstrap failed: "
                    f"{exc}"
                ),
                configured_symbols=(
                    configured_symbols
                ),
                healthy_symbols=(
                    healthy_symbols
                ),
            )
        # -------------------------------------------------
        # 8. Runtime Watchdog
        # -------------------------------------------------
        watchdog_health = (
            self.runtime.check_watchdog()
            if self.runtime is not None
            else WatchdogHealthState.UNHEALTHY
        )
        if (
            watchdog_health
            != WatchdogHealthState.HEALTHY
        ):
            self._safe_shutdown_runtime()
            return self._blocked_result(
                reason=(
                    "Runtime watchdog is not HEALTHY."
                ),
                configured_symbols=(
                    configured_symbols
                ),
                healthy_symbols=(
                    healthy_symbols
                ),
            )
        # -------------------------------------------------
        # 9. Activate TradingProtection
        #
        # This is deliberately AFTER the protected
        # bootstrap cycle and watchdog check.
        # -------------------------------------------------
        if not self._activate_trading_protection():
            self._safe_shutdown_runtime()
            return self._blocked_result(
                reason=(
                    "TradingProtection could not "
                    "be activated safely."
                ),
                configured_symbols=(
                    configured_symbols
                ),
                healthy_symbols=(
                    healthy_symbols
                ),
            )
        # -------------------------------------------------
        # 10. Runtime State
        # -------------------------------------------------
        runtime_state = (
            self._runtime_state()
        )
        # -------------------------------------------------
        # 11. Health Gates
        # -------------------------------------------------
        risk_approved = (
            self._risk_preflight()
        )
        execution_healthy = (
            self._execution_preflight()
        )
        reconciliation_healthy = (
            self._reconciliation_preflight()
        )
        reporting_healthy = (
            self._reporting_preflight()
        )
        # -------------------------------------------------
        # 12. M63.8 Snapshot
        # -------------------------------------------------
        snapshot = (
            DemoGoLiveValidationSnapshot(
                mt5_connected=(
                    connected
                ),
                account_available=(
                    account is not None
                ),
                demo_account_confirmed=(
                    self._is_demo_account(
                        account
                    )
                ),
                configured_symbols=(
                    configured_symbols
                ),
                healthy_symbols=(
                    healthy_symbols
                ),
                market_data_healthy=(
                    set(
                        healthy_symbols
                    )
                    == set(
                        configured_symbols
                    )
                    and bool(
                        configured_symbols
                    )
                ),
                runtime_state=(
                    runtime_state
                ),
                trading_protection_state=(
                    self.protection.state
                    if self.protection is not None
                    else "UNKNOWN"
                ),
                risk_approved=(
                    risk_approved
                ),
                execution_healthy=(
                    execution_healthy
                ),
                reconciliation_healthy=(
                    reconciliation_healthy
                ),
                reporting_healthy=(
                    reporting_healthy
                ),
            )
        )
        validation_result = (
            self.validator.validate(
                snapshot
            )
        )
        self._print_validation_result(
            validation_result
        )
        # -------------------------------------------------
        # 13. Final Decision
        # -------------------------------------------------
        if not validation_result.ready:
            self._safe_shutdown_runtime()
            return DemoOperationalLaunchResult(
                ready=False,
                validation_result=(
                    validation_result
                ),
                configured_symbols=(
                    configured_symbols
                ),
                healthy_symbols=(
                    healthy_symbols
                ),
                account_login=(
                    self._account_login(
                        account
                    )
                ),
                account_server=(
                    self._account_server(
                        account
                    )
                ),
                account_trade_mode=(
                    self._account_trade_mode(
                        account
                    )
                ),
                reason=(
                    "M63.8 validation BLOCKED."
                ),
            )
        print()
        print(
            "M63.8 RESULT : READY"
        )
        print(
            "DEMO trading boundary passed."
        )
        return DemoOperationalLaunchResult(
            ready=True,
            validation_result=(
                validation_result
            ),
            configured_symbols=(
                configured_symbols
            ),
            healthy_symbols=(
                healthy_symbols
            ),
            account_login=(
                self._account_login(
                    account
                )
            ),
            account_server=(
                self._account_server(
                    account
                )
            ),
            account_trade_mode=(
                self._account_trade_mode(
                    account
                )
            ),
            reason=(
                "M63.8 validation READY."
            ),
        )
    # =====================================================
    # Start M63.9
    # =====================================================
    def start_observation(
        self,
        *,
        once: bool = False,
    ) -> None:
        """
        Start M63.9 after M63.8 READY.
        once=True:
            Execute exactly one controlled DEMO cycle.
        once=False:
            Continue until the M63.9 observation window
            expires or the launcher is stopped.
        """
        result = (
            self.bootstrap()
        )
        if not result.ready:
            raise RuntimeError(
                "DEMO operational launch blocked: "
                + result.reason
            )
        if (
            self.runtime is None
            or self.protection is None
        ):
            raise RuntimeError(
                "Runtime/protection bootstrap "
                "is incomplete."
            )
        self.adapter = (
            DemoOperationRunnerAdapter(
                self.runtime
            )
        )
        self.operation = (
            ControlledDemoOperation(
                runner=self.adapter,
                go_live_result=(
                    result.validation_result
                ),
                observation_days=(
                    self.observation_days
                ),
                ledger_path=(
                    self.ledger_path
                ),
            )
        )
        self.operation.start()
        print()
        print("=" * 70)
        print(
            "M63.9 CONTROLLED DEMO OPERATION STARTED"
        )
        print(
            f"Observation Days : "
            f"{self.observation_days}"
        )
        print(
            f"Cycle Interval   : "
            f"{self.config.interval} seconds"
        )
        print(
            f"Symbols          : "
            f"{', '.join(result.configured_symbols)}"
        )
        print(
            "Trading Mode     : DEMO"
        )
        print("=" * 70)
        try:
            if once:
                self._run_one_controlled_cycle()
                return
            self._run_continuously()
        except KeyboardInterrupt:
            print()
            print(
                "Keyboard interrupt received."
            )
        finally:
            self._shutdown_operation()
    # =====================================================
    # One Controlled Cycle
    # =====================================================
    def _run_one_controlled_cycle(
        self,
    ) -> None:
        self._revalidate_demo_account()
        self._refresh_runtime_health()
        if self.operation is None:
            raise RuntimeError(
                "M63.9 operation is not initialized."
            )
        print()
        print(
            "Running one controlled DEMO cycle..."
        )
        event = (
            self.operation.run_cycle()
        )
        print()
        print(
            "===== DEMO CYCLE RESULT ====="
        )
        print(
            f"Cycle       : "
            f"{event.cycle_number}"
        )
        print(
            f"Status      : "
            f"{event.cycle_status}"
        )
        print(
            f"Success     : "
            f"{event.success}"
        )
        print(
            f"Executed    : "
            f"{event.executed_symbols}"
        )
        print(
            f"No Trade    : "
            f"{event.no_trade_symbols}"
        )
        print(
            f"Failed      : "
            f"{event.failed_symbols}"
        )
        print(
            f"Trade IDs   : "
            f"{event.trade_ids}"
        )
        print(
            "=============================="
        )
    # =====================================================
    # Continuous Observation
    # =====================================================
    def _run_continuously(
        self,
    ) -> None:
        if self.operation is None:
            raise RuntimeError(
                "M63.9 operation is not initialized."
            )
        while True:
            status = (
                self.operation.status()
            )
            if not status.active:
                print()
                print(
                    "M63.9 observation operation "
                    "is no longer active."
                )
                break
            # ---------------------------------------------
            # Re-check DEMO account before EVERY cycle.
            # ---------------------------------------------
            try:
                self._revalidate_demo_account()
            except Exception as exc:
                print()
                print(
                    "DEMO account revalidation FAILED."
                )
                print(exc)
                self._pause_trading()
                break
            # ---------------------------------------------
            # Refresh watchdog/protection state.
            # ---------------------------------------------
            self._refresh_runtime_health()
            # ---------------------------------------------
            # Execute one controlled observation cycle.
            #
            # If protection is PAUSED, ContinuousRunner
            # will not call TradingCycle.execute().
            # ---------------------------------------------
            event = (
                self.operation.run_cycle()
            )
            print()
            print(
                "===== M63.9 OBSERVATION EVENT ====="
            )
            print(
                f"Cycle       : "
                f"{event.cycle_number}"
            )
            print(
                f"Status      : "
                f"{event.cycle_status}"
            )
            print(
                f"Success     : "
                f"{event.success}"
            )
            print(
                f"Executed    : "
                f"{event.executed_symbols}"
            )
            print(
                f"No Trade    : "
                f"{event.no_trade_symbols}"
            )
            print(
                f"Failed      : "
                f"{event.failed_symbols}"
            )
            print(
                f"Trade IDs   : "
                f"{event.trade_ids}"
            )
            print(
                f"Protection  : "
                f"{event.trading_protection_state}"
            )
            print(
                "==================================="
            )
            if (
                not event.success
                and event.errors
            ):
                print()
                print(
                    "Cycle errors:"
                )
                for error in event.errors:
                    print(
                        f" - {error}"
                    )
            # ---------------------------------------------
            # M63.9 uses the existing 300-second runner
            # interval. Do not create another scheduler.
            # ---------------------------------------------
            status = (
                self.operation.status()
            )
            if not status.active:
                break
            print()
            print(
                f"Waiting "
                f"{self.config.interval} seconds "
                "for next DEMO cycle..."
            )
            time.sleep(
                self.config.interval
            )
    # =====================================================
    # MT5
    # =====================================================
    def _connect_mt5(
        self,
    ) -> bool:
        try:
            initialized = bool(
                self.mt5.initialize()
            )
        except Exception as exc:
            print()
            print(
                "MT5 initialization exception:"
            )
            print(exc)
            return False
        if not initialized:
            print()
            print(
                "MT5 initialization failed."
            )
            return False
        print()
        print(
            "MT5 Connected."
        )
        return True
    def _read_account(
        self,
    ):
        try:
            account = (
                self.mt5.account_info()
            )
        except Exception as exc:
            print()
            print(
                "MT5 account_info() failed:"
            )
            print(exc)
            return None
        self.account_info = (
            account
        )
        return account
    # =====================================================
    # DEMO Account Guard
    # =====================================================
    def _is_demo_account(
        self,
        account,
    ) -> bool:
        if account is None:
            return False
        trade_mode = getattr(
            account,
            "trade_mode",
            None,
        )
        demo_constant = getattr(
            self.mt5,
            "ACCOUNT_TRADE_MODE_DEMO",
            0,
        )
        # -------------------------------------------------
        # Explicit DEMO constant comparison.
        # -------------------------------------------------
        if (
            trade_mode
            == demo_constant
        ):
            return True
        # -------------------------------------------------
        # Defensive fallback.
        #
        # Never treat REAL as DEMO.
        # Unknown values remain blocked.
        # -------------------------------------------------
        return False
    # =====================================================
    # Symbol Health
    # =====================================================
    def _configured_symbols(
        self,
    ) -> list[str]:
        symbols = [
            str(symbol).strip()
            for symbol in self.config.symbols
            if str(symbol).strip()
        ]
        return list(
            dict.fromkeys(
                symbols
            )
        )
    def _healthy_symbols(
        self,
        symbols: tuple[str, ...],
    ) -> list[str]:
        healthy: list[str] = []
        for symbol in symbols:
            try:
                selected = (
                    self.mt5.symbol_select(
                        symbol,
                        True,
                    )
                )
                if not selected:
                    continue
                info = (
                    self.mt5.symbol_info(
                        symbol
                    )
                )
                tick = (
                    self.mt5.symbol_info_tick(
                        symbol
                    )
                )
                if info is None:
                    continue
                if tick is None:
                    continue
                bid = float(
                    getattr(
                        tick,
                        "bid",
                        0.0,
                    )
                    or 0.0
                )
                ask = float(
                    getattr(
                        tick,
                        "ask",
                        0.0,
                    )
                    or 0.0
                )
                if bid <= 0.0:
                    continue
                if ask <= 0.0:
                    continue
                healthy.append(
                    symbol
                )
            except Exception:
                continue
        return healthy
    # =====================================================
    # Runtime
    # =====================================================
    def _default_runtime_factory(
        self,
        interval: int,
        protection: TradingProtection,
    ) -> Runtime:
        return Runtime(
            interval=interval,
            trading_protection=protection,
        )
    def _bootstrap_runtime(
        self,
    ) -> None:
        print()
        print(
            "Bootstrapping Runtime with "
            "TradingProtection PAUSED..."
        )
        self.protection = (
            TradingProtection()
        )
        # -------------------------------------------------
        # CRITICAL:
        #
        # TradingProtection starts ACTIVE by design.
        # Convert it to PAUSED before Runtime startup.
        # -------------------------------------------------
        self.protection.update(
            WatchdogHealthState.UNHEALTHY
        )
        if self.protection.can_trade():
            raise RuntimeError(
                "TradingProtection failed to enter "
                "PAUSED state."
            )
        self.runtime = (
            self.runtime_factory(
                self.config.interval,
                self.protection,
            )
        )
        started = (
            self.runtime.start(
                cycles=1,
            )
        )
        if not started:
            raise RuntimeError(
                "Runtime protected bootstrap failed."
            )
        if not self.runtime.running:
            raise RuntimeError(
                "Runtime is not running after "
                "protected bootstrap."
            )
        print(
            "Protected Runtime bootstrap completed."
        )
    def _activate_trading_protection(
        self,
    ) -> bool:
        if (
            self.runtime is None
            or self.protection is None
        ):
            return False
        try:
            applied = (
                self.runtime.apply_health_state(
                    WatchdogHealthState.HEALTHY
                )
            )
        except Exception:
            return False
        if not applied:
            return False
        return (
            self.protection.can_trade()
        )
    def _runtime_state(
        self,
    ) -> Any:
        if self.runtime is None:
            return "UNKNOWN"
        try:
            return (
                self.runtime
                .status_snapshot()
                .operational_state
            )
        except Exception:
            return "UNKNOWN"
    def _refresh_runtime_health(
        self,
    ) -> WatchdogHealthState:
        if self.runtime is None:
            return (
                WatchdogHealthState.UNHEALTHY
            )
        try:
            health = (
                self.runtime.check_watchdog()
            )
        except Exception:
            self._pause_trading()
            return (
                WatchdogHealthState.UNHEALTHY
            )
        if (
            health
            == WatchdogHealthState.HEALTHY
        ):
            try:
                self.runtime.apply_health_state(
                    WatchdogHealthState.HEALTHY
                )
            except Exception:
                self._pause_trading()
        else:
            self._pause_trading()
        return health
    def _pause_trading(
        self,
    ) -> None:
        if self.protection is None:
            return
        try:
            self.protection.update(
                WatchdogHealthState.UNHEALTHY
            )
        except Exception:
            pass
    # =====================================================
    # Technical Health Gates
    # =====================================================
    def _risk_preflight(
        self,
    ) -> bool:
        account = (
            self.account_info
        )
        if account is None:
            return False
        try:
            balance = float(
                getattr(
                    account,
                    "balance",
                    0.0,
                )
            )
            equity = float(
                getattr(
                    account,
                    "equity",
                    0.0,
                )
            )
            free_margin = float(
                getattr(
                    account,
                    "margin_free",
                    0.0,
                )
            )
        except (
            TypeError,
            ValueError,
        ):
            return False
        return (
            balance > 0.0
            and equity > 0.0
            and free_margin > 0.0
        )
    def _execution_preflight(
        self,
    ) -> bool:
        account = (
            self.account_info
        )
        if account is None:
            return False
        trade_allowed = getattr(
            account,
            "trade_allowed",
            None,
        )
        trade_expert = getattr(
            account,
            "trade_expert",
            None,
        )
        # -------------------------------------------------
        # If MT5 exposes the flags, they must be true.
        # -------------------------------------------------
        if (
            trade_allowed is False
        ):
            return False
        if (
            trade_expert is False
        ):
            return False
        required_api = (
            "order_check",
            "order_send",
            "positions_get",
        )
        return all(
            callable(
                getattr(
                    self.mt5,
                    name,
                    None,
                )
            )
            for name in required_api
        )
    def _reconciliation_preflight(
        self,
    ) -> bool:
        try:
            positions = (
                self.mt5.positions_get()
            )
            orders = (
                self.mt5.orders_get()
            )
            history = (
                self.mt5.history_deals_get()
            )
        except Exception:
            return False
        # -------------------------------------------------
        # MT5 returns None on API failure.
        # Empty tuple/list is a healthy "no state"
        # condition.
        # -------------------------------------------------
        return (
            positions is not None
            and orders is not None
            and history is not None
        )
    def _reporting_preflight(
        self,
    ) -> bool:
        try:
            directory = (
                ReportGenerator.REPORT_DIRECTORY
            )
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )
            probe = (
                directory
                / ".phoenix_reporting_probe"
            )
            probe.write_text(
                "OK",
                encoding="utf-8",
            )
            probe.unlink(
                missing_ok=True,
            )
            return True
        except Exception:
            return False
    # =====================================================
    # Configuration Safety
    # =====================================================
    def _validate_configuration(
        self,
    ) -> None:
        symbols = (
            self._configured_symbols()
        )
        if not symbols:
            raise RuntimeError(
                "No configured DEMO trading symbols."
            )
        # -------------------------------------------------
        # CRITICAL LIVE/DEMO SAFETY
        #
        # Paper mode must be disabled before the
        # operational launcher can permit DEMO orders.
        # -------------------------------------------------
        if (
            self.config.paper_trading_enabled
        ):
            raise RuntimeError(
                "paper_trading.enabled is TRUE. "
                "DEMO operational launch is blocked. "
                "Disable paper trading before running "
                "the DEMO launcher."
            )
    def _validate_observation_days(
        self,
    ) -> None:
        if not (
            ControlledDemoOperation.MIN_OBSERVATION_DAYS
            <= self.observation_days
            <= ControlledDemoOperation.MAX_OBSERVATION_DAYS
        ):
            raise ValueError(
                "Observation duration must be "
                "between 7 and 10 days."
            )
    # =====================================================
    # Validation Output
    # =====================================================
    def _print_validation_result(
        self,
        result: DemoGoLiveValidationResult,
    ) -> None:
        print()
        print("=" * 70)
        print(
            "M63.8 DEMO GO-LIVE VALIDATION"
        )
        print("=" * 70)
        for gate in result.gates:
            state = (
                getattr(
                    gate.state,
                    "value",
                    gate.state,
                )
            )
            marker = (
                "PASS"
                if gate.passed
                else "FAIL"
            )
            print(
                f"{marker:<5} "
                f"{gate.name:<22} "
                f"{state:<5} "
                f"{gate.reason}"
            )
        print("-" * 70)
        print(
            "FINAL STATE : "
            f"{result.state.value}"
        )
        print("=" * 70)
    # =====================================================
    # Result Helpers
    # =====================================================
    def _blocked_result(
        self,
        *,
        reason: str,
        configured_symbols: tuple[str, ...] = (),
        healthy_symbols: tuple[str, ...] = (),
    ) -> DemoOperationalLaunchResult:
        print()
        print(
            "DEMO OPERATION BLOCKED:"
        )
        print(
            reason
        )
        return DemoOperationalLaunchResult(
            ready=False,
            validation_result=None,
            configured_symbols=(
                configured_symbols
            ),
            healthy_symbols=(
                healthy_symbols
            ),
            account_login=(
                self._account_login(
                    self.account_info
                )
            ),
            account_server=(
                self._account_server(
                    self.account_info
                )
            ),
            account_trade_mode=(
                self._account_trade_mode(
                    self.account_info
                )
            ),
            reason=reason,
        )
    # =====================================================
    # Account Helpers
    # =====================================================
    @staticmethod
    def _account_login(
        account,
    ) -> int | None:
        if account is None:
            return None
        value = getattr(
            account,
            "login",
            None,
        )
        try:
            return (
                int(value)
                if value is not None
                else None
            )
        except (
            TypeError,
            ValueError,
        ):
            return None
    @staticmethod
    def _account_server(
        account,
    ) -> str:
        if account is None:
            return ""
        return str(
            getattr(
                account,
                "server",
                "",
            )
            or ""
        )
    def _account_trade_mode(
        self,
        account,
    ) -> str:
        if account is None:
            return "UNKNOWN"
        value = getattr(
            account,
            "trade_mode",
            None,
        )
        if (
            value
            == getattr(
                self.mt5,
                "ACCOUNT_TRADE_MODE_DEMO",
                0,
            )
        ):
            return "DEMO"
        if (
            value
            == getattr(
                self.mt5,
                "ACCOUNT_TRADE_MODE_REAL",
                2,
            )
        ):
            return "REAL"
        if (
            value
            == getattr(
                self.mt5,
                "ACCOUNT_TRADE_MODE_CONTEST",
                1,
            )
        ):
            return "CONTEST"
        return "UNKNOWN"
    # =====================================================
    # Shutdown
    # =====================================================
    def _safe_shutdown_runtime(
        self,
    ) -> None:
        self._pause_trading()
        if self.runtime is not None:
            try:
                self.runtime.stop()
            except Exception:
                pass
    def _shutdown_operation(
        self,
    ) -> None:
        if self.operation is not None:
            try:
                self.operation.stop()
            except Exception:
                pass
        self._pause_trading()
        if self.runtime is not None:
            try:
                self.runtime.stop()
            except Exception:
                pass
        try:
            self.mt5.shutdown()
        except Exception:
            pass
        print()
        print(
            "DEMO operational launcher stopped."
        )
# =========================================================
# CLI
# =========================================================
def build_argument_parser() -> argparse.ArgumentParser:
    """
    Build command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Project Phoenix M63 DEMO "
            "Operational Launcher"
        )
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help=(
            "Run exactly one controlled DEMO "
            "observation cycle."
        ),
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_OBSERVATION_DAYS,
        choices=range(
            ControlledDemoOperation.MIN_OBSERVATION_DAYS,
            ControlledDemoOperation.MAX_OBSERVATION_DAYS + 1,
        ),
        help=(
            "M63.9 observation duration "
            "(7-10 days)."
        ),
    )
    parser.add_argument(
        "--ledger",
        default=str(
            DEFAULT_LEDGER_PATH
        ),
        help=(
            "M63.9 observation JSONL ledger."
        ),
    )
    return parser
def main() -> int:
    """
    CLI entry point.
    """
    parser = (
        build_argument_parser()
    )
    args = (
        parser.parse_args()
    )
    launcher = (
        DemoOperationalLauncher(
            observation_days=args.days,
            ledger_path=args.ledger,
        )
    )
    try:
        launcher.start_observation(
            once=args.once,
        )
    except Exception as exc:
        print()
        print(
            "=" * 70
        )
        print(
            "PROJECT PHOENIX DEMO LAUNCH FAILED"
        )
        print(
            "=" * 70
        )
        print(
            str(exc)
        )
        print(
            "=" * 70
        )
        launcher._safe_shutdown_runtime()
        try:
            launcher.mt5.shutdown()
        except Exception:
            pass
        return 1
    return 0
if __name__ == "__main__":
    raise SystemExit(
        main()
    )
