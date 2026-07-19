"""
Project Phoenix
Milestone M14 - AI Decision Engine

Module:
    ai_reasoning.py

Purpose:
    Applies deterministic AI reasoning rules.
"""

from __future__ import annotations

from ai_decision.ai_models import (
    AIContext,
    AIRecommendation,
    AIDecisionStatus,
)


class AIReasoning:
    """
    Rule-based AI reasoning engine.
    """

    def evaluate(
        self,
        context: AIContext,
    ) -> AIRecommendation:
        """
        Evaluate trading context and
        generate an AI recommendation.
        """

        score = (
            context.signal_strength * 0.30
            + context.performance_score * 0.25
            + context.portfolio_score * 0.20
            + context.optimization_score * 0.15
            + (100 - context.risk_score) * 0.10
        )

        confidence = round(score / 100, 2)

        if score >= 70:

            decision = AIDecisionStatus.APPROVE

            reason = "Trading conditions are favorable."

        else:

            decision = AIDecisionStatus.REJECT

            reason = "Trading conditions are unfavorable."

        return AIRecommendation(

            decision=decision,

            confidence=confidence,

            score=round(score, 2),

            reason=reason,

        )