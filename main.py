from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from starlette.responses import HTMLResponse

from tortoise.contrib.fastapi import register_tortoise
from tortoise.signals import post_save
from tortoise import BaseDBAsyncClient

from typing import Optional, Type, List

from emails import * 
from db_models import User, Business, Product
from pydentic_models import (
    user_pydenticIn,
    user_pydenticOut,
    user_pydentic,
    business_pydentic,
)
from authentication import get_hashed_password, verify_token, token_generator

app = FastAPI()

templates = Jinja2Templates(directory='templates')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_user(token: str=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config_credentials['SECRET'], algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        
    return await user

@app.post('/user/me')
async def user_login(user: user_pydenticIn=Depends(get_current_user)):
    business = await Business.get(owner=user)

    return {
        'status': 'OK',
        'data': {
            'username': user.username,
            'email': user.email,
            'verified': user.is_verified,
            'joined_date': user.join_date.strtime('%d %b %Y')
        }
    }
    
    
@app.post('/token')
async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_form.username, request_form.password)
    return {'access_token': token,
            'token_type': 'bearer'}

@app.get('verification/', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    user = await verify_token(token)
    
    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse(
            'verification.html', 
            {'request': request,
             'username': user.username},
        )
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
    )
        
@post_save(User)
async def create_business(sender: 'Type[User]', instance: User, created:bool, 
    using_db: 'Optional[BaseDBAsyncClient]', updated_fields: List[str]) -> None :
    if created:
        business_obj = await Business.create(
            name=instance.username, 
            owner = instance,
        )
        
        await business_pydentic.from_tortoise_orm(business_obj)
        await send_email([instance.email], instance)

@app.post('/registration')
async def user_registration(user: user_pydenticIn):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = get_hashed_password(user_info['password'])
    user_obj = await User.create(**user_info)
    new_user = await user_pydentic.from_tortoise_orm(user_obj)
    return {
        'status': 'OK',
        'data': f'Hello, {new_user.username}, thanks for your registration,  check your email'
    }

@app.get('/')
def index():
    return {'Message': 'Hello World!'}

register_tortoise(
    app,
    db_url='sqlite://database.sqlite3',
    modules={'models': ['db_models']},
    generate_schemas=True,
    add_exception_handlers=True,
)