import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from insta_bot.auth import get_logins
from insta_bot.function_subscribe import subscribe_function
from keyboards.inline.cancel_keyboard import cancel_keyboard
from keyboards.inline.logins_keyboard import logins_keyboard
from loader import dp, bot


@dp.callback_query_handler(text="cancel", state=["input_hashtag_sub", "finish_sub"])
async def cancel_sub(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    await bot.send_message(user_id, f"Вы успешно отменили ввод.")
    await state.reset_data()
    await state.finish()


@dp.message_handler(text="Подписка на аккаунты ✅")
async def get_hashtag_sub(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await message.answer(f"Привет, извини, но ты не можешь использовать меня.")
        return
    await message.answer("Введите хэштег:", reply_markup=cancel_keyboard)
    await state.set_state("input_hashtag_sub")


@dp.message_handler(state="input_hashtag_sub")
async def choice_login_sub(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await message.answer(f"Привет, извини, но ты не можешь использовать меня.")
        return
    hashtag = message.text
    await state.update_data(hashtag=hashtag)
    keyboard = await logins_keyboard()
    await message.answer("Хорошо, теперь выберите аккаунт:", reply_markup=keyboard)
    await state.set_state("finish_sub")


@dp.callback_query_handler(state="finish_sub")
async def finish_sub(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    data = await state.get_data()
    hashtag = data.get("hashtag")
    login = call.data
    await bot.send_message(user_id, f"Начинаю подписываться на аккаунты, используя аккаунт *{login}*.\nКаждый час буду присылать отчёт...",
                           parse_mode="Markdown")
    logins = await get_logins()
    asyncio.create_task(sub_function_try_except(user_id, login, logins[login], hashtag))
    await state.reset_data()
    await state.finish()


async def sub_function_try_except(user_id, login, password, hashtag):
    try:
        await subscribe_function(login, password, hashtag, user_id)
    except:
        await bot.send_message(user_id, f"Не удалось подписаться на аккаунты")
        return