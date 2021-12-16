from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

contactkey = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📞 Nomerni ulashish', request_contact=True),
        ],
    ],
    resize_keyboard=True
)

locationkey = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📍Location', request_location=True)
        ],
    ],
    resize_keyboard=True
)
