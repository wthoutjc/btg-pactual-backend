from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK
from src.schemas.user import User
from src.api.dependencies.dependency_user import get_user, update_user

user_router = APIRouter()

@user_router.get(
    "/",
    status_code=HTTP_200_OK,
    response_description="get user",
    response_model=User
)
def get(
    user: User = Depends(get_user)
):
    return user

@user_router.put(
    "/{user_id}",
    status_code=HTTP_200_OK,
    response_description="update user",
    response_model=User
)
def update_user(
    user: User = Depends(update_user)
):
    return user