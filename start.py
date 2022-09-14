import asyncio

from bot import handlers
from loader import dp, executor, BotCommand

async def set_commands(dispatcher):
    await dispatcher.bot.set_my_commands([
        BotCommand("/start", "Запустить бота"),
        BotCommand("/find", "Найти собеседника"),
        BotCommand("/next", "Новый собеседник"),
        BotCommand("/stop", "Завершить диалог"),
        BotCommand("/rules", "Получить правила")
    ])

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=set_commands)