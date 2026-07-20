"""
=================================================
Project Phoenix
Analytics Engine
=================================================

Calculates trading analytics.
"""


class AnalyticsEngine:
    """
    Performs trading performance calculations.
    """

    def calculate(
        self,
        winning_trades: int,
        losing_trades: int,
        gross_profit: float,
        gross_loss: float,
    ):

        total_trades = winning_trades + losing_trades

        win_rate = (
            (winning_trades / total_trades) * 100
            if total_trades
            else 0.0
        )

        loss_rate = (
            (losing_trades / total_trades) * 100
            if total_trades
            else 0.0
        )

        net_profit = gross_profit - gross_loss

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else float("inf")
        )

        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate, 2),
            "loss_rate": round(loss_rate, 2),
            "gross_profit": gross_profit,
            "gross_loss": gross_loss,
            "net_profit": net_profit,
            "profit_factor": round(profit_factor, 2),
        }