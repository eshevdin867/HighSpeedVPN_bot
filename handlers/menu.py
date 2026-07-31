from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.db import get_last_news
from states.support import SupportState


router = Router()


# =====================================
# Последние новости
# =====================================

@router.callback_query(lambda c: c.data == "news")
async def news(callback: CallbackQuery):

    current_news = await get_last_news()

    if current_news:

        await callback.message.answer(
            f"""
📰 Последние новости:

{current_news}
"""
        )

    else:

        await callback.message.answer(
            "📰 Новостей пока нет."
        )


    await callback.answer()



# =====================================
# Связаться с разработчиком
# =====================================

@router.callback_query(lambda c: c.data == "support")
async def support(
        callback: CallbackQuery,
        state: FSMContext
):

    await state.set_state(
        SupportState.waiting_message
    )


    await callback.message.answer(
        """
💬 Опишите вашу проблему.

Можно отправить:
• текст;
• фото;
• документ;
• видео;
• голосовое сообщение.

Сообщение будет отправлено разработчику.
"""
    )


    await callback.answer()
