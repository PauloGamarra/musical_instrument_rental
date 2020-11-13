from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import Config
from contextlib import contextmanager
from typing import Tuple, NoReturn, Callable

cfg = Config().load()

class DatabaseConnector:
    Session = None

    @classmethod
    def connect(cls: DatabaseConnector) -> NoReturn:
        """Configure and connect the database.

        It is responsible for creating an engine for the URI provided and
        configure the session.
        """
        engine = create_engine(cls._build_uri(), echo=True)
        cls.Session = sessionmaker(expire_on_commit=False)
        cls.Session.configure(bind=engine)

    @classmethod
    def get_session_scope(cls: DatabaseConnector) -> Callable:
        @contextmanager
        def session_scope(raise_exception: bool = True) -> NoReturn:
            """Provide a transactional scope around a series of operations.
            """
            session = cls.Session()
            try:
                yield session
                session.commit()
            except:
                session.rollback()
                if raise_exception:
                    raise
            finally:
                session.close()

        return session_scope

    @classmethod
    def _build_uri(cls: DatabaseConnector) -> str:
        user = cfg["RENTAL_DATABASE_USER"]
        password = cfg["RENTAL_DATABASE_PASSWORD"]
        host = cfg["RENTAL_DATABASE_HOST"]
        database = cfg["RENTAL_DATABASE_DATABASE"]
        port = cfg["RENTAL_DATABASE_PORT"]

        return f"postgresql://{user}:{password}@{host}:{port}/{database}"