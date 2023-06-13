import asyncio

from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from data.config import ADMINS
from insta_bot.function_all import close_browser_all
from insta_bot.function_like_save import close_browser_like_save
from insta_bot.function_like_share import close_browser_like_share
from insta_bot.function_share import close_browser_share
from insta_bot.function_share_save import close_browser_share_save
from insta_bot.function_subscribe import close_browser_sub
from keyboards.default.menu_keyboard import menu
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await message.answer(f"Привет, извини, но ты не можешь использовать меня.")
        return
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я - ваш персональный бот для работы с инстаграммом! Приступим?",
        reply_markup=menu)


@dp.message_handler(text="Отменить ❌")
async def cancel_all(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await message.answer(f"Привет, извини, но ты не можешь использовать меня.")
        return
    all_close = []
    all_close.append(close_browser_all())
    all_close.append(close_browser_like_save())
    all_close.append(close_browser_like_share())
    all_close.append(close_browser_share())
    all_close.append(close_browser_share_save())
    all_close.append(close_browser_sub())
    flag = False
    for close in all_close:
        try:
            await close
        except:
            continue
        await message.answer(f"Вы отменили выполнение программы! Дождитесь сообщения о завершении работы!\n Примерное время ожидания 2 минуты")
        flag = True
    if not flag:
        await message.answer(f"Нет программ в работе!")
        return
