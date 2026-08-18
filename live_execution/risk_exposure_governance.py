"""
=================================================
Project Phoenix
Risk & Exposure Governance
M63.6
=================================================

Integrates live MT5 account/position state with
the existing Phoenix Risk and Portfolio boundaries.

This module does NOT:
- calculate a new strategy
- replace Risk Engine
- replace Portfolio Engine
- submit orders
- modify positions
- close positions

It provides the final live-account governance
decision before M63.5 execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from deployment.trading_protection import (
    TradingProtection,
)

from live_execution.account_info import (
    AccountInfo,
)

from live_execution.position_manager import (
    PositionManager,
)

from portfolio.portfolio_engine import (
    PortfolioEngine,
)

from portfolio.portfolio_models import (
    PortfolioContext,
    PositionDirection,
)

from risk_engine.risk_models import (
    RiskDecision,
    RiskResult,
)


class RiskExposureGovernanceState(
    Enum,
):
    """
    Final M63.6 governance state.
    """

    APPROVED = "APPROVED"

    BLOCKED = "BLOCKED"


class RiskExposureGovernanceReason(
    Enum,
):
    """
    Standard M63.6 governance reasons.
    """

    NONE = "NONE"

    TRADING_PROTECTION_PAUSED = (
        "TRADING_PROTECTION_PAUSED"
    )

    ACCOUNT_UNAVAILABLE = (
        "ACCOUNT_UNAVAILABLE"
    )

    INVALID_ACCOUNT_STATE = (
        "INVALID_ACCOUNT_STATE"
    )

    RISK_REJECTED = (
        "RISK_REJECTED"
    )

    PORTFOLIO_REJECTED = (
        "PORTFOLIO_REJECTED"
    )

    PORTFOLIO_EMERGENCY_EXIT = (
        "PORTFOLIO_EMERGENCY_EXIT"
    )

    PORTFOLIO_LIMITED = (
        "PORTFOLIO_LIMITED"
    )


@dataclass(frozen=True)
class RiskExposureGovernanceResult:
    """
    Final M63.6 governance result.
    """

    state: RiskExposureGovernanceState

    reason: RiskExposureGovernanceReason

    message: str

    balance: float = 0.0

    equity: float = 0.0

    free_margin: float = 0.0

    open_positions: int = 0

    symbol_exposure: float = 0.0

    gross_exposure: float = 0.0

    net_exposure: float = 0.0

    portfolio_heat: float = 0.0

    risk_percent: float = 0.0

    position_size: float = 0.0

    drawdown: float = 0.0

    portfolio_decision: str = ""

    risk_decision: str = ""

    metadata: dict[str, Any] | None = None

    @property
    def approved(self) -> bool:
        return (
            self.state
            == RiskExposureGovernanceState.APPROVED
        )

    @property
    def blocked(self) -> bool:
        return not self.approved


class RiskExposureGovernance:
    """
    M63.6 live-account risk and exposure
    governance boundary.
    """

    def __init__(
        self,
        account: AccountInfo | None = None,
        positions: PositionManager | None = None,
        protection: TradingProtection | None = None,
        portfolio_engine: PortfolioEngine | None = None,
    ) -> None:

        self.account = (
            account
            if account is not None
            else AccountInfo()
        )

        self.positions = (
            positions
            if positions is not None
            else PositionManager()
        )

        self.protection = (
            protection
            if protection is not None
            else TradingProtection()
        )

        self.portfolio_engine = (
            portfolio_engine
            if portfolio_engine is not None
            else PortfolioEngine()
        )

    # =====================================================
    # Main Governance Entry Point
    # =====================================================

    def evaluate(
        self,
        symbol: str,
        risk_result: RiskResult,
    ) -> RiskExposureGovernanceResult:
        """
        Evaluate whether a new trade is permitted.

        Existing Risk Engine output is consumed rather
        than recalculated.
        """

        # -------------------------------------------------
        # 1. TradingProtection
        # -------------------------------------------------

        if not self.protection.can_trade():

            return self._blocked(
                reason=(
                    RiskExposureGovernanceReason
                    .TRADING_PROTECTION_PAUSED
                ),
                message=(
                    "TradingProtection is paused. "
                    "New trading is blocked."
                ),
                risk_result=risk_result,
            )

        # -------------------------------------------------
        # 2. Account State
        # -------------------------------------------------

        account = self.account.get()

        if account is None:

            return self._blocked(
                reason=(
                    RiskExposureGovernanceReason
                    .ACCOUNT_UNAVAILABLE
                ),
                message=(
                    "MT5 account information "
                    "is unavailable."
                ),
                risk_result=risk_result,
            )

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

        if balance <= 0.0 or equity <= 0.0:

            return self._blocked(
                reason=(
                    RiskExposureGovernanceReason
                    .INVALID_ACCOUNT_STATE
                ),
                message=(
                    "MT5 account balance/equity "
                    "is invalid."
                ),
                balance=balance,
                equity=equity,
                free_margin=free_margin,
                risk_result=risk_result,
            )

        # -------------------------------------------------
        # 3. Existing Risk Engine Decision
        # -------------------------------------------------

        if (
            risk_result is None
            or
            risk_result.decision
            != RiskDecision.APPROVED
        ):

            reason = ""

            if risk_result is not None:
                reason = risk_result.reason

            return self._blocked(
                reason=(
                    RiskExposureGovernanceReason
                    .RISK_REJECTED
                ),
                message=(
                    "Existing Risk Engine "
                    "did not approve the trade."
                    + (
                        f" Reason: {reason}"
                        if reason
                        else ""
                    )
                ),
                balance=balance,
                equity=equity,
                free_margin=free_margin,
                risk_result=risk_result,
            )

        # -------------------------------------------------
        # 4. Read Current MT5 Positions
        # -------------------------------------------------

        positions = (
            self.positions.get_positions()
        )

        if positions is None:
            positions = []

        # -------------------------------------------------
        # 5. Convert MT5 positions into the existing
        #    Portfolio PositionInfo model.
        # -------------------------------------------------

        portfolio_positions = []

        for position in positions:

            position_symbol = str(
                getattr(
                    position,
                    "symbol",
                    "",
                )
            )

            volume = float(
                getattr(
                    position,
                    "volume",
                    0.0,
                )
            )

            entry_price = float(
                getattr(
                    position,
                    "price_open",
                    0.0,
                )
            )

            current_price = float(
                getattr(
                    position,
                    "price_current",
                    0.0,
                )
            )

            floating_profit = float(
                getattr(
                    position,
                    "profit",
                    0.0,
                )
            )

            position_type = getattr(
                position,
                "type",
                0,
            )

            if position_type == 0:
                direction = (
                    PositionDirection.BUY
                )
            else:
                direction = (
                    PositionDirection.SELL
                )

            currency = (
                "USD"
            )

            portfolio_positions.append(
                self._build_position_info(
                    symbol=position_symbol,
                    direction=direction,
                    volume=volume,
                    entry_price=entry_price,
                    current_price=current_price,
                    floating_profit=floating_profit,
                    currency=currency,
                )
            )

        # -------------------------------------------------
        # 6. Existing Portfolio Engine
        # -------------------------------------------------

        portfolio_context = (
            PortfolioContext(
                account_balance=balance,
                account_equity=equity,
                positions=portfolio_positions,
            )
        )

        try:

            portfolio_decision = (
                self.portfolio_engine.evaluate(
                    portfolio_context
                )
            )

        except Exception as exc:

            return self._blocked(
                reason=(
                    RiskExposureGovernanceReason
                    .PORTFOLIO_REJECTED
                ),
                message=(
                    "Portfolio governance "
                    f"failed: {exc}"
                ),
                balance=balance,
                equity=equity,
                free_margin=free_margin,
                risk_result=risk_result,
            )

        # -------------------------------------------------
        # 7. Existing Portfolio Decision
        # -------------------------------------------------

        portfolio_decision_name = (
            portfolio_decision
            .decision
            .value
        )

        if not portfolio_decision.approved:

            if (
                portfolio_decision_name
                == "EMERGENCY_EXIT"
            ):

                reason = (
                    RiskExposureGovernanceReason
                    .PORTFOLIO_EMERGENCY_EXIT
                )

            elif portfolio_decision_name in (
                "BLOCK_NEW_TRADE",
                "LIMIT_POSITION",
                "REDUCE_POSITION",
            ):

                reason = (
                    RiskExposureGovernanceReason
                    .PORTFOLIO_LIMITED
                )

            else:

                reason = (
                    RiskExposureGovernanceReason
                    .PORTFOLIO_REJECTED
                )

            return self._blocked(
                reason=reason,
                message=(
                    "Existing Portfolio Engine "
                    "blocked the new trade. "
                    f"{portfolio_decision.reason}"
                ),
                balance=balance,
                equity=equity,
                free_margin=free_margin,
                positions=positions,
                symbol=symbol,
                risk_result=risk_result,
                portfolio_decision=(
                    portfolio_decision
                ),
            )

        # -------------------------------------------------
        # 8. APPROVED
        # -------------------------------------------------

        exposure = (
            portfolio_decision.exposure
        )

        metrics = (
            portfolio_decision.metrics
        )

        symbol_exposure = (
            exposure.symbol_exposure.get(
                symbol,
                0.0,
            )
        )

        return RiskExposureGovernanceResult(

            state=(
                RiskExposureGovernanceState
                .APPROVED
            ),

            reason=(
                RiskExposureGovernanceReason
                .NONE
            ),

            message=(
                "Risk and portfolio governance "
                "approved the new trade."
            ),

            balance=balance,

            equity=equity,

            free_margin=free_margin,

            open_positions=(
                metrics.open_positions
            ),

            symbol_exposure=(
                symbol_exposure
            ),

            gross_exposure=(
                exposure.gross_exposure
            ),

            net_exposure=(
                exposure.net_exposure
            ),

            portfolio_heat=(
                metrics.portfolio_heat
            ),

            risk_percent=(
                risk_result.metrics
                .risk_percent
            ),

            position_size=(
                risk_result.metrics
                .position_size
            ),

            drawdown=(
                risk_result.metrics
                .drawdown
            ),

            portfolio_decision=(
                portfolio_decision_name
            ),

            risk_decision=(
                risk_result
                .decision
                .value
            ),

            metadata={
                "symbol": symbol,
                "risk_reason": (
                    risk_result.reason
                ),
                "portfolio_reason": (
                    portfolio_decision.reason
                ),
            },
        )

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _build_position_info(
        *,
        symbol: str,
        direction: PositionDirection,
        volume: float,
        entry_price: float,
        current_price: float,
        floating_profit: float,
        currency: str,
    ):

        from portfolio.portfolio_models import (
            PositionInfo,
        )

        return PositionInfo(
            symbol=symbol,
            direction=direction,
            volume=volume,
            entry_price=entry_price,
            current_price=current_price,
            floating_profit=floating_profit,
            currency=currency,
        )

    @staticmethod
    def _blocked(
        *,
        reason: RiskExposureGovernanceReason,
        message: str,
        balance: float = 0.0,
        equity: float = 0.0,
        free_margin: float = 0.0,
        positions=None,
        symbol: str = "",
        risk_result: RiskResult | None = None,
        portfolio_decision=None,
    ) -> RiskExposureGovernanceResult:

        positions = (
            positions
            if positions is not None
            else []
        )

        symbol_exposure = 0.0

        gross_exposure = 0.0

        net_exposure = 0.0

        open_positions = len(
            positions
        )

        if portfolio_decision is not None:

            exposure = (
                portfolio_decision.exposure
            )

            metrics = (
                portfolio_decision.metrics
            )

            symbol_exposure = (
                exposure.symbol_exposure.get(
                    symbol,
                    0.0,
                )
            )

            gross_exposure = (
                exposure.gross_exposure
            )

            net_exposure = (
                exposure.net_exposure
            )

            open_positions = (
                metrics.open_positions
            )

            portfolio_heat = (
                metrics.portfolio_heat
            )

        else:

            portfolio_heat = 0.0

        return RiskExposureGovernanceResult(

            state=(
                RiskExposureGovernanceState
                .BLOCKED
            ),

            reason=reason,

            message=message,

            balance=balance,

            equity=equity,

            free_margin=free_margin,

            open_positions=open_positions,

            symbol_exposure=symbol_exposure,

            gross_exposure=gross_exposure,

            net_exposure=net_exposure,

            portfolio_heat=portfolio_heat,

            risk_percent=(
                risk_result.metrics.risk_percent
                if risk_result is not None
                else 0.0
            ),

            position_size=(
                risk_result.metrics.position_size
                if risk_result is not None
                else 0.0
            ),

            drawdown=(
                risk_result.metrics.drawdown
                if risk_result is not None
                else 0.0
            ),

            portfolio_decision=(
                portfolio_decision.decision.value
                if portfolio_decision is not None
                else ""
            ),

            risk_decision=(
                risk_result.decision.value
                if risk_result is not None
                else ""
            ),

            metadata={
                "symbol": symbol,
                "risk_reason": (
                    risk_result.reason
                    if risk_result is not None
                    else ""
                ),
                "portfolio_reason": (
                    portfolio_decision.reason
                    if portfolio_decision is not None
                    else ""
                ),
            },
        )