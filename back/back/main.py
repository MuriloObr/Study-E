import uvicorn
import redis
from .utils.imports import FastAPI, Body, Cookie, Dict, JSONResponse, Depends
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

    return: bool
    """
    user_id = redis_client.get(session_id)
    if user_id:
        return int(str(user_id))
    else:
        return None

@app.get('/hello')
def hello():
    return { 'message': 'Hello World' }

@app.post('/register')
async def register(username: str = Body(...), 
                   email: str = Body(...), 
                   password: str = Body(...)) -> Dict[str, str]:
    result = create_user(username, email, password) 
    return {'message': result}
    
@app.post('/login')
async def login(username: str|None = Body(None),
                email: str|None = Body(None),
                password: str = Body(...)):
    if email is not None:
        response = verify_credentials_with_email(email, password)
    else:
        response = verify_credentials_with_username(username, password)
    
    if response is not None:
        user_id_bytes = str(response).encode('utf-8')  # Converte o valor em bytes
        session_id = str(gen_random_id())  # Generate a random id
        redis_client.set(session_id, user_id_bytes)  # Adiciona a session e o user id ao redis
        redis_client.expire(session_id, 7200)  # Adiciona um tempo para expirar a session (2 hora)

        # Se optarmos por configurar as rotas no FASTAPI, podemos redirecionar o usuário para outra página logo após o login.
        #redirect = RedirectResponse(url='/home', status_code=302)
        #redirect.set_cookie(key='Session', value=session_id)

        user_id_string = user_id_bytes.decode('utf-8')
        content = {'message': 'Logged.'}
        r = JSONResponse(content=content,status_code=200)
        r.set_cookie(key=session_id, value=user_id_string)
        return r

@app.post('/create_question')
def create_question_route(title:str = Body(...), content:str = Body(...), author_id = Depends(get_session)):
    if author_id is None:
        return {'message':'User not authenticated'}
    response = create_question(title, content, author_id)
    return {'message': response}

@app.post('/delete_question')
def delete_data(question_id: str = Body(...), author_id: int = Depends(get_session)):   
    """
    Função para deletar uma questão que foi publicada.
    Irá verificar se o usuário está autenticado e irá chamar a função que executa a exclusão dentro da database.
    """
    if author_id is None:
        return 'User not authenticated'
    # Vai retornar 
    response = delete_question(question_id, author_id)
    return {'message': response}

def start():
    """Launched with `poetry run dev` at root level"""
    uvicorn.run("back.main:app", host="0.0.0.0", port=8000, reload=True)
