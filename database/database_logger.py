"""
=================================================
Project Phoenix
Database Logger
=================================================

Logs database operations.
"""

from database.database_models import DatabaseResult


class DatabaseLogger:
    """
    Logs database results.
    """

    @staticmethod
    def log(result: DatabaseResult) -> None:

        print("===== Database =====")

        print(f"Approved       : {result.approved}")
        print(f"Reason         : {result.reason}")

        print()

        print(f"Connected      : {result.status.connected}")
        print(f"Initialized    : {result.status.initialized}")
        print(f"Database       : {result.status.database_name}")