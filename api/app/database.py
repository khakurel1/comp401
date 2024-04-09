# Import necessary modules and classes
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Define the SQLITE_DATABASE_URL constant for the database URL
SQLITE_DATABASE_URL = "sqlite:///./data.db"


# Create a SQLAlchemy engine using the SQLITE_DATABASE_URL constant
engine = create_engine(
    SQLITE_DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


# Create a session maker using the engine
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Define the Base class as a declarative base for the database models
Base = declarative_base()


# Define a function to retrieve a database session from the pool
def get_db():
    db = SessionLocal()
    try:
        # Yield the database session to be used in the function scope
        yield db
    finally:
        # Close the database session when it is no longer needed
        db.close()