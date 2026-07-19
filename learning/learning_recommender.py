"""
Project Phoenix
Milestone M17 - Learning Engine

Module:
    learning_recommender.py

Purpose:
    Generates optimization recommendations
    from detected learning patterns.
"""

from __future__ import annotations

from learning.learning_models import (
    LearningPattern,
    LearningRecommendation,
)


class LearningRecommender:
    """
    Generates learning recommendations.
    """

    def recommend(
        self,
        pattern: LearningPattern,
    ) -> LearningRecommendation:
        """
        Generate recommendation.
        """

        if pattern.pattern_name == "High Win Rate":

            return LearningRecommendation(

                recommendation_type="RISK_PERCENT",

                current_value=1.0,

                suggested_value=1.2,

                confidence=pattern.confidence,

                reason=(
                    "Increase position size due "
                    "to consistent profitability."
                ),

            )

        return LearningRecommendation(

            recommendation_type="RISK_PERCENT",

            current_value=1.0,

            suggested_value=0.8,

            confidence=pattern.confidence,

            reason=(
                "Reduce position size until "
                "performance improves."
            ),

        )