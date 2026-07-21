"""
Project Phoenix
Milestone M14 - AI Decision Engine

Module:
    ai_engine.py

Purpose:
    Coordinates the complete AI
    Decision Engine.
"""

from __future__ import annotations

from ai_decision.ai_logger import (
    AILogger,
)

from ai_decision.ai_models import (
    AIContext,
    AIDecision,
)

from ai_decision.ai_reasoning import (
    AIReasoning,
)

from ai_decision.ai_scoring import (
    AIScoring,
)

from ai_decision.ai_validator import (
    AIValidator,
)


class AIEngine:
    """
    Coordinates the complete AI
    Decision Engine.
    """

    def __init__(self) -> None:

        self.reasoning = AIReasoning()

        self.scoring = AIScoring()

        self.validator = AIValidator()

        self.logger = AILogger()

    def evaluate(
        self,
        context: AIContext,
    ) -> AIDecision:
        """
        Execute complete AI workflow.
        """

        recommendation = self.reasoning.evaluate(
            context
        )

        recommendation.score = self.scoring.calculate(
            recommendation
        )

        validation = self.validator.validate(
            recommendation
        )

        decision = AIDecision(

            recommendation=recommendation,

            approved=validation.valid,

            reason=validation.reason,

        )

        self.logger.log(
            decision
        )

        return decision