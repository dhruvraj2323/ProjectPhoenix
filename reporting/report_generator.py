"""
=================================================
Project Phoenix
Report Generator
M61.4 - Consolidated Cycle Reporting
=================================================
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from reporting.reporting_models import (
    DailyReport,
    PerformanceSummary,
    TradeRecord,
)


class ReportGenerator:
    """
    Builds and writes Daily Trading Reports.

    Responsibilities:
    - Build DailyReport model
    - Create physical XLSX workbook
    - Write performance summary sheet
    - Write trades sheet
    - Write M61.4 execution summary sheet
    - Store report under reports/Daily/
    """

    REPORT_DIRECTORY = Path("reports") / "Daily"

    # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    def generate(
        self,
        trades: list[TradeRecord],
        summary: PerformanceSummary,
        execution_summary: Any = None,
    ) -> DailyReport:
        """
        Generate complete daily report and
        create the physical XLSX file.

        execution_summary is optional to preserve
        backward compatibility with the existing
        ReportingEngine / M57 interface.
        """

        report = DailyReport()

        report.trades = trades

        report.summary = summary

        report.execution_summary = (
            execution_summary
        )

        report.report_date = datetime.now(UTC)

        report.generated_at = datetime.now(UTC)

        report.report_name = (
            report.report_date.strftime("%Y-%m-%d")
            + "_Trading_Report"
        )

        self.REPORT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            self.REPORT_DIRECTORY
            / f"{report.report_name}.xlsx"
        )

        report.output_file = str(
            output_path
        )

        self._write_workbook(
            trades=trades,
            summary=summary,
            execution_summary=execution_summary,
            output_path=output_path,
            report_date=report.report_date,
            generated_at=report.generated_at,
        )

        return report

    # --------------------------------------------------
    # Workbook
    # --------------------------------------------------

    def _write_workbook(
        self,
        trades: list[TradeRecord],
        summary: PerformanceSummary,
        execution_summary: Any,
        output_path: Path,
        report_date: datetime,
        generated_at: datetime,
    ) -> None:
        """
        Create and save the XLSX workbook.
        """

        workbook = Workbook()

        # --------------------------------------------------
        # Performance Summary
        # --------------------------------------------------

        summary_sheet = workbook.active

        summary_sheet.title = "Summary"

        # --------------------------------------------------
        # Trades
        # --------------------------------------------------

        trades_sheet = workbook.create_sheet(
            title="Trades",
        )

        # --------------------------------------------------
        # M61.4 Execution Summary
        # --------------------------------------------------

        execution_sheet = (
            workbook.create_sheet(
                title="Execution Summary",
            )
        )

        # --------------------------------------------------
        # Write Sheets
        # --------------------------------------------------

        self._write_summary_sheet(
            worksheet=summary_sheet,
            summary=summary,
            report_date=report_date,
            generated_at=generated_at,
        )

        self._write_trades_sheet(
            worksheet=trades_sheet,
            trades=trades,
        )

        self._write_execution_summary_sheet(
            worksheet=execution_sheet,
            execution_summary=execution_summary,
        )

        # --------------------------------------------------
        # Auto Size
        # --------------------------------------------------

        self._auto_size_columns(
            summary_sheet,
        )

        self._auto_size_columns(
            trades_sheet,
        )

        self._auto_size_columns(
            execution_sheet,
        )

        # --------------------------------------------------
        # Save
        # --------------------------------------------------

        workbook.save(
            output_path,
        )

        workbook.close()

    # --------------------------------------------------
    # Summary Sheet
    # --------------------------------------------------

    def _write_summary_sheet(
        self,
        worksheet,
        summary: PerformanceSummary,
        report_date: datetime,
        generated_at: datetime,
    ) -> None:
        """
        Write performance summary into Summary sheet.
        """

        worksheet["A1"] = "Project Phoenix"

        worksheet["A1"].font = Font(
            bold=True,
            size=16,
        )

        worksheet["A2"] = (
            "Daily Trading Report"
        )

        worksheet["A2"].font = Font(
            bold=True,
            size=13,
        )

        worksheet["A4"] = "Report Date"

        worksheet["B4"] = (
            report_date.strftime(
                "%Y-%m-%d"
            )
        )

        worksheet["A5"] = "Generated At"

        worksheet["B5"] = (
            generated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        worksheet["A7"] = "Metric"

        worksheet["B7"] = "Value"

        worksheet["A7"].font = Font(
            bold=True,
        )

        worksheet["B7"].font = Font(
            bold=True,
        )

        metrics = [
            (
                "Total Trades",
                summary.total_trades,
            ),
            (
                "Winning Trades",
                summary.winning_trades,
            ),
            (
                "Losing Trades",
                summary.losing_trades,
            ),
            (
                "Win Rate (%)",
                summary.win_rate,
            ),
            (
                "Gross Profit",
                summary.gross_profit,
            ),
            (
                "Gross Loss",
                summary.gross_loss,
            ),
            (
                "Net Profit",
                summary.net_profit,
            ),
            (
                "Average Profit",
                summary.average_profit,
            ),
            (
                "Average Loss",
                summary.average_loss,
            ),
            (
                "Profit Factor",
                summary.profit_factor,
            ),
        ]

        start_row = 8

        for index, (metric, value) in enumerate(
            metrics,
            start=start_row,
        ):
            worksheet.cell(
                row=index,
                column=1,
                value=metric,
            )

            worksheet.cell(
                row=index,
                column=2,
                value=value,
            )

    # --------------------------------------------------
    # Trades Sheet
    # --------------------------------------------------

    def _write_trades_sheet(
        self,
        worksheet,
        trades: list[TradeRecord],
    ) -> None:
        """
        Write individual trade records into Trades sheet.
        """

        headers = [
            "Trade ID",
            "Symbol",
            "Direction",
            "Strategy",
            "Pattern",
            "Entry Price",
            "Exit Price",
            "Stop Loss",
            "Take Profit",
            "Volume",
            "Profit / Loss",
            "Status",
            "Opened At",
            "Closed At",
        ]

        for column_index, header in enumerate(
            headers,
            start=1,
        ):
            cell = worksheet.cell(
                row=1,
                column=column_index,
                value=header,
            )

            cell.font = Font(
                bold=True,
            )

        for row_index, trade in enumerate(
            trades,
            start=2,
        ):
            values = [
                trade.trade_id,
                trade.symbol,
                trade.direction,
                trade.strategy,
                trade.pattern,
                trade.entry_price,
                trade.exit_price,
                trade.stop_loss,
                trade.take_profit,
                trade.volume,
                trade.profit_loss,
                trade.status,
                trade.opened_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                trade.closed_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            ]

            for column_index, value in enumerate(
                values,
                start=1,
            ):
                worksheet.cell(
                    row=row_index,
                    column=column_index,
                    value=value,
                )

    # --------------------------------------------------
    # M61.4
    # Execution Summary Sheet
    # --------------------------------------------------

    def _write_execution_summary_sheet(
        self,
        worksheet,
        execution_summary: Any,
    ) -> None:
        """
        Write cycle-level execution summary.

        The method intentionally accepts Any so that
        the reporting layer does not depend on the
        deployment package at runtime.
        """

        worksheet["A1"] = "Project Phoenix"

        worksheet["A1"].font = Font(
            bold=True,
            size=16,
        )

        worksheet["A2"] = (
            "Cycle Execution Summary"
        )

        worksheet["A2"].font = Font(
            bold=True,
            size=13,
        )

        # --------------------------------------------------
        # Empty / unavailable summary
        # --------------------------------------------------

        if execution_summary is None:

            worksheet["A4"] = (
                "Execution Summary"
            )

            worksheet["B4"] = (
                "Not Available"
            )

            return

        # --------------------------------------------------
        # Cycle Metrics
        # --------------------------------------------------

        worksheet["A4"] = "Cycle Status"

        worksheet["B4"] = (
            self._enum_value(
                execution_summary.status
            )
        )

        worksheet["A5"] = "Total Symbols"

        worksheet["B5"] = (
            execution_summary.total_symbols
        )

        worksheet["A6"] = (
            "Executed Symbols"
        )

        worksheet["B6"] = (
            execution_summary.executed_symbols
        )

        worksheet["A7"] = (
            "No Trade Symbols"
        )

        worksheet["B7"] = (
            execution_summary.no_trade_symbols
        )

        worksheet["A8"] = (
            "Failed Symbols"
        )

        worksheet["B8"] = (
            execution_summary.failed_symbols
        )

        # --------------------------------------------------
        # Symbol Results
        # --------------------------------------------------

        worksheet["A10"] = (
            "Symbol"
        )

        worksheet["B10"] = (
            "Status"
        )

        worksheet["C10"] = (
            "Trade ID"
        )

        worksheet["D10"] = (
            "Error"
        )

        for column in (
            "A10",
            "B10",
            "C10",
            "D10",
        ):
            worksheet[column].font = Font(
                bold=True,
            )

        results = getattr(
            execution_summary,
            "symbol_results",
            [],
        )

        for row_index, result in enumerate(
            results,
            start=11,
        ):
            worksheet.cell(
                row=row_index,
                column=1,
                value=getattr(
                    result,
                    "symbol",
                    "",
                ),
            )

            worksheet.cell(
                row=row_index,
                column=2,
                value=self._enum_value(
                    getattr(
                        result,
                        "status",
                        "",
                    )
                ),
            )

            worksheet.cell(
                row=row_index,
                column=3,
                value=getattr(
                    result,
                    "trade_id",
                    "",
                ),
            )

            worksheet.cell(
                row=row_index,
                column=4,
                value=getattr(
                    result,
                    "error",
                    "",
                ),
            )

    # --------------------------------------------------
    # Enum Utility
    # --------------------------------------------------

    @staticmethod
    def _enum_value(
        value: Any,
    ) -> str:
        """
        Return Enum.value when available.
        Otherwise return a string representation.
        """

        if value is None:
            return ""

        enum_value = getattr(
            value,
            "value",
            None,
        )

        if enum_value is not None:
            return str(enum_value)

        return str(value)

    # --------------------------------------------------
    # Column Width
    # --------------------------------------------------

    def _auto_size_columns(
        self,
        worksheet,
    ) -> None:
        """
        Automatically size worksheet columns.
        """

        for column_cells in (
            worksheet.columns
        ):
            max_length = 0

            column_letter = (
                get_column_letter(
                    column_cells[0].column,
                )
            )

            for cell in column_cells:

                value = cell.value

                if value is None:
                    continue

                value_length = len(
                    str(value),
                )

                if value_length > max_length:
                    max_length = (
                        value_length
                    )

            worksheet.column_dimensions[
                column_letter
            ].width = min(
                max_length + 2,
                40,
            )