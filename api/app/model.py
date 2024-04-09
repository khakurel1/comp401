# Import necessary modules and classes
from __future__ import annotations
from passlib.context import CryptContext
from .database import Base
from sqlalchemy import TIMESTAMP, Column, String, JSON, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy import ForeignKey


# Define the Notification class
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    user = Column(ForeignKey("users.id"))
    message = Column(String, nullable=False, default="")
    createdAt = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    read = Column(Boolean, default=False)


# Define the Job class
class Job(Base):
    __tablename__ = "jobs"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    evaluation = Column(ForeignKey("evaluations.id"))
    createdAt = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    startedAt = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
    completedAt = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
    done = Column(Boolean, default=False)


# Define the User class
class User(Base):
    __tablename__ = "users"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    username = Column(String(256), nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    createdAt = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


# Define the Evaluation class
class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    tickers = Column(JSON, nullable=False, default=False)
    createdAt = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    data = Column(JSON, nullable=True)
    user = Column(ForeignKey("users.id"))


# Define the CryptContext object for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define a function to verify a password against a hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Define a function to hash a password using the CryptContext object
def get_password_hash(password):
    return pwd_context.hash(password)