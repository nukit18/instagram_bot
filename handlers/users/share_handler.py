import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from insta_bot.auth import get_logins
from insta_bot.function_share import share_function
from keyboards.inline.cancel_keyboard import cancel_keyboard
from keyboards.inline.confirm_keyboard import confirm_keyboard
from keyboards.inline.logins_keyboard import logins_keyboard
from loader import dp, bot


@dp.callback_query_handler(text="cancel", state=["input_hashtag_share", "login_share", "group_share", "finish_share"])
async def cancel_share(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    await bot.send_message(user_id, f"Вы успешно отменили ввод.")
    await state.reset_data()
    await state.finish()


@dp.message_handler(text="Репост")
async def get_hashtag_share(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await message.answer(f"Привет, извини, но ты не можешь использовать меня.")
        return
    await message.answer("Введите хэштег:", reply_markup=cancel_keyboard)
    await state.set_state("input_hashtag_share")


@dp.message_handler(state="input_hashtag_share")
async def choice_login_share(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await message.answer(f"Привет, извини, но ты не можешь использовать меня.")
        return
    hashtag = message.text
    await state.update_data(hashtag=hashtag)
    keyboard = await logins_keyboard()
    await message.answer("Хорошо, теперь выберите аккаунт:", reply_markup=keyboard)
    await state.set_state("login_share")


@dp.callback_query_handler(state="login_share")
async def login_share(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    login = call.data
    await state.update_data(login=login)
    await bot.send_message(user_id, "А теперь введите название беседы, в которую нужно будет отправлять репост:\n"
                                    "Обязательно нужно ввести название группы правильно!")
    await state.set_state("group_share")


@dp.message_handler(state="group_share")
async def input_group_share(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    group_name = message.text
    await state.update_data(group_name=group_name)
    await message.answer("Проверьте, пожалуйста, правильность введенных данных:", reply_markup=confirm_keyboard)
    await state.set_state("finish_share")


@dp.callback_query_handler(text="confirm", state="finish_share")
async def finish_share(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    if user_id not in ADMINS:
        await bot.send_message(user_id, f"Привет, извини, но ты не можешь использовать меня.")
        return
    data = await state.get_data()
    hashtag = data.get("hashtag")
    login = data.get("login")
    group_name = data.get("group_name")
    await bot.send_message(user_id,
                           f"Начинаю выполнять функцию: *Репост*,\nиспользуя аккаунт *{login}*.\nПришлю отчет, как закончу.",
                           parse_mode="Markdown")
    logins = await get_logins()
    asyncio.create_task(share_function_try_except(user_id, login, logins[login], hashtag, group_name))
    await state.reset_data()
    await state.finish()


async def share_function_try_except(user_id, login, password, hashtag, group_name):
    try:
        await share_function(login, password, hashtag, group_name, user_id)
    except:
        await bot.send_message(user_id, f"Не удалось выполнить функцию.\n*Репост*", parse_mode="Markdown")
        return