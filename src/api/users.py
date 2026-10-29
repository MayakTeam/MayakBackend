from fastapi import APIRouter, HTTPException

from src.authentication import check_authentication
from src.api.dependencies import SessionDep
from src.schemas.users import UserCreateSchema, UserResponseSchema
from src.models import UserModel
from src.safety import hash_password

from sqlalchemy import select

users_router = APIRouter(tags=["Users"])

@users_router.get("/current_user")
async def get_current_user():
    
    return {"message": "Current user information"}


@users_router.post("/users", response_model=UserResponseSchema, status_code=201)
async def create_user(user: UserCreateSchema, session: SessionDep):
    existing = await session.scalar(
        select(UserModel)
        .where(UserModel.username == user.username)
    )
    if existing:
        raise HTTPException(status_code=409, detail="Логин уже занят")

    hashed = hash_password(user.password)
    db_user = UserModel(
        username=user.username,
        password_hash=hashed,
        role_id=user.role_id
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)   # Получение id из БД
    
    return db_user