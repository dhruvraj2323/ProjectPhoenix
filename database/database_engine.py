"""
=================================================
Project Phoenix
Database Engine
=================================================

Master controller for the Database Layer.
"""

from database.database_connection import DatabaseConnection
from database.database_logger import DatabaseLogger
from database.database_models import DatabaseResult
from database.database_repository import DatabaseRepository


class DatabaseEngine:
    """
    Executes the complete database workflow.
    """

    def __init__(self):

        self.db = DatabaseConnection()

    # -------------------------------------------------

    def run(self) -> DatabaseResult:

        connection = self.db.connect()

        status = self.db.initialize()

        # Initialize repository (creates tables)
        DatabaseRepository(connection)

        result = DatabaseResult(
            approved=True,
            reason="Database initialization completed successfully.",
            status=status,
        )

        DatabaseLogger.log(result)

        return result

    # -------------------------------------------------

    def shutdown(self):

        self.db.close()