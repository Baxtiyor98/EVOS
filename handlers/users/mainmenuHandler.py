from aiogram import types
import logging

from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from data.config import ADMINS
from loader import dp
from geopy import Nominatim
from utils.db_api.database import DBCommands
from keyboards.default.mainKeyboard import mainKeyboard,back
from keyboards.inline.settingKeyboard import settingkey
from states.personalData import Setting, Order
from aiogram.types.message import ContentType, ContentTypes
from utils.db_api.database import User
from aiogram.dispatcher import FSMContext
from keyboards.inline.cat_menuKeyboards import categoryKeyboard, orderKeyboard, confirmLocationKeyboard
from keyboards.default.mainKeyboard import locationKey


db = DBCommands()

@dp.message_handler(text='📍Manzilni o\'zgartirish')
async def change_location(message: types.Message):
    await message.answer('Yangi location yuboring!', reply_markup=locationKey)

@dp.message_handler(content_types=ContentTypes.LOCATION)
async def change_location(message: types.Message):
    id =  types.User.get_current().id
    location =  message.location
    print(location)
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
        await db.update_location(id,f"{location['latitude']},{location['longitude']}")
    elif ContentTypes.TEXT:
        location = message.text
        await db.update_location(id,f"{location}")
    await message.answer(f"Sizning manzilingiz:\n{s[:-1]}\nManzilni tasdiqlaysizmi?", reply_markup=confirmLocationKeyboard())


@dp.message_handler(content_types=ContentTypes.LOCATION)
async def confirm(call: types.CallbackQuery):
    data = call.data
    await call.message.edit_reply_markup()
    if data == "yes":
        await call.answer('Manzil muvaffaqiyatli o\'zgartirildi', reply_markup=mainKeyboard,show_alert=False)
    elif data == "no":
        await call.message.answer(text = "Qayta geo-joylashuv yuboring yoki manzil kiriting",reply_markup=locationKey)

@dp.message_handler(text='⚙️Sozlamalar')
async def setting(message: types.Message):
    id =  types.User.get_current().id
    user = await User.query.where(User.telegram_id == str(id)).gino.first()
    await message.answer(f"Ism: {user.full_name}\nTelefon: +{user.phone_number}\n\nQuyidagilardan birini tanlang", reply_markup=settingkey)

@dp.message_handler(text='💬Fikr bildirish',state=None)
async def connect_admin(message: types.Message,state: FSMContext):
    await Setting.chat.set()
    await message.answer('Sizning fikringiz biz uchun muhim!',reply_markup=back)

@dp.message_handler(content_types=types.ContentTypes.TEXT,state=Setting.chat)
@dp.message_handler(content_types=types.ContentTypes.VOICE,state=Setting.chat)
@dp.message_handler(content_types=types.ContentTypes.VIDEO,state=Setting.chat)
@dp.message_handler(content_types=types.ContentTypes.PHOTO,state=Setting.chat)
@dp.message_handler(content_types=types.ContentTypes.AUDIO,state=Setting.chat)
@dp.message_handler(text='💬Fikr bildirish',state=Setting.chat)
async def connect_admin(message: types.Message,state: FSMContext):
    if types.ContentTypes.TEXT:
        mess = message.text
    elif types.ContentTypes.AUDIO:
        mess = message.audio
    elif types.ContentTypes.VOICE:
        mess = message.voice
    elif types.ContentTypes.PHOTO:
        mess = message.photo
    elif types.ContentTypes.VIDEO:
        mess = message.video
    for admin in ADMINS:
        try:
            if mess == '◀️Ortga':
                await message.answer('Sizning fikringiz biz uchun muhim edi!', reply_markup=mainKeyboard)
                await state.finish()
            else:
                await dp.bot.send_message(admin, mess)
                await message.answer('Fikr bildirganingiz uchun rahmat!', reply_markup=mainKeyboard)
                await state.finish()
        except Exception as err:
            logging.exception(err)

@dp.message_handler(text_contains='◀️Ortga',state=Setting.chat)
async def change(message: types.Message,state: FSMContext):
    await message.answer('Sizning fikringiz biz uchun muhim edi!',disable_notification=True, reply_markup=mainKeyboard)
    await state.finish()

@dp.message_handler(text='🧾Menu')
async def category_menu(message: types.Message,state: FSMContext):
    category = await db.get_category()
    await message.answer("https://telegra.ph/EVOS-MENU-04-05-2",reply_markup=categoryKeyboard(category))

@dp.message_handler(text='👨‍💻Programmer')
async def admin(message: types.Message):
    await message.answer(text="Botni tuzuvchi dasturchi👇👇\n@Django_developer_IT\nBot yuzasidan taklif va fikrlaringiz bo'lsa bemalol murojaat qilishingiz mumkin")

@dp.message_handler(text='🛒Buyurtmalarim')
async def setting(message: types.Message):
    await Order.order.set()
    user =  types.User.get_current()
    order = await db.get_order(user.id)
    if len(order)>0:
        await message.answer('Istalgan buyurtmani bekor qilishingiz mumkin', reply_markup=ReplyKeyboardRemove())
        await message.answer(text=f'Jami buyurtmalar soni: {len(order)}', reply_markup=orderKeyboard(order))
    else:
        await message.answer('Siz hali hanuz birorta ham buyurtma bermagansiz.')

@dp.message_handler(text=['💳Click','💳Payme','💵Naqd'])
async def setting(message: types.Message):
    user =  types.User.get_current()
    order = await db.get_order(user.id)

    s = 0
    for i in order:
        s+=int(i.price)*int(i.quantity)
    await message.answer(f"To'lov turi: {message.text}\nMahsulotlar:    {s} so'm\nYetkazib berish:    9 000 so'm\nJami:    {s+9000} so'm\n"
                        "To'langan:  0 so'm\nBuyurtmangiz qabul qilindi.\nBuyurtmangizni etkazib berish vaqti hisob-fakturani to'lash vaqtidan boshlab 30 daqiqa.",reply_markup=mainKeyboard)

@dp.message_handler(text_contains='◀️Ortga')
async def change(message: types.Message):
    await message.answer('Bosh menyu', reply_markup=mainKeyboard)





