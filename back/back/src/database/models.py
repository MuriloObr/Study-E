from typing import ByteString, List
from ..utils.imports import ForeignKey, relationship
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[ByteString] = mapped_column(nullable=False)
    published_questions: Mapped[List["Question"]] = relationship(back_populates='author')
    published_answers: Mapped[List["Answer"]] = relationship(back_populates='author')

class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped["User"] = relationship(back_populates='published_questions')

class Answer(Base):
    __tablename__ = 'answers'
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped["User"] = relationship(back_populates='published_answers')

class Classes(Base):
    __tablename__ = 'classes'
    id: Mapped[int] = mapped_column(primary_key=True)