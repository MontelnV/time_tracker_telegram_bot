import sys, logging, asyncio, os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import router
from app.database import async_main, drop_tables

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

async def main():
    # await drop_tables()
    await async_main()

    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try: asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
