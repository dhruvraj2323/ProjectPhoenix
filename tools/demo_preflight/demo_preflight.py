"""
=================================================
Project Phoenix
MT5 Demo Pre-Flight V1.0
=================================================

Purpose:

Validate the real MT5 Demo environment before
any actual order is sent.

IMPORTANT:

This script MUST NOT call mt5.order_send().

Flow:

MT5 Initialize
        ↓
Terminal / Account Validation
        ↓
Symbol Validation
        ↓
Live Tick
        ↓
Build Demo BUY Request
        ↓
MT5 order_check()
        ↓
PASS
        ↓
STOP

No actual order is sent.
"""

from __future__ import annotations

import MetaTrader5 as mt5


# ==================================================
# Configuration
# ==================================================

SYMBOL = "XAUUSDm"
VOLUME = 0.01
DEVIATION = 20
MAGIC = 26081101
COMMENT = "ProjectPhoenix_PRECHECK"


# ==================================================
# Main
# ==================================================

def main() -> int:

    print()
    print("=" * 50)
    print("PROJECT PHOENIX MT5 DEMO PRE-FLIGHT V1.0")
    print("=" * 50)

    # --------------------------------------------------
    # MT5 Initialize
    # --------------------------------------------------

    initialized = mt5.initialize()

    print()
    print("MT5 Initialized :", initialized)

    if not initialized:

        print(
            "ERROR           :",
            mt5.last_error(),
        )

        return 1

    try:

        # --------------------------------------------------
        # Terminal
        # --------------------------------------------------

        terminal = mt5.terminal_info()

        print()
        print("===== TERMINAL =====")

        if terminal is None:

            print(
                "Terminal       : unavailable"
            )

            return 1

        print(
            "Connected       :",
            terminal.connected,
        )

        print(
            "Trade Allowed   :",
            terminal.trade_allowed,
        )

        print()
        print("===== TERMINAL =====")

        if terminal is None:

            print(
                "Terminal       : unavailable"
            )

            return 1

        print(
            "Connected       :",
            terminal.connected,
        )

        print(
            "Trade Allowed   :",
            terminal.trade_allowed,
        )

        print(
            "Trade API Disabled:",
            terminal.tradeapi_disabled,
        )

        print(
            "Server/Terminal :",
            terminal.name,
        )

        print(
            "Build           :",
            terminal.build,
        )

        print(
            "Server          :",
            terminal.name,
        )

        print(
            "Build           :",
            terminal.build,
        )

        # --------------------------------------------------
        # Account
        # --------------------------------------------------

        account = mt5.account_info()

        print()
        print("===== ACCOUNT =====")

        if account is None:

            print(
                "Account         : unavailable"
            )

            print(
                "Last Error      :",
                mt5.last_error(),
            )

            return 1

        print(
            "Login           :",
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
            "Trade Allowed   :",
            account.trade_allowed,
        )

        print(
            "Trade Expert    :",
            account.trade_expert,
        )

        # --------------------------------------------------
        # Symbol
        # --------------------------------------------------

        symbol = mt5.symbol_info(
            SYMBOL,
        )

        print()
        print("===== SYMBOL =====")

        if symbol is None:

            print(
                "Symbol          :",
                SYMBOL,
            )

            print(
                "Status          : NOT FOUND"
            )

            print(
                "Last Error      :",
                mt5.last_error(),
            )

            return 1

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
            "Filling Mode    :",
            symbol.filling_mode,
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
        # Live Tick
        # --------------------------------------------------

        tick = mt5.symbol_info_tick(
            SYMBOL,
        )

        print()
        print("===== LIVE TICK =====")

        if tick is None:

            print(
                "Tick            : unavailable"
            )

            print(
                "Last Error      :",
                mt5.last_error(),
            )

            return 1

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
                "ERROR           : Invalid Ask price"
            )

            return 1

        # --------------------------------------------------
        # Build BUY Request
        # --------------------------------------------------

        price = round(
            float(tick.ask),
            int(symbol.digits),
        )

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": SYMBOL,

            "volume": VOLUME,

            "type": mt5.ORDER_TYPE_BUY,

            "price": price,

            "deviation": DEVIATION,

            "magic": MAGIC,

            "comment": COMMENT,

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": (
                mt5.ORDER_FILLING_IOC
            ),
        }

        print()
        print("===== DEMO REQUEST =====")

        print(
            "Symbol          :",
            SYMBOL,
        )

        print(
            "Side            : BUY"
        )

        print(
            "Volume          :",
            VOLUME,
        )

        print(
            "Price           :",
            price,
        )

        print(
            "Magic           :",
            MAGIC,
        )

        print(
            "Comment         :",
            COMMENT,
        )

        # --------------------------------------------------
        # Safety Check
        # --------------------------------------------------

        print()
        print("===== SAFETY =====")

        print(
            "order_send()    : NOT CALLED"
        )

        # --------------------------------------------------
        # MT5 Order Check
        # --------------------------------------------------

        print()
        print("===== MT5 ORDER CHECK =====")

        check = mt5.order_check(
            request,
        )

        if check is None:

            print(
                "Status          : FAILED"
            )

            print(
                "Last Error      :",
                mt5.last_error(),
            )

            return 1

        print(
            "Retcode         :",
            check.retcode,
        )

        print(
            "Comment         :",
            check.comment,
        )

        # MT5 order_check success retcode = 0

        if check.retcode != 0:

            print()
            print(
                "=========================================="
            )

            print(
                "DEMO PRE-FLIGHT FAILED"
            )

            print(
                "=========================================="
            )

            return 1

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        print()
        print(
            "=========================================="
        )

        print(
            "DEMO PRE-FLIGHT PASSED"
        )

        print(
            "NO ORDER SENT"
        )

        print(
            "=========================================="
        )

        return 0

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