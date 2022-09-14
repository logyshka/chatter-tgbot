import datetime
import re
from loader import dp, Message, CallbackQuery, User, ConversationStatus, UserStatus, ContentTypes, IsUnbanned, \
    Conversation, rules_link
from bot.keyboards import main_menu, close_dialog, close_search, close, report1, report2


@dp.message_handler(lambda message: IsUnbanned(message)(), commands=["link"])
async def LINK(message: Message):
    user = User(message.from_user.id)
    if user.status == UserStatus.BUSY:
        if Conversation(user.conversation_id).start_time + datetime.timedelta(minutes=2) > datetime.datetime.now():
            await message.answer(
                text="<i>⚠ Ссылку на свой аккаунт можно отправить только спустя <u>2 минуты</u> после начала диалога!</i>")
        else:
            await dp.bot.send_message(chat_id=user.interlocutor,
                                      text=f"<i>👤 Ваш собеседник поделился <a href='https://t.me/{message.from_user.username}'>ссылкой</a> на свой аккаунт!</i>\n\n"
                                           f"<b>https://t.me/{message.from_user.username}</b>")


@dp.message_handler(lambda message: IsUnbanned(message)()
                                    and (message.text == "/find" or message.text == "🔍 Поиск собеседника"),
                    content_types=ContentTypes.TEXT)
async def FIND(message: Message):
    user = User(message.from_user.id)
    if user.status == UserStatus.FREE:
        result = user.start_conversation()
        if result == ConversationStatus.WAITING:
            text = "<i>🔍 Поиск собеседника начат!</i>"
            await message.answer(text=text, reply_markup=close_search)
        else:
            text = "<i>✅ Собеседник успешно найден!</i>\n\n" \
                   "<i>◾ Доступные команды: </i>\n\n" \
                   "<b>➖ /next - следующий собеседник</b>\n" \
                   "<b>➖ /stop - завершить диалог</b>\n" \
                   "<b>➖ /link - поделиться ссылкой на свой аккаунт</b>"
            await dp.bot.send_message(chat_id=user.interlocutor,
                                      text=text,
                                      reply_markup=close_dialog)
            await message.answer(text=text,
                                 reply_markup=close_dialog)


@dp.message_handler(lambda message: IsUnbanned(message)()
                                    and (message.text == "/next" or message.text == "♻ Новый собеседник"),
                    content_types=ContentTypes.TEXT)
async def NEXT(message: Message):
    user = User(message.from_user.id)
    if user.status == UserStatus.BUSY:
        if user.interlocutor:
            text = "<i>😔 Диалог был завершён!</i>\n\n" \
                   "<i>◾ Доступные команды:</i>\n\n" \
                   "<b>➖ /find - начать диалог</b>"
            text2 = "<i>⚠ Вы можете оценить вашего собеседника, используя кнопки внизу, или пожаловаться на него в случае, если он вёл себя некорректно</i>"
            await dp.bot.send_message(chat_id=user.interlocutor,
                                      text=text,
                                      reply_markup=main_menu)
            await dp.bot.send_message(chat_id=user.interlocutor,
                                      text=text2,
                                      reply_markup=report2(user.id))
            await message.answer(text=text,
                                 reply_markup=main_menu)
            await message.answer(text=text2,
                                 reply_markup=report2(user.interlocutor))
            user.end_conversation()
        else:
            await message.answer(text="<i>⚠ Вы не находитесь в диалоге!</i>\n\n"
                                      "<b>⚠ Для завершения поиска используйте команду /stop или <u>кнопку</u></b>",
                                 reply_markup=close_search)

    if user.status == UserStatus.FREE:
        result = user.start_conversation()
        if result == ConversationStatus.WAITING:
            text = "<i>🔍 Поиск собеседника начат!</i>"
            await message.answer(text=text, reply_markup=close_search)
        else:
            text = "<i>✅ Собеседник успешно найден!</i>\n\n" \
                   "<i>◾ Доступные команды: </i>\n\n" \
                   "<b>➖ /next - следующий собеседник</b>\n" \
                   "<b>➖ /stop - завершить диалог</b>\n" \
                   "<b>➖ /link - поделиться ссылкой на свой аккаунт</b>"
            await dp.bot.send_message(chat_id=user.interlocutor,
                                      text=text,
                                      reply_markup=close_dialog)
            await message.answer(text=text,
                                 reply_markup=close_dialog)


