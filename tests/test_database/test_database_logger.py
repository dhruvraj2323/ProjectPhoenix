"""
=================================================
Project Phoenix
Database Logger Test
=================================================
"""

from database.database_logger import DatabaseLogger
from database.database_models import (
    DatabaseResult,
    DatabaseStatus,
)


def run_test():

    status = DatabaseStatus(
        connected=True,
        initialized=True,
        database_name="project_phoenix.db",
    )

    result = DatabaseResult(
        approved=True,
        reason="Database initialized successfully.",
        status=status,
    )

    DatabaseLogger.log(result)

    assert result.approved

    print()
    print("Database Logger Test Passed")


if __name__ == "__main__":

    run_test()