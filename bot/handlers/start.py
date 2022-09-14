import datetime
import re
import time



from loader import dp, Message, CallbackQuery, User, IsUnbanned, rules_link, ContainerSubscriptions, Bill, IsAdmin, FSMContext
from bot.keyboards import main_menu, choosing_gender, cabinet, subscription, buy_subscription, close
from bot.states import PromocodeActivity

@dp.message_handler(commands=["start"])
async def START(message: Message):
    user = User(message.from_user.id)
    if re.search(r"/start \d+", message.text):
        if user.refer == 0:
            user = User(message.from_user.id)
            owner = User(re.findall(r"/start (\d+)", message.text)[0])
            if owner.id != user.id:
                owner.get_subscription(1)
                user.set_refer(owner.id)
                user.get_subscription(1)
                await dp.bot.send_message(chat_id=owner.id,
                                          text=f"<i>🥳 <code>@{message.from_user.username}</code> перешёл по вашей ссылке!</i>\n\n"
                                               f"<b>📅 Ваша подписка закончится <code>{owner.subscription}</code></b>")
                await message.answer(text=f"<i>🥳 <code>@{message.from_user.username}</code>, вы перешли по реферальной ссылке, поэтому получаете бесплатную подписку на день!</i>\n\n"
                                          f"<b>📅 Ваша подписка закончится <code>{user.subscription}</code></b>")
    if user.gender == "unknown":
        await message.answer(text="<i>⚠ Для работы с ботом выберите ваш пол</i>",
                             reply_markup=choosing_gender)
    else:
        await message.answer(f"<i>👋🏻 Приветствую, {message.from_user.full_name}</i>\n\n"
                             f"<i>⚠ Прежде чем перейти к использованию бота, учти, что ты автоматически принимаешь <a href='{rules_link}'>правила бота</a></i>\n\n"
                             f"<b>🥳 Ну а теперь, после прочтения <a href='{rules_link}'>правил бота</a>, ты можешь смело писать /find или нажимать на кнопку поиска собеседника и общаться</b>\n\n"
                             f"<b>♥ Приятного общения</b>", reply_markup=main_menu)
    await message.delete()


@dp.callback_query_handler(lambda call: IsUnbanned(call)() and "choose_gender_" in call.data)
async def CHOOSE_GENDER(call: CallbackQuery):
    gender = call.data.replace("choose_gender_", "")
    user = User(call.from_user.id)
    if user.gender == "unknown":
        user.set_gender(gender=gender)
        await call.message.answer(f"<i>👋🏻 Приветствую, {call.from_user.full_name}</i>\n\n"
                                  f"<i>⚠ Прежде чем перейти к использованию бота, учти, что ты автоматически принимаешь <a href='{rules_link}'>правила бота</a></i>\n\n"
                                  f"<b>🥳 Ну а теперь, после прочтения <a href='{rules_link}'>правил бота</a>, ты можешь смело писать /find или нажимать на кнопку поиска собеседника и общаться</b>\n\n"
                                  f"<b>♥ Приятного общения</b>", reply_markup=main_menu)
        await call.message.delete()
    elif user.gender == gender:
        await call.answer("⚠ У вас уже установлен этот пол!", show_alert=True)
    else:
        user.set_gender(gender=gender)
        await call.message.edit_reply_markup(reply_markup=cabinet(user.gender))


@dp.message_handler(lambda message: IsUnbanned(message)() and message.text == "👤 Личный кабинет")
async def CABINET(message: Message):
    user = User(message.from_user.id)
    subscription_info = f"<i>💎 Подписка до <code>{user.subscription}</code></i>\n\n" if user.subscription else "<i>☹ У вас нет подписки</i>\n\n"
    await message.answer(text=f"<i>🆔 Ваш id <code>[{user.id}]</code></i>\n\n"
                              + subscription_info +
                              f"<i>📅 Вы в с нами с <code>{user.reg_date}</code></i>\n\n"
                              f"<i>🥶 Вы получили временных банов</i> <code>[{user.warnings - 1}]</code>\n\n"
                              f"<i>📊 Собеседники поставили вам:</i>\n\n"
                              f"<i>🥰 Лайков</i> <code>[{user.likes}]</code>\n"
                              f"<i>🤮 Дисклайков</i> <code>[{user.dislikes}]</code>",
                         reply_markup=cabinet(user.gender))
    await message.delete()


