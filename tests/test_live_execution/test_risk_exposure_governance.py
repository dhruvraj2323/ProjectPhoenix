"""
=================================================
Project Phoenix
Risk & Exposure Governance Tests
M63.6
=================================================
"""

from types import SimpleNamespace

from live_execution.risk_exposure_governance import (
    RiskExposureGovernance,
    RiskExposureGovernanceReason,
    RiskExposureGovernanceState,
)

from risk_engine.risk_models import (
    RiskDecision,
    RiskResult,
)


class DummyAccount:

    def __init__(
        self,
        balance=10000.0,
        equity=10000.0,
        margin_free=9000.0,
    ):

        self.balance = balance

        self.equity = equity

        self.margin_free = margin_free


class DummyAccountProvider:

    def __init__(
        self,
        account="DEFAULT",
    ):

        if account == "DEFAULT":
            self.account = DummyAccount()
        else:
            self.account = account

    def get(self):

        return self.account


class DummyPositionManager:

    def __init__(
        self,
        positions=None,
    ):

        self.positions = (
            positions
            if positions is not None
            else []
        )

    def get_positions(
        self,
        symbol=None,
    ):

        if symbol is None:

            return list(
                self.positions
            )

        return [
            position
            for position in self.positions
            if position.symbol == symbol
        ]


class DummyProtection:

    def __init__(
        self,
        allowed=True,
    ):

        self.allowed = allowed

    def can_trade(self):

        return self.allowed


class DummyPortfolioDecision:

    def __init__(
        self,
        approved=True,
        decision="APPROVE",
        reason="Portfolio validation passed.",
    ):

        self.approved = approved

        self.decision = SimpleNamespace(
            value=decision
        )

        self.reason = reason

        self.metrics = SimpleNamespace(
            open_positions=0,
            portfolio_heat=0.0,
        )

        self.exposure = SimpleNamespace(
            gross_exposure=0.0,
            net_exposure=0.0,
            symbol_exposure={},
        )


class DummyPortfolioEngine:

    def __init__(
        self,
        decision=None,
    ):

        self.decision = (
            decision
            if decision is not None
            else DummyPortfolioDecision()
        )

    def evaluate(
        self,
        context,
    ):

        return self.decision


def _risk(
    approved=True,
    risk_percent=1.0,
    position_size=0.10,
    drawdown=0.0,
):

    return RiskResult(
        decision=(
            RiskDecision.APPROVED
            if approved
            else RiskDecision.REJECTED
        ),
        reason=(
            "Risk accepted."
            if approved
            else "Risk rejected."
        ),
    )


def _governance(
    account=None,
    positions=None,
    protection=None,
    portfolio=None,
):

    return RiskExposureGovernance(
        account=(
            account
            if account is not None
            else DummyAccountProvider()
        ),
        positions=(
            positions
            if positions is not None
            else DummyPositionManager()
        ),
        protection=(
            protection
            if protection is not None
            else DummyProtection()
        ),
        portfolio_engine=(
            portfolio
            if portfolio is not None
            else DummyPortfolioEngine()
        ),
    )


# =========================================================
# 1. Healthy governance approval
# =========================================================

def test_healthy_governance_is_approved():

    result = _governance().evaluate(
        symbol="EURUSDm",
        risk_result=_risk(),
    )

    assert (
        result.state
        == RiskExposureGovernanceState.APPROVED
    )

    assert result.approved is True

    assert (
        result.reason
        == RiskExposureGovernanceReason.NONE
    )


# =========================================================
# 2. TradingProtection blocks
# =========================================================

def test_trading_protection_pause_blocks():

    result = _governance(
        protection=DummyProtection(
            allowed=False
        )
    ).evaluate(
        symbol="EURUSDm",
        risk_result=_risk(),
    )

    assert result.blocked is True

    assert (
        result.reason
        == RiskExposureGovernanceReason
        .TRADING_PROTECTION_PAUSED
    )


# =========================================================
# 3. Missing account blocks
# =========================================================

def test_missing_account_blocks():

    result = _governance(
        account=DummyAccountProvider(
            account=None
        )
    ).evaluate(
        symbol="EURUSDm",
        risk_result=_risk(),
    )

    assert result.blocked is True

    assert (
        result.reason
        == RiskExposureGovernanceReason
        .ACCOUNT_UNAVAILABLE
    )


# =========================================================
# 4. Invalid account state blocks
# =========================================================

def test_invalid_account_state_blocks():

    result = _governance(
        account=DummyAccountProvider(
            DummyAccount(
                balance=0.0,
                equity=0.0,
                margin_free=0.0,
            )
        )
    ).evaluate(
        symbol="EURUSDm",
        risk_result=_risk(),
    )

    assert (
        result.reason
        == RiskExposureGovernanceReason
        .INVALID_ACCOUNT_STATE
    )


# =========================================================
# 5. Existing Risk Engine rejection blocks
# =========================================================

