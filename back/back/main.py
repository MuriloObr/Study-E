import uvicorn
import redis
from .utils.imports import FastAPI, Body, Cookie, Dict, JSONResponse, Depends, HTTPException, status
from .database.crud_database import *
from .utils.generate_id import gen_random_id
from back.utils.get_env import REDIS_URL, REDIS_PASSWORD


app = FastAPI()
redis_client = redis.Redis(
    host=REDIS_URL,  # type: ignore
    port=11403,
    password=REDIS_PASSWORD)

def get_session(session_id: str = Cookie(...)) -> int|None:
    """
    Função para verificar se o usuário está autenticado.
    A função irá buscar pela session armazenada nos Cookies e realizar uma busca no banco de dados do Redis para pegar o id do usuário.

    Args:
        session_id (str): O identificador da sessão armazenado nos cookies.
    
    Returns: 
        int|None Retorna o ID do usuário se a sessão ainda for válida. 
                Retorna None se a sessão já tiver expirado ou não for válida.
    """
    try:
        user_id = redis_client.get(session_id).decode('utf-8')  # type: ignore
        if user_id:
            return int(str(user_id))
        else:
            return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error retrieving user session: {str(e)}'
        )
        
@app.get('/hello')
def hello():
    return { 'message': 'Hello World' }

@app.post('/register')
async def register(username: str = Body(...), 
                   email: str = Body(...), 
                   password: str = Body(...)):
    create_user(username=username, email=email, password=password) 
    
@app.post('/login')
async def login(username: str|None = Body(None),
                email: str|None = Body(None),
                password: str = Body(...)):
    if email is None and username is None:
        return {'message': 'An e-mail or username must be informed.'}

    elif email is not None:
        response = verify_credentials(email=email, password=password)
    else:
        response = verify_credentials(username=username, password=password)
    
    if response is not None:
        user_id_bytes = str(response).encode('utf-8')  # Converte o valor em bytes
        session_id = str(gen_random_id())  # Generate a random id
        redis_client.set(session_id, user_id_bytes)  # Adiciona a session e o user id ao redis
        redis_client.expire(session_id, 7200)  # Adiciona um tempo para expirar a session (2 hora)

        content = {'message': 'Logged.'}
        r = JSONResponse(content=content,status_code=200)
        r.set_cookie(key='session_id', value=session_id)
        return r

@app.post('/create_question')
async def create_question_route(title:str = Body(...), content:str = Body(...), author_id: int = Depends(get_session)):
    if author_id is None:
        return {'message': 'User not authenticated.'}
    create_question(title, content, author_id)

@app.post('/delete_question')
async def delete_question_route(question_id: int = Body(...), author_id: int = Depends(get_session)):   
    """
    Função para deletar uma questão que foi publicada.
    Irá verificar se o usuário está autenticado e irá chamar a função que executa a exclusão dentro da database.
    """
    if author_id is None:
        return {'message':'User not authenticated'}
    delete_question(question_id, author_id)

def start():
    """Launched with `poetry run dev` at root level"""
    uvicorn.run("back.main:app", host="0.0.0.0", port=9000, reload=True)
