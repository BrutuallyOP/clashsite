from app.models import User
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: str) -> User | None:
        return await self.db.get(User, user_id)

    async def get_by_username(self, username: str) -> User | None:
        stmnt = select(User).where(User.username == username)
        result = await self.db.execute(stmnt)
        return result.scalar_one_or_none()

    async def create(self, username: str, hashed_password: str, level: int = 0):
        user = User(username=username, hashed_password=hashed_password, level=level)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_password(self, user_id: str, new_pwd_hash: str) -> None:
        await self.db.execute(
            update(User).where(User.id == user_id).values(hashed_password=new_pwd_hash)
        )
        await self.db.commit()

    async def update_username(self, user_id: str, new_username: str) -> None:
        await self.db.execute(
            update(User).where(User.id == user_id).values(username=new_username)
        )
        await self.db.commit()

    async def update_level(self, user_id: str, new_level: int) -> None:
        await self.db.execute(
            update(User).where(User.id == user_id).values(level=new_level)
        )
        await self.db.commit()

    async def list_all(self):
        users = await self.db.execute(select(User))
        return users.scalars().all()

    async def delete_user(self, user_id: str):
        await self.db.execute(delete(User).where(User.id == user_id))
        await self.db.commit()
