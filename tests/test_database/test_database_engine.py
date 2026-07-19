"""
=================================================
Project Phoenix
Database Engine Test
=================================================
"""

from database.database_engine import DatabaseEngine


def run_test():

    engine = DatabaseEngine()

    result = engine.run()

    print()

    print("===== Database Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    engine.shutdown()

    print()

    print("Database Engine Test Passed")


if __name__ == "__main__":

    run_test()