"""
=================================================
Project Phoenix
Test Orchestrator Engine Pipeline
M39
=================================================
"""

from orchestrator_engine.orchestrator_engine_pipeline import (
    OrchestratorEnginePipeline,
)


def test_orchestrator_engine_pipeline():

    pipeline = OrchestratorEnginePipeline()

    stages = pipeline.stages()

    assert pipeline.total_stages() == 8

    assert len(stages) == 8

    assert stages[0].name == "Market Data"

    assert stages[1].name == "Signal Engine"

    assert stages[2].name == "Strategy Engine"

    assert stages[3].name == "Risk Engine"

    assert stages[4].name == "Execution Engine"

    assert stages[5].name == "Paper Trading"

    assert stages[6].name == "Portfolio Engine"

    assert stages[7].name == "Performance Engine"