from fastapi import FastAPI
from dotenv import load_dotenv
from lib.db import engine, create_table
from contextlib import asynccontextmanager

from routes import auth

load_dotenv()

@asynccontextmanager
async def lifespan(app = FastAPI):
    yield
    engine.begin()
    create_table()

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def get_home():
    return {'message': 'Hello World'}

app.include_router(auth.router, prefix='/api/auth', tags=['auth'])