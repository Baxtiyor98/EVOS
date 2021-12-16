from aiogram.dispatcher.filters import Command, Text, state
from aiogram.types import Message, ReplyKeyboardRemove,CallbackQuery, location
from aiogram.utils.mixins import T
from keyboards.default.registrationKeyboard import locationkey,contactkey
from aiogram.types.message import ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram import types
from utils.db_api.database import User
from utils.db_api.database import DBCommands
from keyboards.default.mainKeyboard import mainKeyboard
from states.personalData import Setting,catManu


# from keyboards.inline.settingKeyboard
from loader import dp
db = DBCommands()

@dp.callback_query_handler(text=['phone_number','location','full_name'],state=None)
async def setting(call: CallbackQuery):
    callback_data = call.data
    if callback_data=='phone_number':
        await call.message.answer('Telefon nomer yuboring', reply_markup=contactkey)
    elif callback_data=='location':
        await call.message.answer('Manzilingizni yuboring!',reply_markup=locationkey)
    else:
        await Setting.setting.set()
        await call.message.answer('To\'liq ism, familyangizni yuboring!',reply_markup=ReplyKeyboardRemove())
    await call.message.delete()
    await call.answer(cache_time=60)

@dp.message_handler(content_types=ContentTypes.CONTACT)
async def change_contact(message: Message):
    id =  types.User.get_current().id
    phone = message.contact["phone_number"]
    await message.answer('Ma\'lumot yanglandi.', reply_markup=mainKeyboard)
    await db.update_phone(id,phone)


# @dp.message_handler(content_types=ContentTypes.LOCATION)
async def change_location2(message: Message):
    id =  types.User.get_current().id
    location=message.location
    await message.answer('Ma\'lumot yanglandi.', reply_markup=mainKeyboard)
    await db.update_location(id,f"{location['latitude']},{location['longitude']}")


@dp.message_handler(content_types=types.ContentTypes.TEXT,state=Setting.setting)
async def change_name(message: Message,state: FSMContext):
    id =  types.User.get_current().id
    name=message.text
    print(name,id)
    await message.answer('Ma\'lumot yanglandi.', reply_markup=mainKeyboard)
    await db.update_name(id,name)
    await state.finish()

