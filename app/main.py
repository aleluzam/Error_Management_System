from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_tables
from database import engine
from endpoints import routes, routes_login


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting api")
    create_tables()
    yield
    engine.dispose()

       
app = FastAPI(lifespan=lifespan)
app.include_router(routes)
app.include_router(routes_login)


@app.get("/")
def route():
    return {"message": "Hello Word"}


    