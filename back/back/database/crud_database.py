from .models import User, Answer, Question, Subject
from ..utils.imports import create_engine, sessionmaker, HTTPException, status, Any
from sqlalchemy.exc import NoResultFound
from back.database.models import *
from contextlib import contextmanager
from passlib.hash import bcrypt
from back.utils.get_env import DATABASE_URL

engine = create_engine(DATABASE_URL)  # type: ignore
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para retornar uma sessão da database (deve ser usado com with)
@contextmanager
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

def create_user(username: str, email: str, password: str) -> str:
    with get_db() as db:
        # Verifica se o usuário já existe no banco de dados
        if db.query(User).filter_by(username=username).first() is not None:
            return 'User already exists'

        elif db.query(User).filter_by(email=email).first() is not None:
            return 'E-mail already exists'

        # Se o usuário não existir, cria e adiciona ao banco de dados
        else:
            # Cria uma instância da classe correspondente a tabela User
            # Adiciona os novos dados e confirma a operação.
            # Cria uma hash, para salvar a senha de forma segura.
            password_hash = bcrypt.hash(password).encode('utf-8')
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.add(new_user)
            db.commit()
            return 'User registered succesfully'

def verify_credentials_with_email(email, password) -> str|int|None:
    """Função para verificar se o email e a senha estão corretos na tentativa de login do usuário"""
    with get_db() as db:
        try:
            user = db.query(User).filter_by(email=email).first()
            if user is not None:
                if bcrypt.verify(password, user.password_hash):
                    return user.id
        except NoResultFound:
            return "E-mail or password not found."

def verify_credentials_with_username(username, password) -> str|int|None:
    """Função para verificar se o username e a senha estão corretos na tentativa de login do usuário"""
    with get_db() as db:
        try:
            user = db.query(User).filter_by(username=username).first()
            if user is not None:
                if bcrypt.verify(password.encode('utf-8'), str(user.password_hash)):
                    return user.id
        except NoResultFound:
            return "Username or password not found."

def create_question(title: str, content:str, author_id: int):
    """Metodo para criar uma nova pergunta na database."""
    with get_db() as db:
        try:
            # Cria uma instância do objeto que corresponde a tabela de perguntas.
            new_question = Question(title=title, content=content, author_id=author_id)

            # Adiciona á database
            db.add(new_question)
            db.commit()
            db.refresh(new_question)

            # Retorna o id
            return new_question.id
        except Exception as e:
            db.rollback()
            return f'Um erro ocorreu ao tentar criar a questão: {str(e)}'

def delete_question(question_id:Any, author_id:int):
    """
    Função para realizar a exclusão na database.
    
    Verifica se a question_id existe.
    Verifica se o usuário é o criador da question.
    """
    with get_db() as db:
        question = db.query(Question).filter_by(question_id=question_id).first()
        if question is None:
            return f'Question com id {question_id} não encontrado.',
        if question.author_id != author_id:
            return f'Você não tem permissão para deletar essa question.',

        try:
            db.delete(question)
            db.commit()
        except Exception as e:
            db.rollback()  # Para reverter em caso de erro.
            return f'Um erro ocorreu ao tentar deletar a questão: {str(e)}.'

def add_answer_to_question(question_id:str, content:str, author_id: int):
    """Função para adicionar uma resposta a uma questão."""
    with get_db() as db:
        question = db.query(Question).filter_by(id=question_id).first()
        if question is None:
            return f'Questão com id: {question_id} não encontrada.'
        new_answer = Answer(content=content, author_id=author_id)
        question.answers.append(new_answer)
        db.commit()
        return f'Resposta adicionada com sucesso. answer_id: {new_answer.id}'