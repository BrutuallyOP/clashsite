from app.models import Tracker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TrackerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tracker_id: str) -> Tracker | None:
        return await self.db.get(Tracker, tracker_id)

    async def create(self, layout_id: str, user_id: str):
        tracker = Tracker(layout_id=layout_id, user_id=user_id)
        self.db.add(tracker)
        await self.db.commit()
        await self.db.refresh(tracker)
        return tracker

    async def fetch_consumers(self, layout_id: str):
        consumers = await self.db.execute(
            select(Tracker).where(Tracker.layout_id == layout_id)
        )
        return consumers.scalars().all()

    async def fetch_downloads(self, user_id: str):
        downloads = await self.db.execute(
            select(Tracker).where(Tracker.user_id == user_id)
        )
        return downloads.scalars().all()
