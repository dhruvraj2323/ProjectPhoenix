"""
=================================================
Project Phoenix
Test Paper Trading Validator
M24
=================================================
"""

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_validator import (
    PaperValidator,
)


def test_paper_validator():

    validator = PaperValidator()

    context = PaperContext(

        paper_id="PAPER-001",

        account_id="ACC-001",

    )

    context.execution_result = object()

    assert validator.validate(context) is True

    invalid = PaperContext(

        paper_id="",

        account_id="ACC-001",

    )

    invalid.execution_result = object()

    assert validator.validate(invalid) is False

    assert invalid.failed is True

    assert invalid.reason == "Paper ID is missing."

    invalid = PaperContext(

        paper_id="PAPER-002",

        account_id="ACC-002",

    )

    invalid.portfolio.balance = -100

    invalid.execution_result = object()

    assert validator.validate(invalid) is False

    assert invalid.reason == "Invalid virtual balance."

    invalid = PaperContext(

        paper_id="PAPER-003",

        account_id="ACC-003",

    )

    assert validator.validate(invalid) is False

    assert invalid.reason == "Execution result not available."