from typing import Annotated
from odmantic import ObjectId
from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict, Field, field_validator, SecretStr


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    display_name: str = ""


class UserCreate(UserBase):
    email: EmailStr
    password: Annotated[str | None, StringConstraints(min_length=8, max_length=64)] = None


class UserUpdate(UserBase):
    original: Annotated[str | None, StringConstraints(min_length=8, max_length=64)] = None
    password: Annotated[str | None, StringConstraints(min_length=8, max_length=64)] = None


class UserInDBBase(UserBase):
    id: ObjectId | None = None
    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    hashed_password: bool = Field(default=False, alias="password")
    model_config = ConfigDict(populate_by_name=True)
    @field_validator("hashed_password", mode="before")
    def evaluate_hashed_password(cls, hashed_password):
        if hashed_password:
            return True
        return False


class UserInDB(UserInDBBase):
    hashed_password: SecretStr | None = None