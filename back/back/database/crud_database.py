from ..utils.imports import create_engine, sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.exc import NoResultFound
from back.database.models import *
from contextlib import contextmanager
from passlib.hash import bcrypt
from back.utils.get_env import DATABASE_URL

engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para retornar uma sessão da database (deve ser usado com with)
@contextmanager
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

def create_user(name: str, email: str, password: str) -> str:
    with get_db() as db:
        # Verifica se o usuário já existe no banco de dados
        if not db.query(exists().where(User.name == name)).scalar():
            return 'User already exists'

        elif not db.query(exists().where(User.email == email)).scalar():
            return 'E-mail already exists'

        # Se o usuário não existir, cria e adiciona ao banco de dados
        else:
            # Cria uma instância da classe correspondente a tabela User
            # Adiciona os novos dados e confirma a operação.
            # Cria uma hash, para salvar a senha de forma segura.
            password_hash = bcrypt.hash(password)
            new_user = User(name=name, email=email, password_hash=password_hash)
            db.add(new_user)
            db.commit()
            return 'User registered succesfully'

def verify_credentials_with_email(email, password):
    """Função para verificar se o email e a senha estão corretos na tentativa de login do usuário"""
    with get_db() as db:
        try:
            user = db.query(User).filter(User.email == email).one()
            password_hash = str(user.password_hash)
            if bcrypt.verify(password.encode('utf-8'), password_hash):
                return user.id
        except NoResultFound:
            return None

def verify_credentials_with_username(username, password):
    """Função para verificar se o username e a senha estão corretos na tentativa de login do usuário"""
    with get_db() as db:
        try:
            user = db.query(User).filter(User.username == username).one()
            password_hash = str(user.password_hash)
            if bcrypt.verify(password.encode('utf-8'), password_hash):
                return user.id
        except NoResultFound:
            return None

def create_question(title, content, author_id):...
