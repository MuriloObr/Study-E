from ..utils.imports import ForeignKey, relationship, List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    published_questions: Mapped[List["Question"]] = relationship(back_populates='author')
    published_answers: Mapped[List["Answer"]] = relationship(back_populates='author')

class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates='published_questions')
    answers: Mapped[List["Answer"]] = relationship("Answer", back_populates='question')

class Answer(Base):
    __tablename__ = 'answers'
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    author: Mapped["User"] = relationship(back_populates='published_answers')
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'), nullable=False)
    question: Mapped["Question"] = relationship(back_populates='answers')

class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)