"""
=================================================
Project Phoenix
Create Market Test Data
=================================================

Creates a lightweight historical ZIP file for
unit and integration testing.

Input:
    data/raw/historical/
    HISTDATA_COM_MT_XAUUSD_M1_2009_2020.zip

Output:
    tests/test_data/sample_xauusd.zip
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path


SOURCE_ZIP = Path(
    "data/raw/historical/HISTDATA_COM_MT_XAUUSD_M1_2009_2020.zip"
)

OUTPUT_ZIP = Path(
    "tests/test_data/sample_xauusd.zip"
)

MAX_LINES = 50


def main() -> None:

    if not SOURCE_ZIP.exists():
        raise FileNotFoundError(
            f"Source file not found:\n{SOURCE_ZIP}"
        )

    OUTPUT_ZIP.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with zipfile.ZipFile(SOURCE_ZIP, "r") as source_zip:

        members = source_zip.namelist()

        if not members:
            raise RuntimeError(
                "Source ZIP contains no files."
            )

        first_file = members[0]

        with source_zip.open(first_file) as fp:

            lines = fp.read().decode(
                "utf-8",
                errors="ignore",
            ).splitlines()

        sample = lines[:MAX_LINES]

    buffer = io.BytesIO()

    with zipfile.ZipFile(
        buffer,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as out_zip:

        out_zip.writestr(
            first_file,
            "\n".join(sample),
        )

    OUTPUT_ZIP.write_bytes(
        buffer.getvalue()
    )

    print("=" * 50)
    print("Project Phoenix Test Data Created")
    print("=" * 50)
    print(f"Source : {SOURCE_ZIP}")
    print(f"Output : {OUTPUT_ZIP}")
    print(f"Lines  : {len(sample)}")


if __name__ == "__main__":
    main()