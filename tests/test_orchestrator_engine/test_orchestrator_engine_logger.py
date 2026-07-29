"""
=================================================
Project Phoenix
Test Orchestrator Engine Logger
M39
=================================================
"""

from orchestrator_engine.orchestrator_engine_logger import (
    OrchestratorEngineLogger,
)

from orchestrator_engine.orchestrator_engine_models import (
    OrchestratorResult,
)


def test_orchestrator_engine_logger():

    logger = OrchestratorEngineLogger()

    result = OrchestratorResult(

        approved=True,

        status="SUCCESS",

        reason="Pipeline completed.",

    )

    logger.log_start()

    logger.log_stage("Market Data")

    logger.log_stage("Signal Engine")

    logger.log_stage("Strategy Engine")

    logger.log_result(result)

    logger.log_finish()

    assert result.approved is True

    assert result.status == "SUCCESS"

    assert result.reason == "Pipeline completed."