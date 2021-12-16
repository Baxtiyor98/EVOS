from aiogram import types
from loader import dp
from utils.db_api.database import DBCommands
from states.personalData import catManu
from aiogram.dispatcher import FSMContext
from keyboards.inline.cat_menuKeyboards import productKeyboard,categoryKeyboard,quantityKeyboard
from aiogram.types import CallbackQuery

db = DBCommands()

@dp.callback_query_handler(text = ['back','continue'],state=catManu.menu)
async def category_menu(call: CallbackQuery,state: FSMContext):
    await call.message.delete()
    category = await db.get_category()
    await call.message.answer("https://telegra.ph/EVOS-MENU-04-05-2",reply_markup=categoryKeyboard(category))
    await call.answer(cache_time=60)
    await state.finish()

@dp.callback_query_handler(state=None)
async def product_menu(call: CallbackQuery,state: FSMContext):
    product = await db.get_products()
    await call.message.answer(text='Kategoriyalardan birini tanlang',reply_markup=productKeyboard(product,call.data))
    await call.message.delete()
    await call.answer(cache_time=60)
    await catManu.menu.set()

@dp.callback_query_handler(text=['up','down','cart'],state=catManu.menu)
async def order(call: types.CallbackQuery,state: FSMContext):
    id =  types.User.get_current().id
    data = await state.get_data()
    quantity=data.get('menu')
    message = call.message.text
    nomi = message.split('\n')[0].split(':')[1]
    soni = int(message.split('\n')[1].split(':')[1])
    narxi = await db.get_price(nomi)
    
    if call.data=='up':
        await state.update_data(
        {"menu":order_quantity(quantity,call.data)})
        last_order = order_quantity(quantity,call.data)
        soni = last_order
        await call.answer(cache_time=0.01)

    elif call.data=='down' and quantity>1:
        await state.update_data(
        {"menu":order_quantity(quantity,call.data)})
        last_order = order_quantity(quantity,call.data)
        soni = last_order
        await call.answer(cache_time=0.001)

    elif call.data=='cart':
        category = await db.get_category()
        await call.message.delete()
        await state.finish()
        await call.answer(text='Zakaz qabul qilindi',show_alert=False)
        await call.message.answer("https://telegra.ph/EVOS-MENU-04-05-2", reply_markup=categoryKeyboard(category))
        price = soni*narxi
        await db.order(id,nomi,soni,price)
        await call.answer(cache_time=0.001)

    await call.message.edit_text(text=f'Nomi:{nomi}\nSoni: {soni}\nJami: {soni*narxi}',reply_markup=quantityKeyboard())

@dp.callback_query_handler(state=catManu.menu)
async def order(call: CallbackQuery,state: FSMContext):
    await call.message.delete()
    product = await db.get_products()
    await state.update_data(
        {"menu":1}
    )
    print(product[int(call.data)-1].product_name,call.data)
    await call.message.answer(text=f'Nomi: {product[int(call.data)-1].product_name}\nSoni: 1\nJami: {int(product[int(call.data)-1].price)}',reply_markup=quantityKeyboard())

def order_quantity(quantity,type_order):
    if type_order=='up':
        return quantity+1
    elif type_order=='down':
        return quantity-1