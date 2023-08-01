from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement="auto")
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement="auto")
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    address = Column(String)
    email_verified = Column(Boolean, nullable=False, default=False)
    phone_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
