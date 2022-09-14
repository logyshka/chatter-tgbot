from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choosing_gender = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("👩🏼 Женский", callback_data="choose_gender_female"),
    InlineKeyboardButton("👨🏼 Мужской", callback_data="choose_gender_male")
)


def cabinet(gender):
    text1 = "👩🏼 Девушка"
    text2 = "👨🏼 Парень"
    if gender == "female":
        text1 += " ✅"
    else:
        text2 += " ✅"
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text1, callback_data="choose_gender_female"),
        InlineKeyboardButton(text2, callback_data="choose_gender_male"),
        InlineKeyboardButton("🔑 Активировать промокод", callback_data="activate_promocode")).add(
        InlineKeyboardButton("✖", callback_data="close")
    )
