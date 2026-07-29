"""
=================================================
Project Phoenix
System Integration Test
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

from trading_system.system_integration import (
    TradingSystem,
)

from trading_system.trading_context import (
    TradingContext,
)

from trading_system.trading_coordinator import (
    TradingCoordinator,
)


class DummyPipeline(MarketPipelineContract):

    def execute(self, context):

        return context


class DummyStrategy(StrategyEngineContract):

    def execute(self, context):

        context.strategy_name = "EMA Strategy"

        return context


class DummyRisk(RiskEngineContract):

    def execute(self, context):

        context.risk_passed = True

        return context


class DummyAI(AIDecisionContract):

    def execute(self, context):

        context.ai_decision = "BUY"

        return context


class DummyExecution(ExecutionEngineContract):

    def execute(self, context):

        context.order_id = "ORDER-001"

        return context


class DummyPaper(PaperTradingContract):

    def execute(self, context):

        context.approve(

            decision="PAPER_EXECUTED",

            reason="Paper trade completed.",

        )

        return context


def test_system_integration():

    coordinator = TradingCoordinator(

        market_pipeline=DummyPipeline(),

        strategy_engine=DummyStrategy(),

        risk_engine=DummyRisk(),

        ai_engine=DummyAI(),

        execution_engine=DummyExecution(),

        paper_engine=DummyPaper(),

    )

    system = TradingSystem(
        coordinator,
    )

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    report = system.execute(
        context,
    )

    summary = report.summary()

    assert summary["approved"] is True

    assert summary["decision"] == "PAPER_EXECUTED"

    assert summary["strategy_name"] == "EMA Strategy"

    assert summary["ai_decision"] == "BUY"

    print()

    print("System Integration Test Passed")


if __name__ == "__main__":

    test_system_integration()