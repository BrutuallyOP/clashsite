from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    username: str = Field(min_length=4, max_length=12)
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(min_length=7, max_length=128)

class UserLogin(UserBase):
    password: str

class UsernameUpdate(BaseModel):
    new_username: str = Field(min_length=4, max_length=12)
    password: str = Field(min_length=7, max_length=128)

class LayoutPublic(BaseModel):
    id: str
    th_level: int
    thumbnail_path: str
    url : str
    note: str | None = None
    model_config = ConfigDict(from_attributes=True)

