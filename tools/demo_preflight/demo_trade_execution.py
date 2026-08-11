"""
=================================================
Project Phoenix
MT5 Demo Trade Execution V1.0
=================================================

Purpose:

Execute ONE controlled demo trade through the
existing Project Phoenix live-execution pipeline.

IMPORTANT:

This script is DEMO ONLY.

Execution path:

TradeContext
    ↓
TradeEngine
    ↓
TradeRequestBuilder
    ↓
TradeExecutor
    ↓
MT5 order_check()
    ↓
OrderSender
    ↓
MT5 order_send()
    ↓
TradeResponse

First controlled trade:

Symbol : XAUUSDm
Side   : BUY
Volume : 0.01

This script does NOT bypass Phoenix execution
components.
"""

from __future__ import annotations

import os
import sys

import MetaTrader5 as mt5


# ==================================================
# Project Root
# ==================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT,
    )

from strategy.strategy_models import (
    StrategyResult,
    StrategySignal,
    StrategyType,
    TradeDirection,
)

from risk_engine.risk_models import (
    RiskMetrics,
    RiskResult,
)

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_engine import (
    TradeEngine,
)


# ==================================================
# Configuration
# ==================================================

SYMBOL = "XAUUSDm"

TIMEFRAME = "M1"

VOLUME = 0.01

EXECUTION_ID = "DEMO-EXEC-001"


# ==================================================
# MT5 Environment Validation
# ==================================================

def validate_mt5() -> bool:

    print()
    print("===== MT5 DEMO VALIDATION =====")

    initialized = mt5.initialize()

    print(
        "Initialized     :",
        initialized,
    )

    if not initialized:

        print(
            "Last Error      :",
            mt5.last_error(),
        )

        return False

    terminal = mt5.terminal_info()

    if terminal is None:

        print(
            "Terminal        : unavailable"
        )

        return False

    print(
        "Connected       :",
        terminal.connected,
    )

    print(
        "Trade Allowed   :",
        terminal.trade_allowed,
    )

    print(
        "Trade API Off   :",
        terminal.tradeapi_disabled,
    )

    account = mt5.account_info()

    if account is None:

        print(
            "Account         : unavailable"
        )

        print(
            "Last Error      :",
            mt5.last_error(),
        )

        return False

    print(
        "Account Login   :",
        account.login,
    )

    print(
        "Server          :",
        account.server,
    )

    print(
        "Balance         :",
        account.balance,
    )

    print(
        "Equity          :",
        account.equity,
    )

    print(
        "Account Trade   :",
        account.trade_allowed,
    )

    print(
        "Account Expert  :",
        account.trade_expert,
    )

    # --------------------------------------------------
    # Safety: Demo server verification
    # --------------------------------------------------

    if "Exness-MT5Trial" not in account.server:

        print()
        print(
            "=========================================="
        )

        print(
            "SAFETY STOP"
        )

        print(
            "Unexpected MT5 server:"
        )

        print(
            account.server
        )

        print(
            "This script is DEMO ONLY."
        )

        print(
            "=========================================="
        )

        return False

    # --------------------------------------------------
    # Symbol validation
    # --------------------------------------------------

    symbol = mt5.symbol_info(
        SYMBOL,
    )

    if symbol is None:

        print(
            "Symbol          : unavailable"
        )

        print(
            "Last Error      :",
            mt5.last_error(),
        )

        return False

    print()
    print("===== SYMBOL =====")

    print(
        "Symbol          :",
        symbol.name,
    )

    print(
        "Visible         :",
        symbol.visible,
    )

    print(
        "Trade Mode      :",
        symbol.trade_mode,
    )

    print(
        "Execution Mode  :",
        symbol.trade_exemode,
    )

    print(
        "Digits          :",
        symbol.digits,
    )

    print(
        "Volume Min      :",
        symbol.volume_min,
    )

    print(
        "Volume Step     :",
        symbol.volume_step,
    )

    # --------------------------------------------------
    # Volume validation
    # --------------------------------------------------

    if VOLUME < symbol.volume_min:

        print()
        print(
            "ERROR: Volume below broker minimum."
        )

        return False

    # --------------------------------------------------
    # Live tick validation
    # --------------------------------------------------

    tick = mt5.symbol_info_tick(
        SYMBOL,
    )

    if tick is None:

        print(
            "Live Tick       : unavailable"
        )

        print(
            "Last Error      :",
            mt5.last_error(),
        )

        return False

    print()
    print("===== LIVE TICK =====")

    print(
        "Bid             :",
        tick.bid,
    )

    print(
        "Ask             :",
        tick.ask,
    )

    if tick.ask <= 0:

        print(
            "ERROR: Invalid Ask price."
        )

        return False

    return True


