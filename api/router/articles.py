from typing import List

from fastapi import APIRouter, HTTPException, Depends

from starlette import status
from starlette.responses import Response

from api import schemas
from api.db import database
from api.token import get_current_user

router = APIRouter(
    prefix='/articles',
    tags=['Articles']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ArticleResponseDTO)
async def create_article(article: schemas.Article):
    query = '''
    INSERT INTO articles(title, description) 
    VALUES (:title, :description)
    '''
    values = {'title': article.title, 'description': article.description}
    last_record_id = await database.execute(query=query, values=values)
    return {**article.dict(), 'id': last_record_id}


@router.get('/', response_model=List[schemas.ArticleResponseDTO])
async def get_articles(current_user: schemas.User = Depends(get_current_user)):
    query = '''
    SELECT * FROM articles
    '''
    return await database.fetch_all(query=query)


@router.get('/{article_id}', response_model=schemas.ArticleResponseDTO)
async def get_article(article_id: int):
    query = '''
    SELECT * FROM articles WHERE id = :id
    '''
    values = {'id': article_id}
    row = await database.fetch_one(query=query, values=values)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id: {article_id} not found')
    return row


@router.put('/{article_id}', response_model=schemas.ArticleResponseDTO)
async def update_article(article_id: int, article: schemas.Article):
    query = '''
    UPDATE articles
    SET title=:title, description=:description
    WHERE id=:id
    '''
    values = {'title': article.title, 'description': article.description, 'id': article_id}
    last_record_id = await database.execute(query=query, values=values)
    if last_record_id == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id: {article_id} not found')
    return {**article.dict(), 'id': last_record_id}


@router.delete('/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int):
    query = '''
    DELETE FROM articles WHERE id=:id
    '''
    values = {'id': article_id}
    await database.execute(query=query, values=values)
    return Response(status_code=status.HTTP_204_NO_CONTENT)