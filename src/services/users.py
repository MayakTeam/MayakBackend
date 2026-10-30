from src.models import UserModel
from src.repositories.users import UserRepository
from src.schemas.users import UserCreateSchema
from src.exceptions import UsernameTakenError
from src.safety import hash_password


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    async def create_user(self, data: UserCreateSchema) -> UserModel:
        # Проверяем, есть ли пользователь с таким именем
        if await self.repo.get_by_username(data.username):
            raise UsernameTakenError()
        # Хэшируем пароль
        hashed = hash_password(data.password)
        # Сохраняем
        return await self.repo.create(UserModel(
            username = data.username,
            password_hash = hashed,
            role_id = data.role_id
        ))