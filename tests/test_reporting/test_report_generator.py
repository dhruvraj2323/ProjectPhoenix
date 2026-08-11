"""
=================================================
Project Phoenix
Report Generator Test
M57
=================================================
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook

from reporting.report_generator import (
    ReportGenerator,
)
from reporting.reporting_models import (
    PerformanceSummary,
    TradeRecord,
)


def test_report_generator(tmp_path):
    """
    Test complete daily XLSX report generation.
    """

    trades = [
        TradeRecord(
            trade_id="TRD-001",
            symbol="XAUUSDm",
            direction="BUY",
            strategy="Breakout",
            pattern="Bull Flag",
            entry_price=2400.00,
            exit_price=2410.00,
            stop_loss=2395.00,
            take_profit=2410.00,
            volume=0.10,
            profit_loss=125.0,
            status="CLOSED",
        ),
        TradeRecord(
            trade_id="TRD-002",
            symbol="BTCUSDm",
            direction="SELL",
            strategy="Reversal",
            pattern="Double Top",
            entry_price=65000.00,
            exit_price=64900.00,
            stop_loss=65100.00,
            take_profit=64800.00,
            volume=0.01,
            profit_loss=-50.0,
            status="CLOSED",
        ),
    ]

    summary = PerformanceSummary(
        total_trades=2,
        winning_trades=1,
        losing_trades=1,
        win_rate=50.0,
        gross_profit=125.0,
        gross_loss=50.0,
        net_profit=75.0,
        average_profit=125.0,
        average_loss=50.0,
        profit_factor=2.5,
    )

    generator = ReportGenerator()

    original_directory = (
        ReportGenerator.REPORT_DIRECTORY
    )

    try:
        ReportGenerator.REPORT_DIRECTORY = (
            tmp_path / "reports" / "Daily"
        )

        report = generator.generate(
            trades,
            summary,
        )

        # --------------------------------------------------
        # Model validation
        # --------------------------------------------------

        assert len(report.trades) == 2

        assert report.summary.total_trades == 2

        assert report.summary.winning_trades == 1

        assert report.summary.losing_trades == 1

        assert report.summary.net_profit == 75.0

        assert report.report_name.endswith(
            "_Trading_Report"
        )

        assert report.output_file.endswith(
            ".xlsx"
        )

        # --------------------------------------------------
        # Physical file validation
        # --------------------------------------------------

        output_file = Path(
            report.output_file
        )

        assert output_file.exists()

        assert output_file.is_file()

        assert output_file.stat().st_size > 0

        # --------------------------------------------------
        # Workbook validation
        # --------------------------------------------------

        workbook = load_workbook(
            output_file,
            read_only=True,
        )

        try:
            assert "Summary" in workbook.sheetnames

            assert "Trades" in workbook.sheetnames

            summary_sheet = workbook[
                "Summary"
            ]

            trades_sheet = workbook[
                "Trades"
            ]

            # --------------------------------------------------
            # Summary validation
            # --------------------------------------------------

            assert summary_sheet["A1"].value == (
                "Project Phoenix"
            )

            assert summary_sheet["A2"].value == (
                "Daily Trading Report"
            )

            assert summary_sheet["A8"].value == (
                "Total Trades"
            )

            assert summary_sheet["B8"].value == 2

            assert summary_sheet["A9"].value == (
                "Winning Trades"
            )

            assert summary_sheet["B9"].value == 1

            assert summary_sheet["A10"].value == (
                "Losing Trades"
            )

            assert summary_sheet["B10"].value == 1

            assert summary_sheet["A11"].value == (
                "Win Rate (%)"
            )

            assert summary_sheet["B11"].value == 50.0

            assert summary_sheet["A14"].value == (
                "Net Profit"
            )

            assert summary_sheet["B14"].value == 75.0

            # --------------------------------------------------
            # Trades validation
            # --------------------------------------------------

            assert trades_sheet["A1"].value == (
                "Trade ID"
            )

            assert trades_sheet["B1"].value == (
                "Symbol"
            )

            assert trades_sheet["C1"].value == (
                "Direction"
            )

            assert trades_sheet["K1"].value == (
                "Profit / Loss"
            )

            assert trades_sheet["A2"].value == (
                "TRD-001"
            )

            assert trades_sheet["B2"].value == (
                "XAUUSDm"
            )

            assert trades_sheet["K2"].value == (
                125.0
            )

            assert trades_sheet["A3"].value == (
                "TRD-002"
            )

            assert trades_sheet["B3"].value == (
                "BTCUSDm"
            )

            assert trades_sheet["K3"].value == (
                -50.0
            )

        finally:
            workbook.close()

    finally:
        ReportGenerator.REPORT_DIRECTORY = (
            original_directory
        )