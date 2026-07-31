from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TARIFFS


def tariffs_keyboard() -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    for tariff_id, tariff in TARIFFS.items():
        builder.button(
            text=f"{tariff['title']} • {tariff['price']} ₽",
            callback_data=f"buy:{tariff_id}"
        )

    builder.adjust(1)

    return builder.as_markup()
