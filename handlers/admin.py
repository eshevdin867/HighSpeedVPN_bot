from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID

from database.db import (
    get_all_users,
    add_news,
    get_last_news
)

from states.admin import AdminState
from keyboards.admin import admin_menu

from services.amnezia_service import amnezia

router = Router()



@router.message(Command("admin"))
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return


    await message.answer(
        "🛠 Админ-панель",
        reply_markup=admin_menu()
    )



# -------------------------
# Количество пользователей
# -------------------------

@router.callback_query(
    lambda c: c.data == "admin_users"
)
async def admin_users(
        callback: CallbackQuery
):

    users = await get_all_users()

    await callback.message.answer(
        f"👥 Пользователей: {len(users)}"
    )

    await callback.answer()



# -------------------------
# Создание новости
# -------------------------

@router.callback_query(
    lambda c: c.data == "admin_news"
)
async def create_news(
        callback: CallbackQuery,
        state: FSMContext
):

    await state.set_state(
        AdminState.waiting_news
    )


    await callback.message.answer(
        "📢 Введите текст новости:"
    )


    await callback.answer()



@router.message(
    AdminState.waiting_news
)
async def save_news(
        message: Message,
        state: FSMContext
):

    if message.from_user.id != ADMIN_ID:
        return


    await add_news(
        message.text
    )


    await message.answer(
        "✅ Новость сохранена."
    )


    await state.clear()



# -------------------------
# Просмотр последней новости
# -------------------------

@router.callback_query(
    lambda c: c.data == "admin_last_news"
)
async def last_news(
        callback: CallbackQuery
):

    news = await get_last_news()


    if not news:

        await callback.message.answer(
            "📰 Новостей пока нет."
        )

    else:

        await callback.message.answer(
            f"📰 Последняя новость:\n\n{news}"
        )


    await callback.answer()

# =====================================
# Публикация последней новости
# =====================================

@router.callback_query(
    lambda c: c.data == "admin_publish_news"
)
async def publish_news(
        callback: CallbackQuery
):

    if callback.from_user.id != ADMIN_ID:
        return


    news = await get_last_news()


    if not news:

        await callback.message.answer(
            "❌ Нет новости для публикации."
        )

        await callback.answer()
        return


    users = await get_all_users()


    success = 0
    failed = 0


    for user_id in users:

        try:

            await callback.bot.send_message(
                user_id,
                f"""
📰 Новости VPN-сервиса:

{news}
"""
            )

            success += 1


        except Exception:

            failed += 1



    await callback.message.answer(
        f"""
📢 Новость опубликована.

✅ Доставлено: {success}
❌ Ошибок: {failed}
"""
    )


    await callback.answer()

# =====================================
# Проверка работоспобности API
# =====================================

@router.message(Command("api"))
async def api_test(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    try:

        clients = await amnezia.get_clients()

        await message.answer(
            f"✅ API работает.\n\nНайдено клиентов: {len(clients)}"
        )

    except Exception as e:

        await message.answer(
            f"❌ Ошибка API:\n\n{e}"
        )
