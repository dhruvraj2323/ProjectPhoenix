"""
=================================================
Project Phoenix
Risk Processor
M59.7.5C
=================================================
"""

from __future__ import annotations

from risk_engine.risk_context import (
    RiskContext,
)

from risk_engine.risk_models import (
    RiskDecision,
)

from risk_engine.swing_detector import (
    SwingDetector,
)

from strategy.strategy_models import (
    TradeDirection,
)


class RiskProcessor:
    """
    Performs risk calculations.
    """

    def __init__(
        self,
    ) -> None:

        self.detector = (
            SwingDetector()
        )

    # --------------------------------------------------

    def process(
        self,
        context: RiskContext,
    ) -> RiskContext:
        """
        Calculate risk metrics.
        """

        metrics = (
            context.risk_result.metrics
        )

        # ---------------------------------------------
        # Risk %
        # ---------------------------------------------

        if context.balance > 0:

            metrics.risk_percent = (

                (context.balance - context.free_margin)

                / context.balance

            ) * 100.0

        else:

            metrics.risk_percent = 0.0

        # ---------------------------------------------
        # Position Size
        # ---------------------------------------------

        metrics.position_size = 0.10

        # ---------------------------------------------
        # Exposure
        # ---------------------------------------------

        metrics.exposure = (

            context.balance

            - context.free_margin

        )

        # ---------------------------------------------
        # Margin Required
        # ---------------------------------------------

        metrics.margin_required = (

            context.balance * 0.01

        )

        # ---------------------------------------------
        # Drawdown
        # ---------------------------------------------

        if context.balance > 0:

            metrics.drawdown = max(

                0.0,

                (

                    (context.balance - context.equity)

                    / context.balance

                )

                * 100.0,

            )

        else:

            metrics.drawdown = 0.0

        # =============================================
        # Swing Detection
        # =============================================

        if context.candles:

            metrics.swing_high = (
                self.detector.last_swing_high(
                    context.candles,
                )
            )

            metrics.swing_low = (
                self.detector.last_swing_low(
                    context.candles,
                )
            )

        # =============================================
        # Dynamic Stop Loss / Take Profit
        # =============================================

        signal = None

        if (

            context.strategy_result
            and
            context.strategy_result.signals

        ):

            signal = (
                context.strategy_result.signals[0]
            )

        if signal is not None:

            entry = (
                signal.entry_price
            )

            if (
                signal.direction
                ==
                TradeDirection.BUY
            ):

                metrics.stop_loss = (
                    metrics.swing_low
                )

                risk = (
                    entry
                    -
                    metrics.stop_loss
                )

                metrics.take_profit = (

                    entry

                    +

                    (
                        risk
                        *
                        metrics.risk_reward
                    )

                )

            else:

                metrics.stop_loss = (
                    metrics.swing_high
                )

                risk = (

                    metrics.stop_loss

                    -

                    entry

                )

                metrics.take_profit = (

                    entry

                    -

                    (
                        risk
                        *
                        metrics.risk_reward
                    )

                )

        # ---------------------------------------------
        # Final Decision
        # ---------------------------------------------

        context.risk_result.decision = (
            RiskDecision.APPROVED
        )

        context.risk_result.reason = (
            "Risk Calculated"
        )

        return context

        print()

        print("===== RISK ENGINE =====")

        print(
            f"Position Size : {metrics.position_size}"
        )

        print(
            f"Swing High    : {metrics.swing_high}"
        )

        print(
            f"Swing Low     : {metrics.swing_low}"
        )

        print(
            f"Stop Loss     : {metrics.stop_loss}"
        )

        print(
            f"Take Profit   : {metrics.take_profit}"
        )

        print("=======================")