"""
Project Phoenix

Unit Test
Portfolio Logger
"""

from portfolio.portfolio_logger import PortfolioLogger

from portfolio.portfolio_models import (
    AllocationInfo,
    ExposureInfo,
    PortfolioDecision,
    PortfolioDecisionType,
    PortfolioMetrics,
    PortfolioRisk,
)


def test_portfolio_logger():

    metrics = PortfolioMetrics(
        balance=100000.0,
        equity=100250.0,
        floating_profit=300.0,
        floating_loss=-50.0,
        used_margin=200.0,
        free_margin=100050.0,
        margin_level=50125.0,
        portfolio_heat=0.20,
        open_positions=2,
        daily_pnl=300.0,
        weekly_pnl=500.0,
        monthly_pnl=1200.0,
    )

    exposure = ExposureInfo(
        gross_exposure=200.0,
        net_exposure=100.0,
        long_exposure=150.0,
        short_exposure=50.0,
    )

    allocation = AllocationInfo(
        capital_used=10000.0,
        capital_available=90000.0,
        allocation_percent=10.0,
        risk_used=1.0,
        risk_available=99.0,
    )

    risk = PortfolioRisk(
        risk_score=20.0,
        drawdown=2.5,
        margin_risk=1.5,
        correlation_risk=0.0,
        concentration_risk=5.0,
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

    logger = PortfolioLogger()

    logger.log(decision)

    print("\nPortfolio Logger Test Passed")


if __name__ == "__main__":

    test_portfolio_logger()