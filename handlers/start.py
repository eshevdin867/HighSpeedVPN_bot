from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.db import (
    user_exists,
    add_user,
    get_last_news
)

from keyboards.menu import main_menu


router = Router()


@router.message(CommandStart())
async def start(message: Message):

    # Проверяем, есть ли пользователь в базе
    if not await user_exists(message.from_user.id):

        await add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )


    # Получаем последнюю новость
    news = await get_last_news()


    text = f"""
👋 Добро пожаловать в HighSpeedVPN!

Данный бот создан специально для клиентов HighSpeedVPN.

Через этот бот вы будете получать важные уведомления, информацию о технических работах и другие новости сервиса.

Если у вас возникнут вопросы или потребуется помощь, вы можете обратиться к разработчику через раздел «💬 Связаться с разработчиком».

В ближайшее время в боте появятся новые возможности:
• подключение новых пользователей;
• управление подпиской;
• уведомления о необходимости оплаты;
• дополнительные функции для удобного использования сервиса.

Спасибо, что выбираете HighSpeedVPN! 🚀
"""


    # Если есть новости — добавляем их
    if news:

        text += f"""

📰 Последние новости:

{news}"""


    await message.answer(
        text,
        reply_markup=main_menu()
    )
