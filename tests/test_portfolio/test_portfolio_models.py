"""
Project Phoenix

Unit Test
Portfolio Models
"""

from portfolio.portfolio_models import (
    AllocationInfo,
    ExposureInfo,
    PortfolioContext,
    PortfolioDecision,
    PortfolioDecisionType,
    PortfolioMetrics,
    PortfolioRisk,
    PositionDirection,
    PositionInfo,
)


def test_portfolio_models():

    position = PositionInfo(
        symbol="RELIANCE",
        direction=PositionDirection.BUY,
        volume=100.0,
        entry_price=2500.0,
        current_price=2525.0,
        floating_profit=250.0,
    )

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=100250.0,
        positions=[position],
    )

    metrics = PortfolioMetrics(
        balance=100000.0,
        equity=100250.0,
        floating_profit=250.0,
        floating_loss=0.0,
        used_margin=100.0,
        free_margin=100150.0,
        margin_level=100250.0,
        portfolio_heat=0.10,
        open_positions=1,
        daily_pnl=0.0,
        weekly_pnl=0.0,
        monthly_pnl=0.0,
    )

    exposure = ExposureInfo(
        gross_exposure=100.0,
        net_exposure=100.0,
        long_exposure=100.0,
        short_exposure=0.0,
    )

    allocation = AllocationInfo(
        capital_used=10000.0,
        capital_available=90000.0,
        allocation_percent=10.0,
        risk_used=1.0,
        risk_available=99.0,
    )

    risk = PortfolioRisk(
        risk_score=0.0,
        drawdown=0.0,
        margin_risk=0.0,
        correlation_risk=0.0,
        concentration_risk=0.0,
    )

    decision = PortfolioDecision(
        decision=PortfolioDecisionType.APPROVE,
        metrics=metrics,
        exposure=exposure,
        allocation=allocation,
        risk=risk,
        approved=True,
        reason="Unit Test",
    )

    assert position.symbol == "RELIANCE"

    assert context.account_balance == 100000.0

    assert decision.approved is True

    print("Portfolio Models Test Passed")


if __name__ == "__main__":

    test_portfolio_models()