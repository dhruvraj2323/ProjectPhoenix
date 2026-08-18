"""
=================================================
Project Phoenix
Trade Record Mapper
M63.7 - Demo Reporting & Analytics
=================================================
"""

from __future__ import annotations

from typing import Any

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

    M63.7 responsibilities:

    - Preserve existing M60.3.1 trade mapping.
    - Capture execution observations already present
      in the execution context.
    - Capture risk observations already present.
    - Capture optional governance observations when
      an upstream integration provides them.
    - Never calculate or invent unavailable metrics.
    """

    # --------------------------------------------------
    # Public Mapping API
    # --------------------------------------------------

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

        metadata = getattr(
            context,
            "metadata",
            {},
        )

        # --------------------------------------------------
        # Trade Response
        # --------------------------------------------------

        trade_response = metadata.get(
            "trade_response",
        )

        if trade_response is None:
            raise RuntimeError(
                "Trade response missing from "
                "execution metadata."
            )

        # --------------------------------------------------
        # Strategy
        # --------------------------------------------------

        strategy_result = (
            context.strategy_result
        )

        if strategy_result is None:
            raise RuntimeError(
                "Strategy result missing."
            )

        signals = getattr(
            strategy_result,
            "signals",
            [],
        )

        if not signals:
            raise RuntimeError(
                "Strategy signal missing."
            )

        signal = signals[0]

        direction = self._enum_value(
            getattr(
                signal,
                "direction",
                "",
            )
        )

        strategy = self._enum_value(
            getattr(
                signal,
                "strategy_name",
                "",
            )
        )

        # --------------------------------------------------
        # Pattern
        # --------------------------------------------------

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
            pattern = str(
                signal_metadata.get(
                    "pattern",
                    "",
                )
            )

        context_pattern = metadata.get(
            "pattern",
            "",
        )

        if not pattern and context_pattern:
            pattern = str(
                context_pattern
            )

        # --------------------------------------------------
        # Risk
        # --------------------------------------------------

        stop_loss = 0.0

        take_profit = 0.0

        volume = 0.0

        risk_percent = None

        drawdown = None

        risk_decision = ""

        if context.risk_result is not None:

            risk_result = (
                context.risk_result
            )

            risk_decision = self._enum_value(
                getattr(
                    risk_result,
                    "decision",
                    "",
                )
            )

            metrics = getattr(
                risk_result,
                "metrics",
                None,
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

                risk_percent = (
                    self._optional_float(
                        getattr(
                            metrics,
                            "risk_percent",
                            None,
                        )
                    )
                )

                drawdown = (
                    self._optional_float(
                        getattr(
                            metrics,
                            "drawdown",
                            None,
                        )
                    )
                )

        # --------------------------------------------------
        # Trade Ticket
        # --------------------------------------------------

        ticket = getattr(
            trade_response,
            "ticket",
            None,
        )

        if ticket is None:
            raise RuntimeError(
                "MT5 trade ticket missing."
            )

        # --------------------------------------------------
        # Execution Values
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Requested Order Values
        #
        # M63.7 observes them when an upstream order
        # object is available. No synthetic value is
        # created if unavailable.
        # --------------------------------------------------

        order = getattr(
            context,
            "order",
            None,
        )

        if order is None:
            order = metadata.get(
                "trade_request",
            )

        requested_price = (
            self._optional_float(
                self._first_available(
                    order,
                    "price",
                    "entry_price",
                )
            )
        )

        requested_volume = (
            self._optional_float(
                self._first_available(
                    order,
                    "quantity",
                    "volume",
                )
            )
        )

        # --------------------------------------------------
        # Execution Status
        # --------------------------------------------------

        execution_status = self._enum_value(
            getattr(
                trade_response,
                "status",
                getattr(
                    execution_result,
                    "status",
                    "",
                ),
            )
        )

        execution_message = str(
            getattr(
                trade_response,
                "broker_message",
                "",
            )
            or ""
        )

        execution_retcode = (
            self._optional_int(
                getattr(
                    trade_response,
                    "retcode",
                    None,
                )
            )
        )

        # --------------------------------------------------
        # MT5 Order Check Diagnostics
        # --------------------------------------------------

        order_check_retcode = (
            self._optional_int(
                metadata.get(
                    "mt5_order_check_retcode",
                )
            )
        )

        order_check_message = str(
            metadata.get(
                "mt5_order_check_comment",
                "",
            )
            or ""
        )

        # --------------------------------------------------
        # Runtime State
        # --------------------------------------------------

        runtime_state = (
            "FAILED"
            if getattr(
                context,
                "failed",
                False,
            )
            else (
                "COMPLETED"
                if getattr(
                    context,
                    "completed",
                    False,
                )
                else "IN_PROGRESS"
            )
        )

        # --------------------------------------------------
        # Optional TradingProtection State
        # --------------------------------------------------

        protection_state = (
            self._metadata_value(
                metadata,
                "trading_protection_state",
            )
        )

        # --------------------------------------------------
        # Optional M63.6 Governance Result
        #
        # Supports future/actual propagation without
        # importing RiskExposureGovernance here.
        # --------------------------------------------------

        governance = (
            metadata.get(
                "risk_exposure_governance",
            )
            or
            metadata.get(
                "governance_result",
            )
        )

        governance_state = ""

        governance_reason = ""

        balance = None

        equity = None

        free_margin = None

        open_positions = None

        symbol_exposure = None

        gross_exposure = None

        net_exposure = None

        portfolio_heat = None

        if governance is not None:

            governance_state = (
                self._enum_value(
                    getattr(
                        governance,
                        "state",
                        "",
                    )
                )
            )

            governance_reason = (
                self._enum_value(
                    getattr(
                        governance,
                        "reason",
                        "",
                    )
                )
            )

            balance = self._optional_float(
                getattr(
                    governance,
                    "balance",
                    None,
                )
            )

            equity = self._optional_float(
                getattr(
                    governance,
                    "equity",
                    None,
                )
            )

            free_margin = (
                self._optional_float(
                    getattr(
                        governance,
                        "free_margin",
                        None,
                    )
                )
            )

            open_positions = (
                self._optional_int(
                    getattr(
                        governance,
                        "open_positions",
                        None,
                    )
                )
            )

            symbol_exposure = (
                self._optional_float(
                    getattr(
                        governance,
                        "symbol_exposure",
                        None,
                    )
                )
            )

            gross_exposure = (
                self._optional_float(
                    getattr(
                        governance,
                        "gross_exposure",
                        None,
                    )
                )
            )

            net_exposure = (
                self._optional_float(
                    getattr(
                        governance,
                        "net_exposure",
                        None,
                    )
                )
            )

            portfolio_heat = (
                self._optional_float(
                    getattr(
                        governance,
                        "portfolio_heat",
                        None,
                    )
                )
            )

        # --------------------------------------------------
        # Optional Market / Execution Analytics
        #
        # These values are only consumed when an
        # upstream component explicitly supplies them.
        # --------------------------------------------------

        spread = self._optional_float(
            metadata.get(
                "spread",
            )
        )

        slippage = self._optional_float(
            metadata.get(
                "slippage",
            )
        )

        mfe = self._optional_float(
            metadata.get(
                "mfe",
            )
        )

        mae = self._optional_float(
            metadata.get(
                "mae",
            )
        )

        # --------------------------------------------------
        # Observation Error
        # --------------------------------------------------

        observation_error = str(
            metadata.get(
                "reporting_observation_error",
                "",
            )
            or ""
        )

        # --------------------------------------------------
        # Build TradeRecord
        # --------------------------------------------------

        return TradeRecord(

            # Existing M57 fields
            trade_id=str(ticket),

            symbol=context.symbol,

            direction=direction,

            strategy=str(strategy),

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

            # M63.7 observation
            strategy_decision=(
                self._strategy_decision(
                    strategy_result
                )
            ),

            risk_decision=risk_decision,

            execution_status=execution_status,

            execution_message=(
                execution_message
            ),

            execution_retcode=(
                execution_retcode
            ),

            requested_price=(
                requested_price
            ),

            executed_price=(
                executed_price
            ),

            requested_volume=(
                requested_volume
            ),

            executed_volume=(
                executed_volume
            ),

            order_check_retcode=(
                order_check_retcode
            ),

            order_check_message=(
                order_check_message
            ),

            runtime_state=runtime_state,

            trading_protection_state=(
                protection_state
            ),

            governance_state=(
                governance_state
            ),

            governance_reason=(
                governance_reason
            ),

            balance=balance,

            equity=equity,

            free_margin=free_margin,

            open_positions=open_positions,

            symbol_exposure=symbol_exposure,

            gross_exposure=gross_exposure,

            net_exposure=net_exposure,

            portfolio_heat=portfolio_heat,

            risk_percent=risk_percent,

            drawdown=drawdown,

            spread=spread,

            slippage=slippage,

            mfe=mfe,

            mae=mae,

            observation_error=(
                observation_error
            ),
        )

    # ==================================================
    # Helpers
    # ==================================================

    @staticmethod
    def _enum_value(
        value: Any,
    ) -> str:
        """
        Safely extract Enum.value.
        """

        if value is None:
            return ""

        enum_value = getattr(
            value,
            "value",
            None,
        )

        if enum_value is not None:
            return str(enum_value)

        return str(value)

    @staticmethod
    def _optional_float(
        value: Any,
    ) -> float | None:
        """
        Convert a value to float when possible.
        """

        if value is None:
            return None

        try:
            return float(value)
        except (
            TypeError,
            ValueError,
        ):
            return None

    @staticmethod
    def _optional_int(
        value: Any,
    ) -> int | None:
        """
        Convert a value to int when possible.
        """

        if value is None:
            return None

        try:
            return int(value)
        except (
            TypeError,
            ValueError,
        ):
            return None

    @staticmethod
    def _first_available(
        obj: Any,
        *names: str,
    ) -> Any:
        """
        Return the first non-None attribute.
        """

        if obj is None:
            return None

        for name in names:

            value = getattr(
                obj,
                name,
                None,
            )

            if value is not None:
                return value

        return None

    @staticmethod
    def _metadata_value(
        metadata: dict[str, Any],
        key: str,
    ) -> str:
        """
        Safely convert metadata value to string.
        """

        value = metadata.get(
            key,
            "",
        )

        if value is None:
            return ""

        return TradeRecordMapper._enum_value(
            value,
        )

    @staticmethod
    def _strategy_decision(
        strategy_result: Any,
    ) -> str:
        """
        Observe the strategy result status.

        We do not invent a new strategy decision
        calculation. The existing StrategyResult status
        is the source of truth.
        """

        status = getattr(
            strategy_result,
            "status",
            "",
        )

        return TradeRecordMapper._enum_value(
            status,
        )