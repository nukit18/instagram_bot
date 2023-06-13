from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel")
        ]
    ]
)