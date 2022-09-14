from loader import dp, CallbackQuery, FSMContext

@dp.callback_query_handler(lambda call: call.data == "close")
async def CLOSE(call: CallbackQuery):
    await call.message.delete()

@dp.callback_query_handler(lambda call: call.data == "close", state="*")
async def CLOSE(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == "close_reply")
async def CLOSE_REPLY(call: CallbackQuery):
    await call.message.reply_to_message.delete()
    await call.message.delete()

@dp.callback_query_handler(lambda call: call.data == "close_reply", state="*")
async def CLOSE_REPLY(call: CallbackQuery, state=FSMContext):
    await call.message.reply_to_message.delete()
    await call.message.delete()
    await state.finish()