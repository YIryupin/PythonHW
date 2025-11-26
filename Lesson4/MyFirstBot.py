import os
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from dotenv import load_dotenv
from aiogram.filters import Command
from aiogram.filters import and_f, or_f
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove


load_dotenv()  # загружаем переменные окружения
API_TOKEN = os.getenv("BOT_TOKEN")  # достаём токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


#Обработка сообщений:
router = Router()

#Обработка команды /Start
@router.message(Command("start"))
async def start_command(message: types.Message):
#    await message.answer(f"Привет! Я твой первый бот на Aiogram. Чем могу помочь?")
    await message.answer("Привет! Нажми кнопку:", reply_markup=getInlineKeyboard())
    await message.answer("👋 Добро пожаловать! Выберите действие:", reply_markup=getReplyKeyboard())

#Обработка команды /Help
@router.message(Command("help"))
async def help_command(message: types.Message):
   await message.answer(f"Тут будет раздел помощи по командам...")

#Обработка команд /Hi, /Hello
@router.message(or_f(Command("hi"), Command("hello")))
async def hello_commands(message: types.Message):
    await message.answer("Привет! Я робот.")

#Обработка неизвестных команд 
@router.message(lambda message: message.text and message.text.startswith('/'))
async def hello_commands(message: types.Message):
    await message.answer("Неизвестная команда, используйте команду /help")


#Обработка любого другого сообщения а также сообщений от ReplyKeyboard
@router.message()
async def echo_message(message: types.Message):
    if message.text == "ℹ️ О боте":
        await message.answer(f"Тут будет раздел информации о боте...")
    elif message.text == "❌ Скрыть клавиатуру":
        await message.answer(
            "⌨️ Клавиатура скрыта!\n"
            "Используйте /start для возврата меню.",
            reply_markup=ReplyKeyboardRemove()
        )
    else: 
        user_text = message.text
        await message.answer(f"Ты написал: {user_text}")

#Обработка обратного вызова для InlineMenu
@router.callback_query()
async def callbacks(callback: CallbackQuery):
    if callback.data == "open_menu":
        await callback.message.answer("Это меню!")

#Метод формирования структуры ReplyKeyboard
def getReplyKeyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ℹ️ О боте"), KeyboardButton(text="❌ Скрыть клавиатуру")],
        ],
        resize_keyboard=True,  # Автоматическое изменение размера
        input_field_placeholder="Выберите действие..."  # Подсказка в поле ввода
    )
    return keyboard

#Метод формирования структуры InlineKeyboard
def getInlineKeyboard():
    InlineKB = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть меню", callback_data="open_menu")]
        ]
    )
    return InlineKB

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

#Вопросы:
#Различия в принципах работы меню? Чем отличается колбак от простой обработки сообщений?
#Лямбда выражения
#Символы ❌
#Навигация по коду