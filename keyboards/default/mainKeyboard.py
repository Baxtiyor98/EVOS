from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

mainKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📍Manzilni o\'zgartirish'),
            KeyboardButton(text='🧾Menu'),
        ],
        [
            KeyboardButton(text='🛒Buyurtmalarim'),
        ],
        [
            KeyboardButton(text='💬Fikr bildirish'),
            KeyboardButton(text='⚙️Sozlamalar'),
        ],
        [
            KeyboardButton(text='👨‍💻Programmer'),
        ],
    ],
    resize_keyboard=True
)

locationKey = ReplyKeyboardMarkup(
    keyboard=[
        [   
            KeyboardButton(text='📍Location',request_location=True),
        ],
        [
            KeyboardButton(text='◀️Ortga')
        ],
    ],
    resize_keyboard=True
)


back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='◀️Ortga')
        ]
    ],
    resize_keyboard=True
)

payKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💵Naqd'),
        ],
        [
            KeyboardButton(text='💳Payme'),
        ],
        [
            KeyboardButton(text='💳Click'),
        ],
        [
            KeyboardButton(text='◀️Ortga'),
        ],
    ],
    resize_keyboard=True
)
