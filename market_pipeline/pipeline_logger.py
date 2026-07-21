"""
=================================================
Project Phoenix
Market Pipeline Logger
M31
=================================================
"""

from __future__ import annotations

import logging

from market_pipeline.pipeline_context import PipelineContext


class PipelineLogger:
    """
    Central logger for the Market Pipeline.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger("ProjectPhoenix.MarketPipeline")

        if not self.logger.handlers:

            handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "[%(levelname)s] %(message)s"
            )

            handler.setFormatter(formatter)

            self.logger.addHandler(handler)

            self.logger.setLevel(logging.INFO)

    # ---------------------------------------------------------

    def log_start(
        self,
        context: PipelineContext,
    ) -> None:

        self.logger.info(
            f"Pipeline Started | "
            f"ID={context.pipeline_id} "
            f"Symbol={context.symbol} "
            f"Timeframe={context.timeframe}"
        )

    # ---------------------------------------------------------

    def log_stage(
        self,
        context: PipelineContext,
    ) -> None:

        self.logger.info(
            f"Stage -> {context.current_stage.value}"
        )

    # ---------------------------------------------------------

    def log_complete(
        self,
        context: PipelineContext,
    ) -> None:

        self.logger.info(
            f"Pipeline Completed | "
            f"Approved={context.approved}"
        )

    # ---------------------------------------------------------

    def log_failure(
        self,
        context: PipelineContext,
    ) -> None:

        self.logger.error(
            f"Pipeline Failed | "
            f"Reason={context.reason}"
        )