from fastapi import APIRouter, HTTPException

from src.authentication import check_authentication
from src.api.dependencies import SessionDep
from src.schemas.users import UserCreateSchema, UserResponseSchema
from src.exceptions import UsernameTakenError
from src.services.users import UserService
from src.repositories.users import UserReposoitory

from sqlalchemy import select

users_router = APIRouter(tags=["Users"])

@users_router.get("/current_user")
async def get_current_user():
    
    return {"message": "Current user information"}

@users_router.post("/users", response_model=UserResponseSchema, status_code=201)
async def create_user(user: UserCreateSchema, session: SessionDep):
    try:
        return await UserService(UserReposoitory(session)).create_user(user)
    except UsernameTakenError:
        raise HTTPException(status_code=409, detail="Логин уже занят")