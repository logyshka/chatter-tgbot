from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

subscription = InlineKeyboardMarkup(row_width=3).add(
    InlineKeyboardButton("😏 1 день", callback_data="buy_sub_day"),
    InlineKeyboardButton("🤤 1 неделя", callback_data="buy_sub_week"),
    InlineKeyboardButton("😎 1 месяц", callback_data="buy_sub_month"),
    InlineKeyboardButton("✖", callback_data="close"))

def buy_subscription(url, bill_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("💰 Оплатить", url=url),
        InlineKeyboardButton("🚫 Отмена", callback_data=f"close_bill_{bill_id}")
    )

