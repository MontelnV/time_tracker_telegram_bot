from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


engine = create_async_engine(
    "sqlite+aiosqlite:///timetable.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class TimetableORM(Base):
    __tablename__ = 'timetable'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    username: Mapped[str]
    timestamp_in: Mapped[datetime | None]
    timestamp_out: Mapped[datetime | None]
    breakfast: Mapped[bool] = mapped_column(default=False)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)