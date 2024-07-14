from fastapi import Depends, HTTPException, Path, Body
from src.services.user import UserService
from src.repositories.user import UserRepository
from src.schemas.user import User, UserCreate
from src.api.dependencies.database import get_mongodb_repo
from typing import Union

def get_user_service(
        user_repository = Depends(get_mongodb_repo(UserRepository))
) -> UserService:
    return UserService(user_repository)

def get_user(
        user_service: UserService = Depends(get_user_service)
) -> Union[User, None]:
    try:
        print(f"[DEBUG] get_user_service: {user_service}")
        user = user_service.get()
        print(f"[DEBUG] user: {user}")
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_user(
        user_id: str = Path(...),
        user_update: UserCreate = Body(...),
        user_service: UserService = Depends(get_user_service)
) -> Union[User, None]:
    try:
        updated_user = user_service.update(user_id, user_update.model_dump())
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