@dp.message_handler(lambda message: IsUnbanned(message)() and message.text == "💎 Подписка")
async def SUBSCRIPTION(message: Message):
    user = User(message.from_user.id)
    cost_1day = ContainerSubscriptions.get('day').cost
    cost_1week = ContainerSubscriptions.get('week').cost
    benefit_week = round(((7 * cost_1day - cost_1week) / (cost_1day * 7)) * 100)
    cost_1month = ContainerSubscriptions.get('month').cost
    benefit_month = round(((30 * cost_1day - cost_1month) / (cost_1day * 30)) * 100)
    await message.answer(text=f"<i>⚙ Существует <u>2 способа</u> получения подписки:</i>\n\n"
                              f"<b>➖ Покупка с помощью кнопок внизу</b>\n\n"
                              f"<i>💰 Цены на подписки:</i>\n\n"
                              f"<i>😏 1 день</i> <code>{cost_1day} RUB</code>\n"
                              f"<i>🤤 1 неделя</i> <code>{cost_1week} RUB</code> <b>(<u>выгода {benefit_week}%</u>)</b>\n"
                              f"<i>😎 1 месяц</i> <code>{cost_1month} RUB</code> <b>(<u>выгода {benefit_month}%</u>)</b>\n\n"
                              f"<b>➖ Приглашение рефералов:</b>\n\n"
                              f"<i>▫ <u>1 реферал</u> → <u>+1 день</u> подписки вам</i>\n"
                              f"<i>▫ Переход по реф. ссылке → <u>+1 день</u> подписки рефералу</i>\n"
                              f"<i>▫ <u>1 купленный день</u> подписки рефералом → <u>+3 часа</u> подписки вам</i>\n\n"
                              f"<i>📎 Ваша пригласительная ссылка:</i>\n\n"
                              f"<i>https://t.me/{(await dp.bot.get_me()).username}?start={user.id}</i>",
                         reply_markup=subscription)
    await message.delete()

@dp.callback_query_handler(lambda call: IsUnbanned(call)() and "buy_sub_" in call.data)
async def BUY_SUB(call: CallbackQuery):
    user = User(call.from_user.id)
    sub = ContainerSubscriptions.get(call.data.replace("buy_sub_", ""))
    start_time = datetime.datetime.now()
    bill = (await Bill.create_bill(sub.cost, user.id, sub.during))
    end_time = start_time + datetime.timedelta(minutes=7)
    if bill:
        message2 = await call.message.answer(
            text=f"<i>⚠ Для приобретения подписки оплатите <code>{sub.cost} RUB</code>, перейдя по <a href='{bill.pay_url}'>ссылке</a></i>:\n\n"
                 f"<b>{bill.pay_url}</b>\n\n"
                 f"<i>⚠ После оплаты бот автоматически выдаст вам соответсвующую подписку!</i>\n"
                 f"<i>⚠ Счёт действителен только <code>7 минут</code>!</i>",
            reply_markup=buy_subscription(bill.pay_url, bill.bill_id))
        complete = False
        while start_time < end_time:
            result = await Bill.check_bill(bill.bill_id)
            if result:
                user.get_subscription(result)
                if user.refer != 0:
                    refer = User(user.refer)
                    refer.get_subscription(round(result / 8, 2))
                    try:
                        await dp.bot.send_message(chat_id=user.refer,
                                                  text=f"<i>🥳 <code>@{call.from_user.username}</code> купил подписку!</i>\n\n"
                                                       f"<b>📅 Ваша подписка закончится <code>{refer.subscription}</code></b>")
                    except:
                        pass
                await call.message.answer(text="<i>✅ Подписка была успешно приобретена!</i>\n\n"
                                               f"<b>📅 Она закончится <code>{user.subscription}</code></b>")
                complete = True
                break
            elif IsAdmin(call)():
                user.get_subscription(await Bill.admin_complete(bill.bill_id))
                await call.message.answer(text="<i>✅ Подписка была успешно приобретена!</i>\n\n"
                                               f"<b>📅 Она закончится <code>{user.subscription}</code></b>")
                break
            time.sleep(0.1)
        if not complete:
            await Bill.close_bill(bill.bill_id)
            await call.message.answer(text="<i>⚠ Счёт был закрыт!</i>")
        await message2.delete()
    else:
        await call.answer(text="⚠ У тебя уже есть неоплаченный счёт\n"
                               "⚠ Оплатите его или дождитесь момента, когда он истечёт (7 минут с момента создания)",
                          show_alert=True)


@dp.callback_query_handler(lambda call: IsUnbanned(call)() and "close_bill_" in call.data)
async def BUY_SUB(call: CallbackQuery):
    await Bill.close_bill(bill_id=call.data.replace("close_bill_", ""))
    await call.message.delete()


@dp.callback_query_handler(lambda call: IsUnbanned(call)() and "activate_promocode" == call.data)
async def ACTIVATE_PROMOCODE(call: CallbackQuery):
    await PromocodeActivity.activate.set()
    await call.answer("⚠ Введите промокод!", show_alert=True)


@dp.message_handler(lambda message: IsUnbanned(message)(), state=PromocodeActivity.activate)
async def ACTIVATE_PROMOCODE(message: Message, state=FSMContext):
    await state.finish()
    user = User(message.from_user.id)
    result = user.activate_promocode(message.text)
    if result:
        await message.answer(text=f"<i>🥳 Вы активировали промокод и получили <u>{result} часов</u> подписки!</i>\n\n")
    else:
        await message.answer(text=f"<i>⚠ Был введён невалидный промокод</i>\n\n",
                             reply_markup=close)
    await message.delete()