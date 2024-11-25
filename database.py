from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.types import Date
from loguru import logger


class LocalDatabase:
    def __init__(self, db_file_name: str = "users.db"):
        self.engine = create_engine(f"sqlite:///{db_file_name}")
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()  # Initialize metadata
        self.metadata.bind = self.engine  # Bind metadata to the engine
        self.users_table = self._initialize_database()

    def get_connection(self) -> Session:
        """Returns session connection to local database."""
        return self.Session()

    def _initialize_database(self) -> Table:
        """Initializes the database schema."""
        inspector = inspect(self.engine)
        if "users" not in inspector.get_table_names():
            logger.info("Users table not found. Creating schema...")
            users_table = Table(
                "users",
                self.metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("first_name", String, nullable=False),
                Column("last_name", String, nullable=False),
                Column("date_of_birth", Date, nullable=False),
            )
            try:
                self.metadata.create_all(self.engine)
                logger.info("Database schema created successfully.")
            except SQLAlchemyError as e:
                logger.error(f"An error occurred during database initialization: {e}")
        else:
            logger.info("Database schema already exists. Skipping initialization.")
            users_table = Table("users", self.metadata, autoload_with=self.engine)

        # Reflect metadata to ensure it's in sync
        self.metadata.reflect(bind=self.engine)
        return users_table


# Instantiate the database globally
db_instance = LocalDatabase()
