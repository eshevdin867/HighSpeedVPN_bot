from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu():

    builder = InlineKeyboardBuilder()

    #builder.button(
    #        text="🛒 Купить VPN",
    #        callback_data="buy_vpn"
    #)

    builder.button(
        text="📢 Последние новости",
        callback_data="news"
    )

    builder.button(
        text="💬 Связаться с разработчиком",
        callback_data="support"
    )

    builder.adjust(1)

    return builder.as_markup()
