from aiogram import Router
from aiogram.types import CallbackQuery

from config import TARIFFS
from keyboards.purchase import tariffs_keyboard
from services.amnezia_service import amnezia
from database.subscription_repository import subscription_repo

router = Router()


@router.callback_query(lambda c: c.data == "buy_vpn")
async def buy_vpn(callback: CallbackQuery):

    await callback.message.answer(
        "🛒 Выберите подходящий тариф:",
        reply_markup=tariffs_keyboard()
    )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("buy:"))
async def create_vpn(callback: CallbackQuery):

    tariff_id = callback.data.split(":")[1]

    tariff = TARIFFS[tariff_id]

    await callback.message.edit_text(
        "⏳ Создаем VPN..."
    )

    try:

        client = await amnezia.create_client(
            days=tariff["days"]
        )

        await subscription_repo.add(
            telegram_id=callback.from_user.id,
            vpn_client_id=client.id,
            client_name=client.client_name,
            tariff=tariff_id,
            days=tariff["days"],
            expires_at=client.expires_at or 0,
        )

        text = f"""
✅ VPN успешно создан!

📅 Тариф:
{tariff["title"]}

👤 Пользователь:
{client.client_name}

Теперь отправляю конфигурацию...
"""

        await callback.message.answer(text)

        await callback.message.answer_document(
            document=("config.conf", client.config.encode("utf-8")),
            caption="📎 Ваш VPN-конфиг."
        )

    except Exception as e:

        await callback.message.answer(
            f"❌ Ошибка создания VPN:\n\n{e}"
        )

    await callback.answer()
