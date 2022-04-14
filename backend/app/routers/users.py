from fastapi import APIRouter, status, Depends
from app.schemas import users
from app.crud import Users
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/users")


@router.post("/", response_model=users.UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: users.UserCreate):
    return await Users.create(username=user.username, password=user.password, email=user.email)


@router.get("/", response_model=list[users.UserPublic])
async def read_users():
    return await Users.get_many()


@router.get("/me", response_model=users.UserPrivate)
async def read_user_me(user: users.User = Depends(get_current_active_user)):
    return user
