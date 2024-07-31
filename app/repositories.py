from app.database import new_session, TimetableORM
from sqlalchemy import select, update
from datetime import datetime, timezone, timedelta

class UserRepository:

    # метод для добавления стартового времени
    @classmethod
    async def add_start_time(cls, user_id: int, username: str, breakfast: bool):
        async with new_session() as session:
            check = breakfast
            current_time = datetime.now()
            timetable_entry = TimetableORM(user_id=user_id, timestamp_in=current_time, breakfast = check, username=username)
            session.add(timetable_entry)
            await session.commit()

    # метод для добавления в запись времени окончания работы с уже существующим стартовым временем
    async def add_end_time(cls, user_id: int, breakfast: bool):
        async with new_session() as session:
            current_time = datetime.now()
            check = breakfast
            existing_entry = await session.execute(
                select(TimetableORM).where(
                    TimetableORM.breakfast == check,
                    TimetableORM.user_id == user_id,
                    TimetableORM.timestamp_out == None
                )
            )
            existing_entry = existing_entry.scalars().first()
            if existing_entry:
                await session.execute(
                    update(TimetableORM).where(TimetableORM.user_id == user_id,  TimetableORM.timestamp_out == None, TimetableORM.breakfast == check).values(
                            timestamp_out=current_time)
                )
                await session.commit()
            else:
                print("Произошла неизвестная ошибка")

    # получение информации о работнике на текущую дату
    @classmethod
    async def get_user_info_by_date(cls, date: datetime):
        current_date = date.date()
        async with new_session() as session:
            q = select(TimetableORM).where(
                TimetableORM.timestamp_in >= current_date,
                TimetableORM.timestamp_in < current_date + timedelta(days=1)
            )
            result = await session.execute(q)
            user = result.scalars().all()
            return user

    # проверка для контроля повторного начала смены (одну смену можно закрыть только один раз за день)
    @classmethod
    async def check_user_info(cls, user_id: int):
        current_date = datetime.now().date()
        async with new_session() as session:
            q = select(TimetableORM).where(
                TimetableORM.user_id == user_id,
                TimetableORM.timestamp_in >= current_date,
                TimetableORM.timestamp_in < current_date + timedelta(days=1)
            )
            result = await session.execute(q)
            user = result.scalars().first()
            if user: return False
            else: return True

    # проверка для контроля начала работы (предотвращает повторное начало рабочей смены)
    @classmethod
    async def check_start_time(cls, user_id: int, breakfast: bool):
        async with new_session() as session:
            q = select(TimetableORM).where(
                TimetableORM.user_id == user_id,
                TimetableORM.breakfast == breakfast,
                TimetableORM.timestamp_out == None
            )
            result = await session.execute(q)
            user = result.scalars().first()
            if user: return True
            else: return False