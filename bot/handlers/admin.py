from loader import dp, Message, User, IsAdmin, Statistic, ContainerSubscriptions, Promocode
from bot.keyboards import close

@dp.message_handler(lambda message: IsAdmin(message)() and message.text == "/admin")
async def ADMIN_OPEN(message: Message):
    await message.answer(text="<i>👑 Приветствую вас, мой повелитель!</i>\n\n"
                              "<i>◾ Доступные команды:</i>\n\n"
                              "<b>➖ <code>/ban user_id</code> | перманентный бан</b>\n"
                              "<b>➖ <code>/warn user_id during</code> | временный бан (during в часах)</b>\n"
                              "<b>➖ <code>/unban user_id</code> | снятие бана/мута</b>\n"
                              "<b>➖ <code>/spam + ответ на сообщение</code> | рассылка</b>\n"
                              "<b>➖ <code>/stat</code> | статистика</b>\n"
                              "<b>➖ <code>/set sub_name sub_price</code> | смена цены на подписку</b>\n"
                              "<b>➖ <code>/new promo body sub_bonus(в часах) activations</code> | создать промокод</b>\n"
                              "<b>➖ <code>/promo</code> | показать действующие промокоды</b>\n"
                              "<b>➖ <code>/delete promo</code> | удалить промокод</b>\n",
                         reply_markup=close)
    await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)(), regexp="/ban \d+")
async def BAN_USER(message: Message):
    user_id = message.text.replace("/ban ", "")
    try:
        user = User(user_id)
        user.get_ban()
        await message.answer(text=f"<i>✅ Пользователь <code>id{user_id}</code> был успешно забанен!</i>",
                             reply_markup=close)
    except:
        await message.answer(text=f"<i>⚠ Пользователь <code>id{user_id}</code> забанен не был!</i>\n\n"
                                  f"<b>🤷‍♂ <u>Причина:</u> <code>некорректный user_id</code></b>",
                             reply_markup=close)
    finally:
        await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)(), regexp="/unban \d+")
async def UNBAN_USER(message: Message):
    user_id = message.text.replace("/unban ", "")
    try:
        user = User(user_id)
        user.get_unban()
        await message.answer(text=f"<i>✅ Пользователь <code>id{user_id}</code> был успешно разбанен!</i>",
                             reply_markup=close)
    except:
        await message.answer(text=f"<i>⚠ Пользователь <code>id{user_id}</code> разбанен не был!</i>\n\n"
                                  f"<b>🤷‍♂ <u>Причина:</u> <code>некорректный user_id</code></b>",
                             reply_markup=close)
    finally:
        await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)(), regexp="/mute \d+ \d+")
async def MUTE_USER(message: Message):
    user_id, during = message.text.replace("/mute ", "").split(" ")
    try:
        user = User(user_id)
        user.admin_get_warn(int(during))
        await message.answer(text=f"<i>✅ Пользователь <code>id{user_id}</code> был успешно забанен до {user.banned_for}!</i>",
                             reply_markup=close)
    except:
        await message.answer(text=f"<i>⚠ Пользователь <code>id{user_id}</code> забанен не был!</i>\n\n"
                                  f"<b>🤷‍♂ <u>Причина:</u> <code>некорректный user_id или during</code></b>",
                             reply_markup=close)
    finally:
        await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)(), commands=["spam"])
async def SPAM(message: Message):
    if message.reply_to_message:
        message1 = await message.reply_to_message.reply(text="<i>✅ Рассылка сообщения успешно началась!</i>")
        success = 0
        failure = 0
        for user_id in User.get_all():
            try:
                await message.reply_to_message.copy_to(chat_id=user_id)
                success += 1
            except:
                failure += 1
        await message1.delete()
        await message.answer(text=f"<i>✅ Рассылка закончилась успешно!</i>\n\n"
                                  f"<b><u>📊 Результаты рассылки:</u></b>\n\n"
                                  f"<b>👌🏻 Успех:</b> <code>{success}</code>\n\n"
                                  f"<b>🤬 Провал:</b> <code>{failure}</code>",
                             reply_markup=close)
        await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)(), commands=["stat"])
async def STAT(message: Message):
    user_stat = Statistic.users_amount()
    conversation_stat = Statistic.conversations_amount()
    await message.answer(text=f"<i>👥 Пользователей в проекте: <code>{user_stat.get('all_users')}</code></i>\n\n"
                              f"<i>🥶 Забаненных: <code>{user_stat.get('banned_users')}</code></i>\n\n"
                              f"<i>🥵 Свободных: <code>{user_stat.get('free_users')}</code></i>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
                              f"<i>💬 Диалогов всего: <code>{conversation_stat.get('amount')}</code></i>\n\n"
                              f"<i>📅 Общая длительность: <code>{conversation_stat.get('total_during')}</code></i>\n\n"
                              f"<i>🕐 Средняя длительность: <code>{conversation_stat.get('average_during')}</code></i>\n\n",
                         reply_markup=close)
    await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)(), regexp="/set ([\w_]+) \d+")
async def MUTE_USER(message: Message):
    sub_type, new_price = message.text.split(" ")[1:]
    try:
        ContainerSubscriptions.get(sub_type).edit_subscription(new_price)
        await message.answer(
            text=f"<i>✅ Цена на подписку <code>{sub_type}</code> была изменена!</i>",
            reply_markup=close)
    except:
        await message.answer(
            text=f"<i>⚠ Цена на подписку <code>{sub_type}</code> не была изменена!</i>",
            reply_markup=close)
    finally:
        await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)(), regexp="/new promo .+ [\d.]+ \d+")
async def NEW_PROMO(message: Message):
    promo, bonus, max = message.text.split(" ")[2:]
    promo = Promocode.create(promo, bonus, max)
    if promo:
        await message.answer(f"<i>✅ Промокод <code>{promo}</code> успешно создан!</i>")
    else:
        await message.answer(f"<i>⚠ Промокод не создан!</i>")
    await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)() and message.text == "/promo")
async def NEW_PROMO(message: Message):
    promos = Promocode.get_all()
    text = ""
    for i in promos:
        promo = Promocode(i[0])
        text += f"<i>PROMO: <code>{promo.promo}</code>\n</i>"
        text += f"<i>BONUS: <code>+{promo.subscription_bonus} hours</code>\n</i>"
        text += f"<i>USED: <code>{len(promo.activations)}/{promo.max_activations}</code>\n</i>"
        text += "➖➖➖➖➖➖➖➖➖➖➖➖\n"
    await message.answer(text=text,
                         reply_markup=close)
    await message.delete()

@dp.message_handler(lambda message: IsAdmin(message)(), regexp="/delete .+$")
async def DELETE_PROMO(message: Message):
    result = Promocode.delete(message.text.split(" ")[1])
    if result:
        await message.answer(f"<i>✅ Промокод успешно удалён!</i>")
    else:
        await message.answer(f"<i>⚠ Промокод не удалён!</i>")
    await message.delete()
