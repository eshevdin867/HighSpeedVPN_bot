from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from states.support import SupportState
from database.db import (
    save_support_message,
    get_user_by_admin_message,
)

router = Router()


# ======================================================
# Пользователь пишет разработчику
# ======================================================

@router.message(SupportState.waiting_message)
async def support_message(message: Message, state: FSMContext):

    # Отправляем карточку пользователя администратору
    user_info = (
        "📨 Новое обращение\n\n"
        f"👤 Имя: {message.from_user.full_name}\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"📎 Username: @{message.from_user.username}"
    )

    await message.bot.send_message(
        ADMIN_ID,
        user_info
    )


    # Копируем оригинальное сообщение пользователя
    copied_message = await message.copy_to(
        ADMIN_ID
    )


    # Запоминаем связь:
    # сообщение админа -> пользователь
    await save_support_message(
        admin_message_id=copied_message.message_id,
        user_id=message.from_user.id
    )


    await message.answer(
        "✅ Ваше сообщение отправлено разработчику.\n\n"
        "Мы ответим вам в ближайшее время."
    )


    await state.clear()



# ======================================================
# Ответ администратора пользователю
# ======================================================

@router.message(F.reply_to_message)
async def admin_reply(message: Message):

    # Только администратор
    if message.from_user.id != ADMIN_ID:
        return


    # Получаем ID сообщения,
    # на которое отвечает администратор
    replied_message_id = (
        message.reply_to_message.message_id
    )


    # Ищем пользователя
    user_id = await get_user_by_admin_message(
        replied_message_id
    )


    if not user_id:
        await message.reply(
            "❌ Не удалось найти пользователя."
        )
        return


    try:

        # Отправляем копию ответа пользователю
        await message.copy_to(
            user_id
        )


        await message.reply(
            "✅ Ответ отправлен пользователю."
        )


    except Exception:

        await message.reply(
            "❌ Не удалось отправить сообщение."
        )
