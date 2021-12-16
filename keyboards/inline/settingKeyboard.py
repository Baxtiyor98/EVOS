from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

settingkey = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Telefon', callback_data='phone_number'),
            InlineKeyboardButton(text='Manzil', callback_data='location'),
            InlineKeyboardButton(text='Ism', callback_data='full_name'),
        ],
    ],
)