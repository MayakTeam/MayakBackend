from fastapi import APIRouter

from src.database import Base, engine
from src import models

developer_router = APIRouter(tags=["Developer"])

@developer_router.get("/destroy_db", summary="Delete the database", description="Drops all tables in the database.")
async def destroy_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    return {"message": "Database destroyed successfully."}


@developer_router.get("/init_db", summary="Initialize the database", description="Creates all tables in the database.")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "Database initialized successfully."}


