from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ReplyKeyboardMarkup, ContentTypes, BotCommand
from database import bot_token, rules_link
from entities import User, Conversation, ConversationStatus, UserStatus, IsUnbanned, IsAdmin, Statistic, ContainerSubscriptions, WeekSubscription, DaySubscription, MonthSubscription, Bill, Promocode

bot = Bot(bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

