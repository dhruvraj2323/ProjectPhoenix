"""
=================================================
Project Phoenix
Main Application
M58
=================================================
"""

from __future__ import annotations

import sys

from deployment.bootstrap import Bootstrap


def main() -> int:
    """
    Project Phoenix entry point.
    """

    print()

    print("========================================")

    print("      Project Phoenix V1.0")

    print("   Paper Trading Deployment")

    print("========================================")

    print()

    bootstrap = Bootstrap()

    try:

        bootstrap.start()

    except KeyboardInterrupt:

        print()

        print("Shutdown requested by user.")

        bootstrap.stop()

        return 0

    except Exception as exc:

        print()

        print("Fatal Error:")

        print(exc)

        bootstrap.stop()

        return 1

    return 0


if __name__ == "__main__":

    sys.exit(
        main(),
    )