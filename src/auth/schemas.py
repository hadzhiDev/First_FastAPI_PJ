from pydantic import BaseModel, ConfigDict, EmailStr
from fastapi_users import schemas, models


class UserRead(schemas.BaseUser[int]):
    username: str
    role_id: int
    id: int
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    role_id: int
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    pass