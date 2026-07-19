"""
Project Phoenix

Unit Test
Portfolio Validator
"""

from portfolio.portfolio_validator import (
    PortfolioValidator,
)

from portfolio.portfolio_models import (
    AllocationInfo,
    ExposureInfo,
    PortfolioContext,
    PortfolioLimits,
    PortfolioMetrics,
    PositionDirection,
    PositionInfo,
)


def _build_metrics(**overrides):

    defaults = dict(
        balance=100000.0,
        equity=100000.0,
        floating_profit=0.0,
        floating_loss=0.0,
        used_margin=1000.0,
        free_margin=99000.0,
        margin_level=1000.0,
        portfolio_heat=1.0,
        open_positions=1,
        daily_pnl=0.0,
        weekly_pnl=0.0,
        monthly_pnl=0.0,
    )

    defaults.update(overrides)

    return PortfolioMetrics(**defaults)


def _build_allocation():

    return AllocationInfo(
        capital_used=10000.0,
        capital_available=90000.0,
        allocation_percent=10.0,
        risk_used=1.0,
        risk_available=99.0,
    )


def _build_exposure():

    return ExposureInfo(
        gross_exposure=100.0,
        net_exposure=100.0,
        long_exposure=100.0,
        short_exposure=0.0,
    )


def test_portfolio_validator_approve():

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=100000.0,
        positions=[],
    )

    validator = PortfolioValidator()

    result = validator.validate(
        context=context,
        metrics=_build_metrics(),
        exposure=_build_exposure(),
        allocation=_build_allocation(),
        correlation_risk=0.0,
    )

    print("===== Portfolio Validator: Healthy =====")
    print(f"Decision : {result.decision.value}")
    print(f"Valid    : {result.valid}")
    print(f"Reason   : {result.reason}")

    assert result.valid is True
    assert result.decision.value == "APPROVE"

    print("\nPortfolio Validator Approve Test Passed")


def test_portfolio_validator_emergency_exit_margin():

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=100000.0,
        positions=[],
        limits=PortfolioLimits(min_margin_level=150.0),
    )

    validator = PortfolioValidator()

    result = validator.validate(
        context=context,
        metrics=_build_metrics(margin_level=110.0),
        exposure=_build_exposure(),
        allocation=_build_allocation(),
        correlation_risk=0.0,
    )

    print("===== Portfolio Validator: Low Margin =====")
    print(f"Decision : {result.decision.value}")
    print(f"Reason   : {result.reason}")

    assert result.valid is False
    assert result.decision.value == "EMERGENCY_EXIT"

    print("\nPortfolio Validator Emergency Exit Test Passed")


def test_portfolio_validator_block_daily_loss():

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=94000.0,
        positions=[],
        limits=PortfolioLimits(daily_loss_limit_percent=5.0),
    )

    validator = PortfolioValidator()

    result = validator.validate(
        context=context,
        metrics=_build_metrics(daily_pnl=-6000.0),
        exposure=_build_exposure(),
        allocation=_build_allocation(),
        correlation_risk=0.0,
    )

    print("===== Portfolio Validator: Daily Loss Breach =====")
    print(f"Decision : {result.decision.value}")
    print(f"Reason   : {result.reason}")

    assert result.valid is False
    assert result.decision.value == "BLOCK_NEW_TRADE"

    print("\nPortfolio Validator Daily Loss Test Passed")


def test_portfolio_validator_limit_correlation():

    context = PortfolioContext(
        account_balance=100000.0,
        account_equity=100000.0,
        positions=[],
        limits=PortfolioLimits(max_correlation_percent=85.0),
    )

    validator = PortfolioValidator()

    result = validator.validate(
        context=context,
        metrics=_build_metrics(),
        exposure=_build_exposure(),
        allocation=_build_allocation(),
        correlation_risk=100.0,
    )

    print("===== Portfolio Validator: High Correlation =====")
    print(f"Decision : {result.decision.value}")
    print(f"Reason   : {result.reason}")

    assert result.valid is False
    assert result.decision.value == "LIMIT_POSITION"

    print("\nPortfolio Validator Correlation Test Passed")


if __name__ == "__main__":

    test_portfolio_validator_approve()
    test_portfolio_validator_emergency_exit_margin()
    test_portfolio_validator_block_daily_loss()
    test_portfolio_validator_limit_correlation()