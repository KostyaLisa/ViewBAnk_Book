from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DatabaseSession:
    def __init__(self, database_url='sqlite:///atm.db'):
        # Create the SQLAlchemy engine
        self.engine = create_engine(database_url)

        # Set up the session factory with scoped sessions to manage thread safety
        self.SessionFactory = scoped_session(sessionmaker(bind=self.engine))

    def create_session(self):
        """Create and return a new session."""
        return self.SessionFactory()

    def close_session(self):
        """Close the current session."""
        self.SessionFactory.remove()

    def __enter__(self):
        """Enable usage of 'with' statements for session management."""
        self.session = self.create_session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """Handle session commit or rollback and close session."""
        try:
            if exc_type:
                self.session.rollback()  # Rollback on error
            else:
                self.session.commit()  # Commit if no exceptions
        finally:
            self.close_session()
