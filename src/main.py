from binascii import Error
from fastapi import FastAPI

from src.db import Base, engine
from src.app_auth.auth_router import auth_router
from src.client.client_router import client_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(client_router)

@app.get("/init")
async def create_db():
    
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Error as e:
            print(e)
        await conn.run_sync(Base.metadata.create_all)