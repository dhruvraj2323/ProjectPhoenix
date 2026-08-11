"""
=================================================
Project Phoenix
Trade Executor
M59.1.7
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_result import (
    TradeResultBuilder,
)

from live_execution.order_sender import (
    OrderSender,
)


class TradeExecutor:
    """
    Executes MT5 market orders.

    Responsibilities:
    - Build MT5 order request
    - Send order through OrderSender
    - Convert MT5 response into TradeResponse
    - Update TradeContext
    - Provide safe diagnostic logging
    """

    def __init__(
        self,
    ) -> None:

        self.result_builder = (
            TradeResultBuilder()
        )

        self.order_sender = (
            OrderSender()
        )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
        context: TradeContext,
    ):
        request = context.trade_request

        # --------------------------------------------------
        # Validate Trade Request
        # --------------------------------------------------

        if request is None:

            response = (
                self.result_builder.failure(
                    "Trade request missing.",
                )
            )

            context.trade_response = response

            context.fail(
                "Trade request missing.",
            )

            return response

        # --------------------------------------------------
        # Build MT5 Request
        # --------------------------------------------------

        mt5_request = {
            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": request.symbol,

            "volume": request.volume,

            "type": (
                mt5.ORDER_TYPE_BUY
                if request.side.value == "BUY"
                else mt5.ORDER_TYPE_SELL
            ),

            "price": request.price,

            "sl": request.stop_loss,

            "tp": request.take_profit,

            "deviation": request.deviation,

            "magic": request.magic_number,

            "comment": request.comment,

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": (
                mt5.ORDER_FILLING_IOC
            ),
        }

        # --------------------------------------------------
        # Symbol Diagnostics
        #
        # IMPORTANT:
        # symbol_info() is diagnostic only.
        # Failure to retrieve symbol information must
        # never crash trade execution.
        # --------------------------------------------------

        self._log_symbol_info(
            request.symbol,
        )

        # --------------------------------------------------
        # Send Order
        # --------------------------------------------------

        result = (
            self.order_sender.send(
                mt5_request,
            )
        )

        # --------------------------------------------------
        # Handle None Response
        # --------------------------------------------------

        if result is None:

            response = (
                self.result_builder.failure(
                    "MT5 returned None.",
                )
            )

            context.fail(
                "MT5 returned None.",
            )

        # --------------------------------------------------
        # Successful Execution
        # --------------------------------------------------

        elif (
            result.retcode
            == mt5.TRADE_RETCODE_DONE
        ):

            response = (
                self.result_builder.success(

                    ticket=result.order,

                    price=result.price,

                    volume=result.volume,

                    message=result.comment,

                    retcode=result.retcode,
                )
            )

            context.complete()

        # --------------------------------------------------
        # Failed Execution
        # --------------------------------------------------

        else:

            response = (
                self.result_builder.failure(

                    message=result.comment,

                    retcode=result.retcode,
                )
            )

            context.fail(
                result.comment,
            )

        # --------------------------------------------------
        # Store Response
        # --------------------------------------------------

        context.trade_response = response

        # --------------------------------------------------
        # MT5 Result Diagnostics
        # --------------------------------------------------

        print()

        print(
            "========== MT5 RESULT =========="
        )

        print(
            result
        )

        print()

        print(
            "Last Error :",
            mt5.last_error(),
        )

        print(
            "==============================="
        )

        print()

        return response

    # ==================================================
    # Symbol Diagnostics
    # ==================================================

    def _log_symbol_info(
        self,
        symbol_name: str,
    ) -> None:
        """
        Safely print MT5 symbol information.

        This method is diagnostic only.

        If MT5 is unavailable or symbol_info()
        returns None, execution must continue
        to the OrderSender.
        """

        try:

            symbol = mt5.symbol_info(
                symbol_name,
            )

        except Exception as exc:

            print()

            print(
                "===== SYMBOL INFO ====="
            )

            print(
                f"Symbol          : {symbol_name}"
            )

            print(
                "Symbol Info     : unavailable"
            )

            print(
                f"Reason          : {exc}"
            )

            print(
                "======================="
            )

            return

        print()

        print(
            "===== SYMBOL INFO ====="
        )

        print(
            f"Symbol          : {symbol_name}"
        )

        # --------------------------------------------------
        # MT5 symbol_info() returned None
        # --------------------------------------------------

        if symbol is None:

            print(
                "Symbol Info     : unavailable"
            )

            print(
                "Reason          : mt5.symbol_info() returned None"
            )

            print(
                "======================="
            )

            return

        # --------------------------------------------------
        # Safe Symbol Information
        # --------------------------------------------------

        print(
            f"Name            : {symbol.name}"
        )

        print(
            f"Visible         : {symbol.visible}"
        )

        print(
            f"Trade Mode      : {symbol.trade_mode}"
        )

        print(
            f"Execution Mode  : {symbol.trade_exemode}"
        )

        print(
            f"Filling Mode    : {symbol.filling_mode}"
        )

        print(
            f"Stops Level     : {symbol.trade_stops_level}"
        )

        print(
            f"Freeze Level    : {symbol.trade_freeze_level}"
        )

        print(
            "======================="
        )