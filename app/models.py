from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement="auto")
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="Cascade"), nullable=False)
    owner = relationship("users")
    owner = relationship("comments")


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


class votes(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="Cascade"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="Cascade"), nullable=False, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class comments(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True,
                        nullable=False, autoincrement="auto")
    comment = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="Cascade"), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="Cascade"), nullable=False)
    commentree = Column(Integer, ForeignKey(
        "comments.comment_id", ondelete="Cascade"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
