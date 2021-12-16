from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import types
from utils.db_api.database import DBCommands
from keyboards.default.mainKeyboard import mainKeyboard,payKeyboard
from states.personalData import Order
from keyboards.inline.cat_menuKeyboards import orderKeyboard

from loader import dp
db = DBCommands()

@dp.callback_query_handler(state=Order.order)
async def order(call: CallbackQuery,state: FSMContext):
    id = types.User.get_current().id
    order = await db.get_order(id)
    callback_data = call.data
    if callback_data=='back':
        await call.message.delete()
        await call.message.answer('Asosiy menyu', reply_markup=mainKeyboard)
        await state.finish()
    elif callback_data=='clear':
        await call.message.delete()
        await call.answer('Barcha buyurtmalar o\'chirildi',show_alert=True)
        await call.message.answer('Asosiy menyu', reply_markup=mainKeyboard)
        await state.finish()
    elif callback_data=='order':
        await call.message.delete()
        await call.message.answer('To\'lov turini tanlang', reply_markup=payKeyboard)
        await state.finish()
    else:
        await db.delete_order(callback_data)
        order = await db.get_order(id)
        await call.message.edit_text(text=f'Jami buyurtmalar soni: {len(order)}',reply_markup=orderKeyboard(order))
    await call.answer(cache_time=60)
