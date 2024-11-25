import os
from database import LocalDatabase


def test_database_initialization():
    test_db_file = "test_users.db"
    db = LocalDatabase(test_db_file)

    assert "users" in db.metadata.tables

    if os.path.exists(test_db_file):
        os.remove(test_db_file)
