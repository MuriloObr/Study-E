from .models import User, Answer, Question, Subject
from ..utils.imports import create_engine, sessionmaker, HTTPException, status, Any, Callable, Dict
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

def easy_db(func):
    """
    Decorator para facilitar algumas operações repetitivas na database.

    Args: 
        filter_dict (Dict): Dicionário contendo os critérios de filtragem. A key deve ser o nome da coluna e a chave deve ser o valor a ser buscado no filtro para essa coluna.
    """
    def wrapper(*args, **kwargs):
        with get_db() as _db:
            def quick_query(obj: Any, filter_dict: Dict[str, Any]):
                query = _db.query(obj).filter_by(**filter_dict).first()
                if query is not None:
                    return query
                else:
                    return None
            try:
                kwargs['db'] = _db
                kwargs['quick_query'] = quick_query
            except:
                pass

            result = func(*args, **kwargs)
            # Tenta confirmar as alterações na database
            try:
                _db.commit()
            # Se não for possível, volta as alterações.
            except Exception as e:
                print(f"Erro ao commitar: {str(e)}")
                _db.rollback()
        return result
    return wrapper

@easy_db
def create_user(db, quick_query, username: str, email: str, password: str) -> str:
    """Função para criar um novo usuário na database."""
    # Verifica se o usuário já existe no banco de dados
    if quick_query(User, {'username':username}) is not None:
        return 'User already exists'

    elif quick_query(User, {'email': email}) is not None:
        return 'E-mail already exists'

    # Se o usuário não existir, cria e adiciona ao banco de dados
    else:
        # Cria uma hash, para salvar a senha de forma segura.
        password_hash = bcrypt.hash(password).encode('utf-8')
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.add(new_user)
        return 'User registered succesfully'

@easy_db
def verify_credentials_with_email(quick_query, email, password) -> str|int|None:
    """Função para verificar se o email e a senha estão corretos na tentativa de login do usuário"""
    try:
        user = quick_query(User, {'email':email})
        if user is not None:
            if bcrypt.verify(password, user.password_hash):
                return user.id
    except NoResultFound:
        return "E-mail or password not found."

@easy_db
def verify_credentials_with_username(quick_query, username, password) -> str|int|None:
    """Função para verificar se o username e a senha estão corretos na tentativa de login do usuário"""
    try:
        user = quick_query(User, {'username': username})
        if user is not None:
            if bcrypt.verify(password.encode('utf-8'), str(user.password_hash)):
                return user.id
    except NoResultFound:
        return "Username or password not found."

@easy_db
def create_question(db, title: str, content:str, author_id: int):
    """Metodo para criar uma nova pergunta na database."""
    try:
        new_question = Question(title=title, content=content, author_id=author_id)
        db.add(new_question)
        return new_question.id
    except Exception as e:
        return f'Um erro ocorreu ao tentar criar a questão: {str(e)}'

@easy_db
def delete_question(db, quick_query, question_id:Any, author_id:int):
    """Função para realizar a exclusão na database."""
    question = quick_query(Question, {'question_id':question_id})
    if question is None:
        return f'Question com id {question_id} não encontrado.',
    # Verifica se o author id da question é o mesmo de quem está solicitando a exclusão.
    if question.author_id != author_id:
        return f'Você não tem permissão para deletar essa question.',
    try:
        db.delete(question)
    except Exception as e:
        return f'Um erro ocorreu ao tentar deletar a questão: {str(e)}.'

@easy_db
def add_answer_to_question(quick_query, question_id:str, content:str, author_id: int):
    """Função para adicionar uma resposta a uma questão."""
    question = quick_query(Question, {'id':question_id})
    if question is None:
        return f'Questão com id: {question_id} não encontrada.'
    new_answer = Answer(content=content, author_id=author_id)
    question.answers.append(new_answer)
    return f'Resposta adicionada com sucesso.\nAnswer id: {new_answer.id}'

@easy_db
def delete_answer_from_question(db, quick_query, answer_id: str, author_id: int):
    answer = quick_query(Answer, {'id':answer_id})
    if answer.author_id == author_id:
        db.delete(answer)
    else:
        return f'Você não tem autorização para excluir essa resposta.'