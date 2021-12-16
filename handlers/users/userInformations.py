from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.types.message import ContentTypes
from geopy import Nominatim

from loader import dp
from states import personalData
from states.personalData import PersonalData
from keyboards.default.registrationKeyboard import contactkey, locationkey
from keyboards.default.mainKeyboard import mainKeyboard
from keyboards.inline.cat_menuKeyboards import confirmLocationKeyboard
from utils.db_api.database import DBCommands
db = DBCommands

@dp.message_handler(Command('account'), state=None)
async def registration(message: types.Message):
    await message.answer("To'liq ismingizni kiriting:")
    await PersonalData.fullname.set()

@dp.message_handler(state=PersonalData.fullname)
async def fullname(message: Message, state: FSMContext):
    full_name = message.text
    await state.update_data(
        {'full_name':full_name}
    )
    await message.answer('Nomerni ulashish tugmasini bosing',reply_markup=contactkey)
    await PersonalData.phone.set()

@dp.message_handler(content_types=ContentTypes.TEXT,state=PersonalData.phone)
@dp.message_handler(content_types=ContentTypes.CONTACT,state=PersonalData.phone)
async def getcontact(message: Message, state: FSMContext):
    if ContentTypes.CONTACT:
        phone = message.contact
        print(phone["phone_number"])
        await state.update_data(
            {"phone":phone["phone_number"]}
        )
    elif ContentTypes.TEXT:
        phone = message.text
        await state.update_data(
        {"phone":phone}
        )
    await message.answer("Geo-joylashuv yuboring yoki manzil kiriting",reply_markup=locationkey)
    await PersonalData.next()


@dp.message_handler(content_types=ContentTypes.LOCATION,state=PersonalData.location)
@dp.message_handler(content_types=ContentTypes.TEXT,state=PersonalData.location)
async def location(message: types.Message, state: FSMContext):
    location =  message.location
    latitude = f"{location['latitude']}"
    longitude = f"{location['longitude']}"
    
    geolocator = Nominatim(user_agent="geoapiExercises")
    locat = geolocator.reverse(latitude+","+longitude)  
    address = locat.raw['address']
    a = ['house_number','road','residential','county','city']
    addres = []
    s = ''
    if 'residential' in address:
        a.pop(3)
    for i in a:
        if i in address:
            addres.append(i)
            s += address[i] + "," 
    if ContentTypes.LOCATION:
        await state.update_data(
            {"location":f"{s[:-1]}"}
        )
    elif ContentTypes.TEXT:
        location = message.text
        await state.update_data(
        {"location":location}
        )
    await message.answer(f"Sizning manzilingiz:\n{s[:-1]}\nManzilni tasdiqlaysizmi?", reply_markup=confirmLocationKeyboard())
    await PersonalData.confirm_location.set()

@dp.callback_query_handler(state=PersonalData.confirm_location)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    await call.message.edit_reply_markup()
    if data == "yes":
        await call.message.answer('Muvaffaqiyatli ro\'yhatdan o\'tdingiz👏👏👏')
        await call.message.answer('Asosiy menyu', reply_markup=mainKeyboard)
        data = await state.get_data()
        user =  types.User.get_current()
        await db.create_user(str(user.id),data.get('full_name'),str(data.get('phone')),user.username,str(data.get('location')))
        await state.finish()
    elif data == "no":
        # await state.finish()
        await call.message.answer(text = "Qayta geo-joylashuv yuboring yoki manzil kiriting",reply_markup=locationkey)
        await PersonalData.location.set()
    
