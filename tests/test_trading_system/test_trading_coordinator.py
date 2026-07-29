"""
=================================================
Project Phoenix
Trading Coordinator Test
=================================================
"""

from trading_system.engine_contracts import (
    MarketPipelineContract,
    StrategyEngineContract,
    RiskEngineContract,
    AIDecisionContract,
    ExecutionEngineContract,
    PaperTradingContract,
)

from trading_system.trading_context import (
    TradingContext,
)

from trading_system.trading_coordinator import (
    TradingCoordinator,
)


class DummyMarketPipeline(
    MarketPipelineContract,
):

    def execute(self, context):

        context.set_metadata(
            "Pipeline",
            "Done",
        )

        return context


class DummyStrategy(
    StrategyEngineContract,
):

    def execute(self, context):

        context.strategy_name = "EMA Strategy"

        return context


class DummyRisk(
    RiskEngineContract,
):

    def execute(self, context):

        context.risk_passed = True

        return context


class DummyAI(
    AIDecisionContract,
):

    def execute(self, context):

        context.ai_decision = "BUY"

        return context


class DummyExecution(
    ExecutionEngineContract,
):

    def execute(self, context):

        context.order_id = "ORDER-001"

        return context


class DummyPaper(
    PaperTradingContract,
):

    def execute(self, context):

        context.approve(

            decision="PAPER_EXECUTED",

            reason="Trade simulated successfully.",

        )

        return context


def test_trading_coordinator():

    coordinator = TradingCoordinator(

        market_pipeline=DummyMarketPipeline(),

        strategy_engine=DummyStrategy(),

        risk_engine=DummyRisk(),

        ai_engine=DummyAI(),

        execution_engine=DummyExecution(),

        paper_engine=DummyPaper(),

    )

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    result = coordinator.execute(
        context
    )

    assert result.strategy_name == "EMA Strategy"

    assert result.risk_passed is True

    assert result.ai_decision == "BUY"

    assert result.order_id == "ORDER-001"

    assert result.approved is True

    assert result.decision == "PAPER_EXECUTED"

    print()

    print("Trading Coordinator Test Passed")


if __name__ == "__main__":

    test_trading_coordinator()