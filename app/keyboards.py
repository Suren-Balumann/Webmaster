from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="❌Отмена")]
], resize_keyboard=True, one_time_keyboard=True)
