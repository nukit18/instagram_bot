from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from insta_bot.auth import get_logins


async def logins_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    logins = await get_logins()
    for login in logins:
        keyboard.insert(InlineKeyboardButton(text=login, callback_data=login))
    return keyboard