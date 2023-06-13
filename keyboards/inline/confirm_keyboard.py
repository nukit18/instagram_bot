from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Все верно ✅", callback_data="confirm")
        ],
        [
            InlineKeyboardButton(text="Отменить ❌", callback_data="cancel")
        ]
    ]
)