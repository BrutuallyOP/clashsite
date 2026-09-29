from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, HttpUrl


class UserBase(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(min_length=7, max_length=128)


class UserLogin(UserBase):
    password: str = Field(min_length=7, max_length=128)


class UsernameUpdate(BaseModel):
    new_username: str = Field(min_length=4, max_length=16)
    password: str = Field(min_length=7, max_length=128)


class PasswordUpdate(BaseModel):
    current_password: str = Field(min_length=7, max_length=128)
    new_password: str = Field(min_length=7, max_length=128)


class UserPublic(UserBase):
    id: str


class LayoutPublic(BaseModel):
    id: str
    th_level: int
    thumbnail_path: str
    url: HttpUrl
    note: str | None = None
    model_config = ConfigDict(from_attributes=True)


class LayoutCreate(BaseModel):
    th_level: int = Field(ge=2)
    note: str | None = Field(default=None, max_length=512)
    min_level: int = Field(default=0, ge=0)
    url: HttpUrl


class UserAdminView(UserBase):
    id: str
    level: int
    created_at: datetime


class UserLevelUpdate(BaseModel):
    level: int = Field(ge=0)


class LayoutAdminView(LayoutPublic):
    min_level: int
    uploader: str


class LayoutUpdate(BaseModel):
    th_level: int | None = Field(default=None, ge=2)
    min_level: int | None = Field(default=None, ge=0)
    note: str | None = Field(default=None, max_length=512)
    # url: HttpUrl | None = None
