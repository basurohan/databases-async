from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from passlib.hash import pbkdf2_sha256

from api import schemas
from api.db import database
from api.token import create_access_token

router = APIRouter(
    prefix='/login',
    tags=['Auth']
)


@router.post('/', status_code=status.HTTP_200_OK)
async def login(login_details: OAuth2PasswordRequestForm = Depends()):
    query = '''
    SELECT * FROM users
    WHERE username=:username
    '''
    values = {'username': login_details.username}
    user_details = await database.fetch_one(query=query, values=values)
    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if not pbkdf2_sha256.verify(login_details.password, user_details.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid login')

    access_token = create_access_token(data={"sub": user_details.username})
    return {"access_token": access_token, "token_type": "bearer"}
