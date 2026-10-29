from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    role_id: int = Field(default=1, ge=1)
    
class UserResponseSchema(BaseModel):
    id: int
    username: str
    role_id: int
    default_workshop_id: Optional[int]
    created_at: datetime
    last_login_at: Optional[datetime]

class GetUserByIdSchema(BaseModel):
    id: int