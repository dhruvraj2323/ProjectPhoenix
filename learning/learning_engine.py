"""
Project Phoenix
Milestone M17 - Learning Engine

Module:
    learning_engine.py

Purpose:
    Coordinates the complete Learning Engine.
"""

from __future__ import annotations

from learning.learning_logger import (
    LearningLogger,
)
from learning.learning_models import (
    LearningContext,
    LearningDecision,
    LearningStatus,
)
from learning.learning_patterns import (
    LearningPatternDetector,
)
from learning.learning_recommender import (
    LearningRecommender,
)
from learning.learning_validator import (
    LearningValidator,
)


class LearningEngine:
    """
    Coordinates the complete
    Learning Engine.
    """

    def __init__(self) -> None:

        self.pattern_detector = (
            LearningPatternDetector()
        )

        self.recommender = (
            LearningRecommender()
        )

        self.validator = (
            LearningValidator()
        )

        self.logger = (
            LearningLogger()
        )

    def run(
        self,
        context: LearningContext,
    ) -> LearningDecision:
        """
        Execute complete learning workflow.
        """

        pattern = (
            self.pattern_detector.detect(
                context
            )
        )

        recommendation = (
            self.recommender.recommend(
                pattern
            )
        )

        validation = (
            self.validator.validate(
                recommendation
            )
        )

        decision = LearningDecision(

            status=(
                LearningStatus.APPROVED
                if validation.valid
                else LearningStatus.REJECTED
            ),

            pattern=pattern,

            recommendation=recommendation,

            approved=validation.valid,

            reason=validation.reason,

        )

        self.logger.log(
            decision
        )

        return decision