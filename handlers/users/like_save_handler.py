import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from insta_bot.auth import get_logins
from insta_bot.function_like_save import like_save_function
from keyboards.inline.cancel_keyboard import cancel_keyboard
from keyboards.inline.confirm_keyboard import confirm_keyboard
from keyboards.inline.logins_keyboard import logins_keyboard
from loader import dp, bot


@dp.callback_query_handler(text="cancel", state=["input_hashtag_like_save", "login_like_save", "finish_like_save"])
async def cancel_like_save(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    await bot.send_message(user_id, f"Вы успешно отменили ввод.")
    await state.reset_data()
    await state.finish()


@dp.message_handler(text="Лайк, сохранение")
async def get_hashtag_like_save(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await message.answer(f"Привет, извини, но ты не можешь использовать меня.")
        return
    await message.answer("Введите хэштег:", reply_markup=cancel_keyboard)
    await state.set_state("input_hashtag_like_save")


@dp.message_handler(state="input_hashtag_like_save")
async def choice_login_like_save(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await message.answer(f"Привет, извини, но ты не можешь использовать меня.")
        return
    hashtag = message.text
    await state.update_data(hashtag=hashtag)
    keyboard = await logins_keyboard()
    await message.answer("Хорошо, теперь выберите аккаунт:", reply_markup=keyboard)
    await state.set_state("login_like_save")


@dp.callback_query_handler(state="login_like_save")
async def input_group_like_save(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    login = call.data
    await state.update_data(login=login)
    await bot.send_message(user_id, "Проверьте, пожалуйста, правильность введенных данных:", reply_markup=confirm_keyboard)
    await state.set_state("finish_like_save")


@dp.callback_query_handler(text="confirm", state="finish_like_save")
async def finish_like_save(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    data = await state.get_data()
    hashtag = data.get("hashtag")
    login = data.get("login")
    await bot.send_message(user_id,
                           f"Начинаю выполнять функцию: *Лайк, сохранение*,\nиспользуя аккаунт *{login}*.\nПришлю отчет, как закончу.",
                           parse_mode="Markdown")
    logins = await get_logins()
    asyncio.create_task(like_save_function_try_except(user_id, login, logins[login], hashtag))
    await state.reset_data()
    await state.finish()


async def like_save_function_try_except(user_id, login, password, hashtag):
    try:
        await like_save_function(login, password, hashtag, user_id)
    except:
        await bot.send_message(user_id, f"Не удалось выполнить функцию.\n*Лайк, сохранение*", parse_mode="Markdown")
        return