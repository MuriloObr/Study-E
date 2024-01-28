from .models import User, Answer, Question, Subject
from ..utils.imports import create_engine, sessionmaker, Any, Dict, HTTPException, JSONResponse
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
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
def quick_query(obj: Any, filter_dict: Dict[str, Any]) -> Any|None:
    "Função para realizar consultas rapidas na database"
    with get_db() as _db:
        query = _db.query(obj).filter_by(**filter_dict).first()
        return query

def create_user(username: str, email: str, password: str):
    """
    Função para criar um novo usuário na database.
    
    Returns:
        Retorna um JSONResponse com o código 200 e uma mensagem indicando que a operação foi bem sucedida.
    """
    with get_db() as db:
        # Verifica se o usuário já existe no banco de dados
        if quick_query(User, {'username':username}) is not None:
            raise HTTPException(status_code=400, detail='User already exists.')

        elif quick_query(User, {'email': email}) is not None:
            raise HTTPException(status_code=400, detail='E-mail already exists.')

        # Se o usuário não existir, cria e adiciona ao banco de dados
        else:
            # Cria uma hash, para salvar a senha de forma segura.
            password_hash = bcrypt.hash(password).encode('utf-8')
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.add(new_user)
            return JSONResponse(content={'message': f'User created successfully.'}, status_code=200)

def verify_credentials(password, email=None, username=None):
    """
    Função para verificar se o email e a senha estão corretos na tentativa de login do usuário

    Returns:
        Retorna um JSONResponse com o código 200 e o id do usuário.
    """
    try:
        col = 'email' if email is not None else 'username'
        query = email if email is not None else username
        user = quick_query(User, {col:query})
        if user is not None:
            if bcrypt.verify(password, user.password_hash):
                return user.id
            else:
                raise HTTPException(status_code=401, detail='Invalid password.')
    except NoResultFound:
        raise HTTPException(status_code=400, detail='E-mail not found.')

def create_question(title: str, content:str, author_id: int):
    """
    Função para criar uma nova pergunta na database.

    Returns:
        Retorna um JSONResponse com o código 200 e o id da questão que foi criada.
    """
    with get_db() as db:
        try:
            title_exists = quick_query(Question, {'title': title})
            if title_exists is not None:
                raise HTTPException(status_code=400, detail='Title already exists.')
            new_question = Question(title=title, content=content,author_id=author_id)
            db.add(new_question)
            db.commit()
            return JSONResponse(content={'question_id': new_question.id}, status_code=200)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f'Error creating question: {str(e)}.')

def delete_question(question_id: int, author_id:int):
    """
    Função para realizar a exclusão de uma pergunta.

    Returns:
        Retorna uma JSONResponse com código 200 e indicando que a operação foi bem sucedida.
    """
    with get_db() as db:
        question = quick_query(Question, {'id': question_id})
        if question is None:
            raise HTTPException(status_code=404, detail=f'Question with id: {question_id} not found.')
        # Verifica se o id do autor da pergunta é o mesmo de quem está solicitando a exclusão.
        if question.author_id != author_id:
            raise HTTPException(status_code=403, detail=f'You do not have permission to delete this question.')
        try:
            db.delete(question)
            db.commit()
            return JSONResponse(content={'message': f'Question with id: {str(question_id)} was successfully deleted.'}, status_code=200)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f'Error deleting the question: {str(e)}')

def add_answer_to_question(question_id:str, content:str, author_id: int):
    """
    Função para adicionar uma resposta a uma questão.

    Returns:
        Retorna um JSONResponse com o id da resposta que foi criada.
    """
    question = quick_query(Question, {'id':question_id})
    if question is None:
        raise HTTPException(status_code=404, detail=f'Question with id: {question_id} not found.')
    new_answer = Answer(content=content, author_id=author_id)
    question.answers.append(new_answer)
    return JSONResponse(content={'answer_id': new_answer.id}, status_code=200)

def delete_answer_from_question(answer_id: str, author_id: int):
    """
    Função para deletar uma resposta.

    Returns:
        Retorna um JSONResponse com código 200 e uma mensagem indicando que a operação foi bem sucedida.
    """
    with get_db() as db:
        answer = quick_query(Answer, {'id':answer_id})
        if answer is not None:
            if answer.author_id == author_id:
                db.delete(answer)
                db.commit()
                return JSONResponse(content={'message': 'Answer successfully deleted.'}, status_code=200)
            else:
                raise HTTPException(status_code=403, detail=f'You do not have permission to delete this answer.')
        else:
            raise HTTPException(status_code=404, detail=f'Answer with id: {str(answer_id)} not found.')
        