from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from utils.db_api.database import DBCommands

db = DBCommands

def categoryKeyboard(category):
    categoryMenu = InlineKeyboardMarkup(row_width=2)
    categoryMenu.insert(InlineKeyboardButton(text='Barcha menyular',url='https://telegra.ph/EVOS-MENU-04-05-2'))
    categories = {}
    for i in category:
        categories[f"{i.category_id}"] = f"{i.category_name}"
    for key,value in categories.items():
        categoryMenu.insert(InlineKeyboardButton(text=value,callback_data=key))
    return categoryMenu

def productKeyboard(product,id):
    productMenu = InlineKeyboardMarkup(row_width=2)
    products = {}
    for i in product:
        if int(i.category_id)==int(id):
            products[f"{i.product_id}"] = f"{i.product_name}"
    print(products)
    for key,value in products.items():
        productMenu.insert(InlineKeyboardButton(text=value,callback_data=key))
    productMenu.add(InlineKeyboardButton(text='Zakazni davom ettirish', callback_data='continue'))
    productMenu.add(InlineKeyboardButton(text='◀️Ortga', callback_data='back'))
    return productMenu

def quantityKeyboard():
    quantityMenu = InlineKeyboardMarkup(row_width=2)
    quantityMenu.insert(InlineKeyboardButton(text='🔼', callback_data='up'))
    quantityMenu.insert(InlineKeyboardButton(text='🔽', callback_data='down'))
    quantityMenu.add(InlineKeyboardButton(text='🛒Savatchaga qo\'shish', callback_data='cart'))
    quantityMenu.add(InlineKeyboardButton(text='◀️Ortga', callback_data='back'))
    return quantityMenu

def orderKeyboard(order):
    orderMenu = InlineKeyboardMarkup(row_width=2)
    orders = {}
    for i in order:
        orders[f"{i.order_id}"] = f"{i.product_name} | {i.quantity} dona"
    print(orders)
    s = 1
    for key,value in orders.items():
        orderMenu.insert(InlineKeyboardButton(text=f'{s}. {value}', callback_data='0000'))
        orderMenu.insert(InlineKeyboardButton(text='❌',callback_data=f"{key}"))
        s+=1
    orderMenu.add(InlineKeyboardButton(text='🚖Buyurtma berish', callback_data='order'))
    orderMenu.insert(InlineKeyboardButton(text='🗑Savatni bo\'shatish', callback_data='clear'))
    orderMenu.insert(InlineKeyboardButton(text='◀️Ortga', callback_data='back'))
    return orderMenu

def confirmLocationKeyboard():
    confirmMenu = InlineKeyboardMarkup(row_width=2)
    confirmMenu.insert(InlineKeyboardButton(text='✅ Ha', callback_data='yes'))
    confirmMenu.insert(InlineKeyboardButton(text='❌ Yo\'q', callback_data='no'))
    return confirmMenu