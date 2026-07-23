"""
=================================================
Project Phoenix
Pattern Engine
M33
=================================================
"""

from __future__ import annotations

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_detector import (
    PatternDetector,
)

from pattern_engine.pattern_validator import (
    PatternValidator,
)

from pattern_engine.pattern_logger import (
    PatternLogger,
)


class PatternEngine:
    """
    Executes complete Pattern Engine workflow.
    """

    def __init__(self):

        self.detector = PatternDetector()

        self.validator = PatternValidator()

        self.logger = PatternLogger()

    def run(
        self,
        context: PatternContext,
    ) -> PatternContext:
        """
        Execute complete pattern detection pipeline.
        """

        self.logger.log_start(context)

        if not self.validator.validate(context):
            return context

        context = self.detector.detect(
            context
        )

        self.logger.log_complete(context)

        return context