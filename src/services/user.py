from src.repositories.user import UserRepository
from src.models.user import User
from typing import Union

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get(self) -> Union[User, None]:
        return self.user_repository.get()

    def update(self, user_id: str, user_update: User) -> Union[User, None]:
        return self.user_repository.update(user_id, user_update)