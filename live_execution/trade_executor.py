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

    def execute(
        self,
        context: TradeContext,
    ):

        request = context.trade_request

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

        result = (
            self.order_sender.send(
                mt5_request,
            )
        )

        if result is None:

            response = (
                self.result_builder.failure(
                    "MT5 returned None.",
                )
            )

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

        context.trade_response = response

        return response