from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Лайк, репост, сохранение")#1
        ],
        [
            KeyboardButton(text="Лайк, репост")#2
        ],
        [
            KeyboardButton(text="Лайк, сохранение")#3
        ],
        [
            KeyboardButton(text="Репост")#4
        ],
        [
            KeyboardButton(text="Репост, сохранение")#5
        ],
        [
            KeyboardButton(text="Подписка на аккаунты ✅")
        ],
        [
            KeyboardButton(text="Отменить ❌")
        ]
    ],
    resize_keyboard=True
)