# ==================================================
# Build Phoenix Context
# ==================================================

def build_context() -> TradeContext:

    # --------------------------------------------------
    # Strategy Signal
    #
    # This is an explicit controlled DEMO BUY.
    #
    # Actual MARKET price will be resolved by
    # TradeRequestBuilder from the live MT5 tick.
    # --------------------------------------------------

    signal = StrategySignal(

        strategy_id="DEMO",

        strategy_name=(
            StrategyType.S01_EMA_TREND
        ),

        direction=TradeDirection.BUY,

        confidence=100,

        entry_price=0.0,

        stop_loss=0.0,

        take_profit=0.0,

        risk_percent=1,

        reason="Controlled Demo Execution Test",

    )

    strategy_result = StrategyResult()

    strategy_result.signals.append(
        signal,
    )

    # --------------------------------------------------
    # Risk Result
    #
    # For this first controlled test:
    # fixed broker-valid minimum volume.
    # --------------------------------------------------

    risk_result = RiskResult()

    risk_result.metrics = RiskMetrics(

        position_size=VOLUME,

        stop_loss=0.0,

        take_profit=0.0,

    )

    # --------------------------------------------------
    # Trade Context
    # --------------------------------------------------

    context = TradeContext(

        execution_id=EXECUTION_ID,

        symbol=SYMBOL,

        timeframe=TIMEFRAME,

    )

    context.strategy_result = (
        strategy_result
    )

    context.signal_result = (
        object()
    )

    context.risk_result = (
        risk_result
    )

    context.ai_result = (
        object()
    )

    return context


# ==================================================
# Execute Demo Trade
# ==================================================

def execute_demo_trade() -> int:

    print()
    print("=" * 50)
    print("PROJECT PHOENIX DEMO TRADE EXECUTION V1.0")
    print("=" * 50)

    print()
    print("!!! DEMO ACCOUNT ONLY !!!")
    print()
    print(
        "Symbol :",
        SYMBOL,
    )

    print(
        "Side   : BUY"
    )

    print(
        "Volume :",
        VOLUME,
    )

    # --------------------------------------------------
    # Validate MT5
    # --------------------------------------------------

    if not validate_mt5():

        return 1

    # --------------------------------------------------
    # Build Context
    # --------------------------------------------------

    context = build_context()

    # --------------------------------------------------
    # Confirmation
    # --------------------------------------------------

    print()
    print("===== EXECUTION SAFETY =====")

    print(
        "Account : DEMO"
    )

    print(
        "Server  : Exness-MT5Trial"
    )

    print(
        "Symbol  :",
        SYMBOL,
    )

    print(
        "Side    : BUY"
    )

    print(
        "Volume  :",
        VOLUME,
    )

    print()
    print(
        "Phoenix TradeEngine will now execute."
    )

    # --------------------------------------------------
    # Phoenix Execution Path
    # --------------------------------------------------

    engine = TradeEngine()

    result = engine.run(
        context,
    )

    # --------------------------------------------------
    # Result
    # --------------------------------------------------

    print()
    print("===== DEMO EXECUTION RESULT =====")

    print(
        "Completed       :",
        result.completed,
    )

    print(
        "Failed          :",
        result.failed,
    )

    print(
        "Reason          :",
        result.reason,
    )

    print(
        "Trade Response  :",
        result.trade_response,
    )

    # --------------------------------------------------
    # Trade Response
    # --------------------------------------------------

    response = result.trade_response

    if response is not None:

        print()

        print(
            "Ticket          :",
            response.ticket,
        )

        print(
            "Executed Price  :",
            response.executed_price,
        )

        print(
            "Executed Volume :",
            response.executed_volume,
        )

        print(
            "Broker Message  :",
            response.broker_message,
        )

        print(
            "Retcode         :",
            response.retcode,
        )

    # --------------------------------------------------
    # Final
    # --------------------------------------------------

    print()
    print("=" * 50)

    if (
        result.completed
        and response is not None
    ):

        print(
            "DEMO TRADE EXECUTED SUCCESSFULLY"
        )

        print(
            "IMPORTANT: Verify the position in MT5."
        )

        print(
            "================================================"
        )

        return 0

    print(
        "DEMO TRADE EXECUTION FAILED"
    )

    print(
        "Check the execution diagnostics above."
    )

    print(
        "================================================"
    )

    return 1


# ==================================================
# Main
# ==================================================

def main() -> int:

    try:

        return execute_demo_trade()

    finally:

        mt5.shutdown()

        print()
        print(
            "MT5 Shutdown     : Complete"
        )


if __name__ == "__main__":

    raise SystemExit(
        main()
    )