"""
=================================================
Project Phoenix
Trade Record Mapper
M60.3.1
=================================================
"""
from __future__ import annotations
from execution_engine.execution_context import (
    ExecutionContext,
)
from reporting.reporting_models import (
    TradeRecord,
)
class TradeRecordMapper:
    """
    Converts a successful ExecutionContext
    into a reporting TradeRecord.
    """
    def map(
        self,
        context: ExecutionContext,
    ) -> TradeRecord:
        if context is None:
            raise ValueError(
                "Execution context is required."
            )
        if not context.completed:
            raise RuntimeError(
                "Cannot create TradeRecord "
                "from incomplete execution."
            )
        if context.failed:
            raise RuntimeError(
                "Cannot create TradeRecord "
                "from failed execution."
            )
        execution_result = (
            context.execution_result
        )
        if execution_result is None:
            raise RuntimeError(
                "Execution result missing."
            )
        if not execution_result.accepted:
            raise RuntimeError(
                "Cannot create TradeRecord "
                "from unaccepted execution."
            )
        trade_response = (
            context.metadata.get(
                "trade_response",
            )
        )
        if trade_response is None:
            raise RuntimeError(
                "Trade response missing from "
                "execution metadata."
            )
        strategy_result = (
            context.strategy_result
        )
        if strategy_result is None:
            raise RuntimeError(
                "Strategy result missing."
            )
        if not strategy_result.signals:
            raise RuntimeError(
                "Strategy signal missing."
            )
        signal = (
            strategy_result.signals[0]
        )
        direction = getattr(
            signal.direction,
            "value",
            signal.direction,
        )
        direction = str(direction)
        strategy = getattr(
            signal.strategy_name,
            "value",
            signal.strategy_name,
        )
        strategy = str(strategy)
        pattern = ""
        signal_metadata = getattr(
            signal,
            "metadata",
            None,
        )
        if isinstance(
            signal_metadata,
            dict,
        ):
            pattern = signal_metadata.get(
                "pattern",
                "",
            )
        context_pattern = (
            context.metadata.get(
                "pattern",
                "",
            )
        )
        if not pattern and context_pattern:
            pattern = context_pattern
        stop_loss = 0.0
        take_profit = 0.0
        volume = 0.0
        if context.risk_result is not None:
            metrics = (
                context.risk_result.metrics
            )
            if metrics is not None:
                stop_loss = float(
                    getattr(
                        metrics,
                        "stop_loss",
                        0.0,
                    )
                )
                take_profit = float(
                    getattr(
                        metrics,
                        "take_profit",
                        0.0,
                    )
                )
                volume = float(
                    getattr(
                        metrics,
                        "position_size",
                        0.0,
                    )
                )
        ticket = getattr(
            trade_response,
            "ticket",
            None,
        )
        if ticket is None:
            raise RuntimeError(
                "MT5 trade ticket missing."
            )
        executed_price = float(
            getattr(
                trade_response,
                "executed_price",
                0.0,
            )
        )
        executed_volume = float(
            getattr(
                trade_response,
                "executed_volume",
                0.0,
            )
        )
        execution_time = getattr(
            trade_response,
            "execution_time",
            None,
        )
        if execution_time is None:
            raise RuntimeError(
                "Trade execution time missing."
            )
        if executed_volume > 0:
            volume = executed_volume
        return TradeRecord(
            trade_id=str(ticket),
            symbol=context.symbol,
            direction=direction,
            strategy=strategy,
            pattern=str(pattern),
            entry_price=executed_price,
            exit_price=0.0,
            stop_loss=stop_loss,
            take_profit=take_profit,
            volume=volume,
            profit_loss=0.0,
            status="OPEN",
            opened_at=execution_time,
            closed_at=execution_time,
        )
