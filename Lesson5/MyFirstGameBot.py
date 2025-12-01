import random
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

from GameLib import RPSGame

load_dotenv()  # загружаем переменные окружения
API_TOKEN = os.getenv("BOT_TOKEN")  # достаём токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

#Обработка сообщений:
router = Router()

@router.message(lambda message: message.text and message.text == "Начать игру")
async def hello_commands(message: types.Message):
    await message.answer("Сделай выбор: ", reply_markup=getInlineKeyboard4RPSGame())

@router.message(lambda message: message.text and message.text == "ℹ️ Правила")
async def hello_commands(message: types.Message):
    await message.answer(RPSGame.getHelp())

#Обработка неизвестных команд 
@router.message(lambda message: message.text and message.text.startswith('/'))
async def hello_commands(message: types.Message):
    await message.answer("Неизвестная команда, используйте меню")


#Обработка любого другого сообщения а также сообщений от ReplyKeyboard
@router.message()
async def echo_message(message: types.Message):
    await message.answer("👋 Привет! Я Гейм Бот! Давай сыграем?", reply_markup=getReplyKeyboard())

#Метод формирования структуры InlineKeyboard
def getInlineKeyboard4RPSGame():
    InlineKB = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Камень", callback_data="Камень")],
            [InlineKeyboardButton(text="Ножницы", callback_data="Ножницы")],
            [InlineKeyboardButton(text="Бумага", callback_data="Бумага")]
        ]
    )
    return InlineKB

#Обработка обратного вызова для InlineMenu
@router.callback_query()
async def callbacks(callback: CallbackQuery):
    game = RPSGame()
    botChoice = game.botChoice()
    await callback.message.answer(f"Твой выбор - {callback.data}")
    await callback.message.answer(f"Мой выбор - {botChoice}")
    gameResult = game.gameResult(callback.data, botChoice)
    if gameResult == "N":
        await callback.message.answer("Ничья!")
    elif gameResult == "P1":
        await callback.message.answer("Ты победил!")
    elif gameResult == "P2":
        await callback.message.answer("Победил геймбот!")
    await callback.message.answer("Хочешь сыграть ещё раз? Нажми Начать игру в меню!")

#Метод формирования структуры ReplyKeyboard
def getReplyKeyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начать игру"), KeyboardButton(text="ℹ️ Правила")],
        ],
        resize_keyboard=True,  # Автоматическое изменение размера
        input_field_placeholder="Выберите действие...",  # Подсказка в поле ввода
        one_time_keyboard=True #скрывает кнопку после использования пользователем
    )
    return keyboard


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
