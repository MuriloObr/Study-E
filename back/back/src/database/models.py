from utils.imports import Column, Integer, String, ForeignKey, relationship, declarative_base
from sqlalchemy import Binary

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(Binary)
    published_questions = relationship('Questions', back_populates='author')
    published_answers = relationship('Answers', back_populates='author')

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    title = Column(String)
    author_id = ForeignKey('users.id')
    author = relationship('User', back_populates='published_questions')

class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    author_id = ForeignKey('users.id')
    author = relationship('User', back_populates='published_answers')

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)