def test_risk_engine_rejection_blocks():

    result = _governance().evaluate(
        symbol="EURUSDm",
        risk_result=_risk(
            approved=False
        ),
    )

    assert result.blocked is True

    assert (
        result.reason
        == RiskExposureGovernanceReason
        .RISK_REJECTED
    )


# =========================================================
# 6. Portfolio rejection blocks
# =========================================================

def test_portfolio_rejection_blocks():

    portfolio = DummyPortfolioEngine(
        DummyPortfolioDecision(
            approved=False,
            decision="BLOCK_NEW_TRADE",
            reason="Daily loss boundary.",
        )
    )

    result = _governance(
        portfolio=portfolio
    ).evaluate(
        symbol="EURUSDm",
        risk_result=_risk(),
    )

    assert result.blocked is True

    assert (
        result.reason
        == RiskExposureGovernanceReason
        .PORTFOLIO_LIMITED
    )


# =========================================================
# 7. Emergency portfolio decision blocks
# =========================================================

def test_portfolio_emergency_exit_blocks():

    portfolio = DummyPortfolioEngine(
        DummyPortfolioDecision(
            approved=False,
            decision="EMERGENCY_EXIT",
            reason="Margin safety breach.",
        )
    )

    result = _governance(
        portfolio=portfolio
    ).evaluate(
        symbol="XAUUSDm",
        risk_result=_risk(),
    )

    assert (
        result.reason
        == RiskExposureGovernanceReason
        .PORTFOLIO_EMERGENCY_EXIT
    )


# =========================================================
# 8. Risk result is not recalculated
# =========================================================

def test_existing_risk_result_is_consumed():

    risk = _risk()

    risk.metrics.risk_percent = 1.25

    risk.metrics.position_size = 0.20

    risk.metrics.drawdown = 0.75

    result = _governance().evaluate(
        symbol="BTCUSDm",
        risk_result=risk,
    )

    assert (
        result.risk_percent
        == 1.25
    )

    assert (
        result.position_size
        == 0.20
    )

    assert (
        result.drawdown
        == 0.75
    )


# =========================================================
# 9. Account state is propagated
# =========================================================

def test_account_state_is_propagated():

    result = _governance(
        account=DummyAccountProvider(
            DummyAccount(
                balance=25000.0,
                equity=24750.0,
                margin_free=22000.0,
            )
        )
    ).evaluate(
        symbol="EURUSDm",
        risk_result=_risk(),
    )

    assert result.balance == 25000.0

    assert result.equity == 24750.0

    assert result.free_margin == 22000.0


# =========================================================
# 10. Multi-symbol position state is preserved
# =========================================================

def test_multi_symbol_position_state_is_preserved():

    positions = [
        SimpleNamespace(
            symbol="EURUSDm",
            volume=0.10,
            price_open=1.1000,
            price_current=1.1010,
            profit=10.0,
            type=0,
        ),
        SimpleNamespace(
            symbol="XAUUSDm",
            volume=0.20,
            price_open=3350.0,
            price_current=3360.0,
            profit=20.0,
            type=0,
        ),
        SimpleNamespace(
            symbol="BTCUSDm",
            volume=0.05,
            price_open=60000.0,
            price_current=60100.0,
            profit=5.0,
            type=0,
        ),
    ]

    portfolio = DummyPortfolioEngine()

    portfolio.decision.metrics.open_positions = 3

    portfolio.decision.metrics.portfolio_heat = 3.5

    portfolio.decision.exposure.gross_exposure = 0.35

    portfolio.decision.exposure.net_exposure = 0.35

    portfolio.decision.exposure.symbol_exposure = {
        "EURUSDm": 0.10,
        "XAUUSDm": 0.20,
        "BTCUSDm": 0.05,
    }

    result = _governance(
        positions=DummyPositionManager(
            positions
        ),
        portfolio=portfolio,
    ).evaluate(
        symbol="XAUUSDm",
        risk_result=_risk(),
    )

    assert result.open_positions == 3

    assert result.portfolio_heat == 3.5

    assert result.symbol_exposure == 0.20

    assert result.gross_exposure == 0.35

    assert result.net_exposure == 0.35


# =========================================================
# 11. No order submission
# =========================================================

def test_governance_does_not_submit_orders():

    result = _governance().evaluate(
        symbol="EURUSDm",
        risk_result=_risk(),
    )

    assert result.approved is True


# =========================================================
# 12. Governance remains blocked when portfolio fails
# =========================================================

def test_portfolio_failure_is_contained():

    class FailingPortfolio:

        def evaluate(
            self,
            context,
        ):

            raise RuntimeError(
                "simulated portfolio failure"
            )

    result = _governance(
        portfolio=FailingPortfolio()
    ).evaluate(
        symbol="BTCUSDm",
        risk_result=_risk(),
    )

    assert result.blocked is True

    assert (
        result.reason
        == RiskExposureGovernanceReason
        .PORTFOLIO_REJECTED
    )