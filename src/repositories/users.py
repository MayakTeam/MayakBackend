from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel

class UserRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_username(self, username: str) -> UserModel | None:
        return await self.session.scalar(
            select(UserModel).where(UserModel.username == username)
        )
    
    # Возможно это стоит вынести в функционал абстрактного класса, т.к. это будет повторяться из раза в раз
    async def create(self, user: UserModel) -> UserModel:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user) # Получаем id
        return user
    
