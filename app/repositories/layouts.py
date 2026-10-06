from app.models import Layout
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class LayoutRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, layout_id: str) -> Layout | None:
        return await self.db.get(Layout, layout_id)

    async def create(
        self,
        *,
        th_level: int,
        note: str | None,
        min_level: int,
        url: str,
        uploader: str,
        thumbnail_path: str
    ) -> Layout:
        layout = Layout(
            th_level=th_level,
            note=note,
            min_level=min_level,
            url=url,
            uploader=uploader,
            thumbnail_path=thumbnail_path,
        )
        self.db.add(layout)
        await self.db.commit()
        await self.db.refresh(layout)
        return layout

    async def update_layout(self, layout_id: str, **fields) -> None:
        if not fields:
            return

        await self.db.execute(
            update(Layout).where(Layout.id == layout_id).values(**fields)
        )
        await self.db.commit()

    async def fetch_layouts(self, user_level: int):
        layouts = await self.db.execute(
            select(Layout).where(Layout.min_level <= user_level)
        )
        return layouts.scalars().all()

    async def fetch_uploads(self, user_id: str):
        layouts = await self.db.execute(
            select(Layout).where(Layout.uploader == user_id)
        )
        return layouts.scalars().all()

    async def delete_layout(self, layout_id: str):
        await self.db.execute(delete(Layout).where(Layout.id == layout_id))
        await self.db.commit()
