from aiogram import executor

from insta_bot.auth import get_path
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    print("Создаю путь к файлам")
    get_path()
    print("Готово")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
