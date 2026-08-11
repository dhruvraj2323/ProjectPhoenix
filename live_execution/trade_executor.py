"""
=================================================
Project Phoenix
Trade Executor
M59.1.8
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

    Pipeline:

        Build MT5 Request
                ↓
        Symbol Diagnostics
                ↓
        MT5 order_check()
                ↓
          Check Passed?
           /        \
         NO          YES
         ↓            ↓
      Reject       order_send()
                       ↓
                 TradeResponse
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
        # Diagnostic only.
        # --------------------------------------------------

        self._log_symbol_info(
            request.symbol,
        )

        # --------------------------------------------------
        # MT5 PRE-TRADE CHECK
        #
        # IMPORTANT:
        # order_check() MUST pass before
        # order_send() is allowed.
        # --------------------------------------------------

        check_result = self._check_order(
            context=context,
            mt5_request=mt5_request,
        )

        # --------------------------------------------------
        # Reject if MT5 pre-check failed
        # --------------------------------------------------

        if check_result is None:

            message = (
                "MT5 order_check() returned None."
            )

            response = (
                self.result_builder.failure(
                    message,
                )
            )

            context.trade_response = response

            context.fail(
                message,
            )

            return response

        check_retcode = getattr(
            check_result,
            "retcode",
            None,
        )

        check_comment = getattr(
            check_result,
            "comment",
            "",
        )

        # MT5 order_check() success retcode is 0.
        if check_retcode != 0:

            message = (
                check_comment
                or
                f"MT5 order_check() failed "
                f"with retcode={check_retcode}."
            )

            response = (
                self.result_builder.failure(
                    message=message,
                    retcode=check_retcode,
                )
            )

            context.trade_response = response

            context.fail(
                message,
            )

            return response

        # --------------------------------------------------
        # PRE-CHECK PASSED
        # --------------------------------------------------

        print()

        print(
            "===== MT5 ORDER CHECK ====="
        )

        print(
            "Status  : PASSED"
        )

        print(
            f"Retcode : {check_retcode}"
        )

        print(
            f"Comment : {check_comment}"
        )

        print(
            "==========================="
        )

        # --------------------------------------------------
        # Send Actual Order
        #
        # ONLY reached after order_check() success.
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
    # MT5 Order Check
    # ==================================================

    def _check_order(
        self,
        context: TradeContext,
        mt5_request: dict,
    ):
        """
        Run MT5 pre-trade validation.

        This method MUST complete successfully
        before order_send() is allowed.
        """

        try:

            result = mt5.order_check(
                mt5_request,
            )

        except Exception as exc:

            print()

            print(
                "===== MT5 ORDER CHECK ====="
            )

            print(
                "Status  : ERROR"
            )

            print(
                f"Reason  : {exc}"
            )

            print(
                "==========================="
            )

            return None

        # --------------------------------------------------
        # Store diagnostic information
        # --------------------------------------------------

        try:

            context.metadata[
                "mt5_order_check"
            ] = result

            context.metadata[
                "mt5_order_check_retcode"
            ] = getattr(
                result,
                "retcode",
                None,
            )

            context.metadata[
                "mt5_order_check_comment"
            ] = getattr(
                result,
                "comment",
                "",
            )

        except Exception:
            # Metadata must never break execution.
            pass

        return result

    # ==================================================
    # Symbol Diagnostics
    # ==================================================

    def _log_symbol_info(
        self,
        symbol_name: str,
    ) -> None:
        """
        Safely print MT5 symbol information.

        Diagnostic only.

        If MT5 is unavailable or symbol_info()
        returns None, execution must continue
        to the order_check() stage.
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
                "Reason          : "
                "mt5.symbol_info() returned None"
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