@dp.message_handler(lambda message: IsUnbanned(message)()
                                    and (
                                            message.text == "/stop" or message.text == "🚫 Завершить поиск" or message.text == "🚫 Завершить диалог"),
                    content_types=ContentTypes.TEXT)
async def STOP(message: Message):
    user = User(message.from_user.id)
    if user.status == UserStatus.FREE:
        await message.answer(text="<i>⚠ Вы не находитесь в диалоге!</i>")
    else:

        if user.interlocutor:
            text = "<i>😔 Диалог был завершён!</i>\n\n" \
                   "<i>◾ Доступные команды:</i>\n\n" \
                   "<b>➖ /find - начать диалог</b>"
            text2 = "<i>⚠ Вы можете оценить вашего собеседника, используя кнопки внизу, или пожаловаться на него в случае, если он вёл себя некорректно</i>"
            await dp.bot.send_message(chat_id=user.interlocutor,
                                      text=text,
                                      reply_markup=main_menu)
            await dp.bot.send_message(chat_id=user.interlocutor,
                                      text=text2,
                                      reply_markup=report2(user.id))
            await message.answer(text=text,
                                 reply_markup=main_menu)
            await message.answer(text=text2,
                                 reply_markup=report2(user.interlocutor))
        else:
            await message.answer(text="<i>😔 Поиск был завершён!</i>\n\n"
                                      "<i>◾ Доступные команды:</i>\n\n"
                                      "<b>➖ /find - начать диалог</b>",
                                 reply_markup=main_menu)
        user.end_conversation()


@dp.message_handler(lambda message: User(message.from_user.id).status == UserStatus.BUSY and IsUnbanned(message)(),
                    content_types=ContentTypes.ANY)
async def CONVERSATION(message: Message):
    user = User(message.from_user.id)
    if message.content_type != ContentTypes.STICKER:
        if message.text:
            search = re.search('(\w+)://([\w\-\._]+)/(\w+).(\w+)', message.text)
            if not search:
                search = "@" in message.text
        elif message.caption:
            search = re.search('(\w+)://([\w\-\._]+)/(\w+).(\w+)', message.caption)
            if not search:
                search = "@" in message.caption
        else:
            search = False
        if search:
            during = round(user.get_warn(1 / 12) * 60, 2)
            await message.answer(text=f"<i>😔 Диалог был завершён, так как вы были заблокированы!</i>\n\n"
                                      f"<i>🕗 Срок блокировки: <u>{during} минут</u></i>\n\n"
                                      f"<i>🤷‍♂ Причина: <u>попытка отправить ссылку</u></i>")
            await dp.bot.send_message(chat_id=user.interlocutor,
                                      text=f"<i>😔 Диалог был завершён, так как ваш собеседник был заблокирован!</i>\n\n"
                                           f"<i>🕗 Срок блокировки: <u>{during} минут</u></i>\n\n"
                                           f"<i>🤷‍♂ Причина: <u>попытка отправить ссылку</u></i>")
            user.end_conversation()
        else:
            await message.copy_to(chat_id=user.interlocutor)


@dp.message_handler(lambda message: User(message.from_user.id).status == UserStatus.FREE
                                    and IsUnbanned(message)() and (
                                            message.text == "📃 Правила бота" or message.text == "/rules"),
                    content_types=ContentTypes.TEXT)
async def RULES(message: Message):
    await message.answer(
        text=f"<i><u>📃 Правила бота</u> вы можете найти, перейдя по <a href='{rules_link}'>ссылке внизу</a></i>\n\n"
             f"<b>{rules_link}</b>",
        reply_markup=close)


@dp.message_handler(lambda message: not IsUnbanned(message)()
                                    and User(
    message.from_user.id).banned_for < datetime.datetime.now() + datetime.timedelta(days=700),
                    content_types=ContentTypes.TEXT)
