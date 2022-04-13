from fastapi import APIRouter, status
from app.schemas import users
from app.crud import Users

router = APIRouter(prefix="/users")


@router.post("/", response_model=users.UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: users.UserCreate):
    return await Users.create(username=user.username, password=user.password, email=user.email)


@router.get("/", response_model=list[users.UserPublic])
async def read_users():
    return await Users.get_many()
