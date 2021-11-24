from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import Response
from passlib.hash import pbkdf2_sha256

from api import schemas
from api.db import database

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponseDTO)
async def create_user(user: schemas.User):
    hashed_password = pbkdf2_sha256.hash(user.password)
    query = '''
    INSERT INTO users(username, password) 
    VALUES (:username, :password)
    '''
    values = {'username': user.username, 'password': hashed_password}
    last_record_id = await database.execute(query=query, values=values)
    return {**user.dict(), 'id': last_record_id}


@router.get('/', response_model=List[schemas.UserResponseDTO])
async def get_users():
    query = '''
    SELECT * FROM users
    '''
    return await database.fetch_all(query=query)


@router.get('/{user_id}', response_model=schemas.UserResponseDTO)
async def get_user(user_id: int):
    query = '''
    SELECT * FROM users WHERE id = :id
    '''
    values = {'id': user_id}
    row = await database.fetch_one(query=query, values=values)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {user_id} not found')
    return row


@router.put('/{user_id}', response_model=schemas.UserResponseDTO)
async def update_user(user_id: int, user: schemas.User):
    query = '''
    UPDATE users
    SET username=:username, password=:password
    WHERE id=:id
    '''
    values = {'username': user.username, 'password': user.password, 'id': user_id}
    last_record_id = await database.execute(query=query, values=values)
    if last_record_id == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {user_id} not found')
    return {**user.dict(), 'id': last_record_id}


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(user_id: int):
    query = '''
    DELETE FROM users WHERE id=:id
    '''
    values = {'id': user_id}
    await database.execute(query=query, values=values)
    return Response(status_code=status.HTTP_204_NO_CONTENT)