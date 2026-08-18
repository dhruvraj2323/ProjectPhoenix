"""
=================================================
Project Phoenix
Test Pre-Trade Governance
M63.2
=================================================
"""

from unittest.mock import MagicMock

from live_execution.pre_trade_governance import (
    PreTradeGovernance,
)

from live_execution.trade_context import (
    TradeContext,
)


def _context():
    context = TradeContext(
        execution_id="EXEC-M63.2",
        symbol="EURUSDm",
        timeframe="M15",
    )

    context.risk_result = object()
    context.signal_result = object()
    context.strategy_result = object()
    context.ai_result = object()

    return context


def _governance():
    authorization = MagicMock()
    authorization.authorize.return_value = True

    safety = MagicMock()
    safety.validate.return_value = True

    account = MagicMock()
    account.get.return_value = object()
    account.balance.return_value = 10000.0
    account.equity.return_value = 9985.0
    account.free_margin.return_value = 9500.0

    trade_validator = MagicMock()
    trade_validator.validate.return_value = True

    governance = PreTradeGovernance(
        trading_authorization=authorization,
        safety_manager=safety,
        account_info=account,
        trade_validator=trade_validator,
    )

    return (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    )


def test_all_governance_gates_pass():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is True
    )

    authorization.authorize.assert_called_once()

    safety.validate.assert_called_once()

    account.get.assert_called_once()

    trade_validator.validate.assert_called_once()


def test_authorization_failure_blocks_governance():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    authorization.authorize.return_value = False

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )

    safety.validate.assert_not_called()
    account.get.assert_not_called()
    trade_validator.validate.assert_not_called()


def test_safety_failure_blocks_governance():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    safety.validate.return_value = False

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )

    account.get.assert_not_called()
    trade_validator.validate.assert_not_called()


def test_safety_exception_blocks_governance():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    safety.validate.side_effect = RuntimeError(
        "market validation failure"
    )

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )

    account.get.assert_not_called()
    trade_validator.validate.assert_not_called()


def test_missing_account_blocks_governance():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    account.get.return_value = None

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )

    trade_validator.validate.assert_not_called()


def test_zero_balance_blocks_governance():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    account.balance.return_value = 0.0

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )

    trade_validator.validate.assert_not_called()


def test_zero_equity_blocks_governance():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    account.equity.return_value = 0.0

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )

    trade_validator.validate.assert_not_called()


def test_zero_free_margin_blocks_governance():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    account.free_margin.return_value = 0.0

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )

    trade_validator.validate.assert_not_called()


def test_trade_validation_failure_blocks_execution():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    trade_validator.validate.return_value = False

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )


def test_trade_validation_exception_blocks_execution():

    (
        governance,
        authorization,
        safety,
        account,
        trade_validator,
    ) = _governance()

    trade_validator.validate.side_effect = RuntimeError(
        "trade validation failure"
    )

    assert (
        governance.validate(
            _context(),
            0.01,
            1.1000,
            1.0900,
            1.1200,
        )
        is False
    )