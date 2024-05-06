from __future__ import annotations
from passlib.context import CryptContext
from .database import Base
from sqlalchemy import TIMESTAMP, Column, String, JSON, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy import ForeignKey

GUID.cache_ok = True


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
    success = Column(Boolean, default=False)

    def to_dict(self, with_rel: bool = False):
        response = {
            "id": self.id,
            "type": self.__tablename__,
            "attributes": {
                "message": self.message,
                "created_at": self.createdAt,
                "read": self.read,
                "success": self.success
            }
        }
        if (with_rel):
            response["relationships"] = {
                User.__tablename__: {
                    "data": {
                        "id": self.user,
                        "type": User.__tablename__,
                    }
                }
            }
        return response


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

    def to_dict(self, with_rel: bool = False):
        response = {
            "id": self.id,
            "type": self.__tablename__,
            "attributes": {
                "created_at": self.createdAt,
                "started_at": self.startedAt,
                "completed_at": self.completedAt,
                "done": self.done,
            }
        }
        if (with_rel):
            response["relationships"] = {
                Evaluation.__tablename__: {
                    "data": {
                        "id": self.evaluation,
                        "type": Evaluation.__tablename__,
                    }
                }
            }
        return response


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

    def to_dict(self, with_rel: bool = False):
        response = {
            "id": self.id,
            "type": self.__tablename__,
            "attributes": {
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "created_at": self.createdAt,
            }
        }
        return response


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

    def to_dict(self, with_rel: bool = False):
        response = {
            "id": self.id,
            "type": self.__tablename__,
            "attributes": {
                "tickers": self.tickers,
                "created_at": self.createdAt,
                "data": self.data,
            }
        }
        if (with_rel):
            response["relationships"] = {
                User.__tablename__: {
                    "data": {
                        "id": self.user,
                        "type": User.__tablename__,
                    }
                }
            }
        return response


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
