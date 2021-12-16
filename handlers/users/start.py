from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from loader import dp
from utils.db_api.database import DBCommands, create_db
from keyboards.default.mainKeyboard import mainKeyboard
from states.personalData import PersonalData
from data.config import ADMINS
db = DBCommands()

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await create_db()
    current_user =  types.User.get_current()
    users = await db.get_users()
    user = []
    for i in users:
        user.append(i.telegram_id)
    if str(current_user.id) in user:
        await message.answer('Siz ro\'yhatdan o\'tgansiz', reply_markup=mainKeyboard)
    else:
        await message.answer("Assalom alaykum foydalanuvchi!\nRo\'yhatdan o\'tish uchun to'liq ismingizni kiriting:",reply_markup=ReplyKeyboardRemove())
        await PersonalData.fullname.set()