async def BAN_DESCRIPTION(message: Message):
    user = User(message.from_user.id)
    if not message.from_user.username:
        text = "<i>⚠ Использование бота будет недоступно вам до тех пор, пока вы не установите себе <u>username</u>!</i>\n\n"
    else:
        text = f"<i>⚠ Использование бота будет недоступно вам до <u>{user.banned_for.replace(microsecond=0)}</u>!</i>\n\n" \
               f"<i>⚠ Во избежании повторной блокировки, соблюдайте <a href='{rules_link}'>правила установленные в боте</a></i>"
    await message.answer(text=text)


@dp.callback_query_handler(lambda call: IsUnbanned(call)() and re.search(r"report_menu_\d+", call.data))
async def REPORT_MENU(call: CallbackQuery):
    if "open" in call.data:
        user_id = call.data.replace("open_report_menu_", "")
        await call.message.edit_text(text="<i>◾ Описание жалоб:</i>\n\n"     
                                          "<b>🔞 | пошлый собеседник</b>\n" 
                                          "<b>💰 | продажа</b>\n"           
                                          "<b>📰 | реклама</b>\n"
                                          "<b>🤬 | оскорбления</b>",
                                     reply_markup=report1(user_id))
    elif "return" in call.data:
        user_id = call.data.replace("return_report_menu_", "")
        text2 = "<i>⚠ Вы можете оценить вашего собеседника, используя кнопки внизу, или пожаловаться на него в случае, если он вёл себя некорректно</i>"
        await call.message.edit_text(text=text2,
                                     reply_markup=report2(user_id))



@dp.callback_query_handler(lambda call: IsUnbanned(call)() and re.search(r"report_\d+_.+$", call.data))
async def REPORT_MENU(call: CallbackQuery):
    method, user_id, reason = call.data.split("_")
    User(user_id).get_report(reason)
    await call.message.answer("<i>✅ Ваша жалоба была принята на рассмотрение!</i>\n"
                              "<i>⚠ Если жалоба обоснована, нарушитель будет наказан!</i>",
                              reply_markup=close)
    await call.message.delete()


@dp.callback_query_handler(lambda call: IsUnbanned(call)() and re.search(r"send_like_to_\d+", call.data))
async def SEND_LIKE(call: CallbackQuery):
    user = User(call.data.replace("send_like_to_", ""))
    user.get_like()
    await call.message.answer("<i>✅ Ваш отзыв был принят</i>",
                              reply_markup=close)
    await call.message.delete()


@dp.callback_query_handler(lambda call: IsUnbanned(call)() and re.search(r"send_dislike_to_\d+", call.data))
async def SEND_DISLIKE(call: CallbackQuery):
    user = User(call.data.replace("send_dislike_to_", ""))
    user.get_dislike()
    await call.message.answer("<i>✅ Ваш отзыв был принят</i>",
                              reply_markup=close)
    await call.message.delete()


@dp.message_handler(
    lambda message: IsUnbanned(message)() and (message.text == "👩🏼 Поиск Ж" or message.text == "👨🏼 Поиск М"))
async def DONATE_SEARCH(message: Message):
    user = User(message.from_user.id)
    if user.subscription:
        excepted_gender = {"👩🏼 Поиск Ж": "female",
                           "👨🏼 Поиск М": "male"}[message.text]
        if user.status == UserStatus.FREE:
            result = user.start_conversation(excepted_gender=excepted_gender)
            if result == ConversationStatus.WAITING:
                text = f"<i>{message.text} начат!</i>"
                await message.answer(text=text, reply_markup=close_search)
            else:
                text = "<i>✅ Собеседник успешно найден!</i>\n\n" \
                       "<i>◾ Доступные команды: </i>\n\n" \
                       "<b>➖ /next - следующий собеседник</b>\n" \
                       "<b>➖ /stop - завершить диалог</b>\n" \
                       "<b>➖ /link - поделиться ссылкой на свой аккаунт</b>"
                await dp.bot.send_message(chat_id=user.interlocutor,
                                          text=text,
                                          reply_markup=close_dialog)
                await message.answer(text=text,
                                     reply_markup=close_dialog)
    else:
        await message.answer("<i>⚠ У вас отсутствует подписка!</i>",
                             reply_markup=close)
