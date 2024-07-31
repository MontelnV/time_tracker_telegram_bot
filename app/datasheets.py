from sqlalchemy import select
from openpyxl import Workbook
from database import new_session, TimetableORM

async def export_user_data_to_xlsx():
    async with new_session() as session:
        user_ids_query = select(TimetableORM.user_id).distinct()
        user_ids_result = await session.execute(user_ids_query)
        user_ids = user_ids_result.scalars().all()

        wb = Workbook()
        ws = wb.active
        ws.append(["Дата", "Работник", "Время прихода", "Время ухода", "Перерыв"])

        previous_date = None

        for user_id in user_ids:
            TimetableORM_query = select(TimetableORM).where(TimetableORM.user_id == user_id)
            TimetableORM_result = await session.execute(TimetableORM_query)
            TimetableORM_entries = TimetableORM_result.scalars().all()

            for entry in TimetableORM_entries:
                current_date = entry.timestamp_in.strftime("%d-%m")
                time_in = entry.timestamp_in.strftime("%H:%M")
                time_out = entry.timestamp_out.strftime("%H:%M")

                row_data = []
                if current_date != previous_date:
                    row_data.append(current_date)
                    previous_date = current_date
                else:
                    row_data.append(None)

                row_data.extend([user_id, time_in, time_out])

                if entry.breakfast:
                    row_data.append("+")
                else:
                    row_data.append("")

                ws.append(row_data)

                user_id = None

        wb.save("TimetableORM.xlsx")

import asyncio
asyncio.run(export_user_data_to_xlsx())