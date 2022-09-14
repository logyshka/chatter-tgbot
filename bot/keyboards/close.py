from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

close = InlineKeyboardMarkup().add(
    InlineKeyboardButton("✖", callback_data="close")
)

close_reply = InlineKeyboardMarkup().add(
    InlineKeyboardButton("✖", callback_data="close_reply")
)