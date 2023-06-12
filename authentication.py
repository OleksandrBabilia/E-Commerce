import jwt
from dotenv import dotenv_values
from passlib.context import CryptContext

from fastapi.exceptions import HTTPException
from fastapi import status

from db_models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

config_credentials = dotenv_values('.env')

def get_hashed_password(password):
    return pwd_context.hash(password)

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config_credentials['SECRET_KEY'], algorithm=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user