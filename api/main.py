from fastapi import FastAPI

from .router import articles, users, auth
from .db import database

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(articles.router)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
