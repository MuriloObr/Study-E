import uvicorn
from ..utils.imports import FastAPI, Body, Cookie, Dict, JSONResponse
from ..database.database import *
from ..database.config import REDIS_PASSWORD, REDIS_URL
from ..utils.generate_id import gen_random_id
import redis

app = FastAPI()
redis_client = redis.Redis(
    host=REDIS_URL,
    port=11403,
    password=REDIS_PASSWORD)

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
        response: None|Column[int] = verify_credentials_with_email(email, password)
    else:
        response: None|Column[int] = verify_credentials_with_username(username, password)
    
    if response is not None:
        user_id_bytes = str(response).encode('utf-8')  # Converte o valor em bytes
        session_id = str(gen_random_id())  # Generate a random id
        redis_client.set(session_id, user_id_bytes)  # Adiciona a session e o user id ao redis
        redis_client.expire(session_id, 3600)  # Adiciona um tempo para expirar a session (1 hora)

        # Se optarmos por configurar as rotas no FASTAPI, podemos redirecionar o usuário para outra página logo após o login.
        #redirect = RedirectResponse(url='/home', status_code=302)
        #redirect.set_cookie(key='Session', value=session_id)

        user_id_string = user_id_bytes.decode('utf-8')
        content = {'message': 'Logged.'}
        r = JSONResponse(content=content,status_code=200)
        r.set_cookie(key=session_id, value=user_id_string)
        return r

def is_authenticated(session_id: str = Cookie(...)):
    """Função para verificar se o usuário está autenticado."""
    user_id = redis_client.get(session_id)
    return user_id is not None


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("back.src.api:app", host="0.0.0.0", port=8000, reload=True)