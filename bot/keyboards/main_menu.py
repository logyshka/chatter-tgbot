from aiogram.types import ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(row_width=2,
                                resize_keyboard=True).add(
    "👩🏼 Поиск Ж", "👨🏼 Поиск М",
    "🔍 Поиск собеседника").add(
    "👤 Личный кабинет", "💎 Подписка",
    "📃 Правила бота")

close_dialog = ReplyKeyboardMarkup(row_width=1,
                                   resize_keyboard=True).add(
    "♻ Новый собеседник",
    "🚫 Завершить диалог"
)
close_search = ReplyKeyboardMarkup(row_width=1,
                                   resize_keyboard=True).add(
    "🚫 Завершить поиск"
)

