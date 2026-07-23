"""
=================================================
Project Phoenix
Processing Report
M31
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext


class ProcessingReport:
    """
    Generates a standardized pipeline report.
    """

    def generate(
        self,
        context: PipelineContext,
    ) -> str:
        """
        Generate report.
        """

        report = []

        report.append("=" * 60)
        report.append("PROJECT PHOENIX")
        report.append("MARKET PIPELINE REPORT")
        report.append("=" * 60)

        report.append("")
        report.append("GENERAL INFORMATION")
        report.append(f"Pipeline ID : {context.pipeline_id}")
        report.append(f"Symbol      : {context.symbol}")
        report.append(f"Timeframe   : {context.timeframe}")
        report.append(f"Stage       : {context.current_stage}")

        report.append("")
        report.append("PIPELINE STATUS")
        report.append(f"Completed   : {context.completed}")
        report.append(f"Approved    : {context.approved}")
        report.append(f"Failed      : {context.failed}")

        report.append("")
        report.append("PIPELINE RESULTS")
        report.append(f"Decision    : {context.decision}")
        report.append(f"Reason      : {context.reason}")

        report.append("")
        report.append("RUNTIME DATA")
        report.append(
            f"Indicators  : {len(context.indicators)}"
        )
        report.append(
            f"Patterns    : {len(context.patterns)}"
        )
        report.append(
            f"Metadata    : {len(context.metadata)}"
        )

        report.append("=" * 60)

        return "\n".join(report)

    # ---------------------------------------------------------

    def print_report(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Print report.
        """

        print(
            self.generate(context)
        )