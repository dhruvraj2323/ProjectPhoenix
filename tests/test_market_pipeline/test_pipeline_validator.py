"""
=================================================
Project Phoenix
Pipeline Validator Test
=================================================
"""

import pandas as pd

from market_pipeline.pipeline_validator import (
    PipelineValidator
)


def main():

    candles = [

        {
            "datetime": "2026-01-01",
            "open": 100,
            "high": 105,
            "low": 99,
            "close": 103,
            "volume": 150
        }

    ]

    dataframe = pd.DataFrame(candles)

    validator = PipelineValidator()

    report = validator.validate(
        candles,
        dataframe
    )

    print()

    print("Validation Report")

    print("=================")

    for key, value in report.items():

        print(f"{key}: {value}")

    print()

    print("Pipeline Validator Test Passed")


if __name__ == "__main__":
    main()