"""
=================================================
Project Phoenix
Pattern Manager
M33
=================================================
"""

from __future__ import annotations

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_engine import (
    PatternEngine,
)


class PatternManager:
    """
    High-level manager for Pattern Engine.
    """

    def __init__(self):

        self.engine = PatternEngine()

    def run(
        self,
        context: PatternContext,
    ) -> PatternContext:
        """
        Execute complete Pattern Engine.
        """

        return self.engine.run(
            context
        )