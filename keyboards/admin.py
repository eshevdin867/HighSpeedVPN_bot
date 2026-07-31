from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_menu():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="👥 Пользователи",
        callback_data="admin_users"
    )

    builder.button(
        text="📝 Создать новость",
        callback_data="admin_news"
    )

    builder.button(
        text="📢 Опубликовать новость",
        callback_data="admin_publish_news"
    )

    builder.button(
        text="📰 Последняя новость",
        callback_data="admin_last_news"
    )

    builder.adjust(1)

    return builder.as_markup()
