from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def report1(user_id):
    return InlineKeyboardMarkup(row_width=4).add(
        InlineKeyboardButton("🔞", callback_data=f"report_{user_id}_18+"),
        InlineKeyboardButton("💰", callback_data=f"report_{user_id}_sell"),
        InlineKeyboardButton("📰", callback_data=f"report_{user_id}_ads"),
        InlineKeyboardButton("🤬", callback_data=f"report_{user_id}_abuse"),
        InlineKeyboardButton("←", callback_data=f"return_report_menu_{user_id}")
    )

def report2(user_id):
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🥰", callback_data=f"send_like_to_{user_id}"),
        InlineKeyboardButton("🤮", callback_data=f"send_dislike_to_{user_id}"),
        InlineKeyboardButton("Пожаловаться →", callback_data=f"open_report_menu_{user_id}")
    )