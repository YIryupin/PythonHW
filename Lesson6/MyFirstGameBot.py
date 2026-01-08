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

from GameLib import RPSGame, Matches21Game
from db import DatabaseManager, DBLib
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

dbManager = DatabaseManager(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
dbLib = DBLib(dbManager)

load_dotenv()  # загружаем переменные окружения
API_TOKEN = os.getenv("BOT_TOKEN")  # достаём токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

#Обработка сообщений:
router = Router()

@router.message(lambda message: message.text and message.text == "Камень ножницы бумага")
async def GameChoiceRPS_commands(message: types.Message):
    dbLib.CreateOrUpdateUser(message.from_user.id, message.from_user.full_name)
    dbLib.ChangeUserGame(message.from_user.id, "RPS")
    await message.answer("Отличный выбор!", reply_markup=getGameMenu(message.text))

@router.message(lambda message: message.text and message.text == "21 спичка")
async def GameChoiceMatches21_commands(message: types.Message):
    dbLib.CreateOrUpdateUser(message.from_user.id, message.from_user.full_name)
    dbLib.ChangeUserGame(message.from_user.id, "Matches21")
    await message.answer("Отличный выбор!", reply_markup=getGameMenu(message.text))

@router.message(lambda message: message.text and message.text == "⬅️ Вернуться в главное меню")
async def MainMenu_commands(message: types.Message):
    await message.answer("Давай сыграем ещё раз! Выбери игру!", reply_markup=getMainMenu())

@router.message(lambda message: message.text and message.text == "🎮 Начать игру")
async def GameStart_commands(message: types.Message):
    gameId = dbLib.GetCurrentGame(message.from_user.id)
    dbLib.userplaylogs_gamestart(message.from_user.id)
    if (gameId == "RPS"):
        await message.answer("Сделай выбор: ", reply_markup=getInlineKeyboard4RPSGame())
    elif (gameId == "Matches21"):
        dbLib.g21matches_setcounter(message.from_user.id, 21)
        await message.answer("На кону спичек - 21. Сделай выбор: ", reply_markup=getInlineKeyboard4Matches21Game())

@router.message(lambda message: message.text and message.text == "📜 Правила игры")
async def GameRules_commands(message: types.Message):
    gameId = dbLib.GetCurrentGame(message.from_user.id)
    if (gameId == "RPS"):
        await message.answer(RPSGame.getHelp())
    elif (gameId == "Matches21"):
        await message.answer(Matches21Game.getHelp())

#Обработка неизвестных команд 
@router.message(lambda message: message.text and message.text.startswith('/'))
async def unknown_commands(message: types.Message):
    dbLib.CreateOrUpdateUser(message.from_user.id, message.from_user.full_name)
    await message.answer("Неизвестная команда, используйте меню", reply_markup=getMainMenu())


#Обработка любого другого сообщения а также сообщений от ReplyKeyboard
@router.message()
async def echo_message(message: types.Message):
    dbLib.CreateOrUpdateUser(message.from_user.id, message.from_user.full_name)
    await message.answer("👋 Привет! Я Гейм Бот! Выбери игру и давай сыграем!", reply_markup=getMainMenu())

#Метод формирования структуры InlineKeyboard для игры Камень Ножницы Бумага
def getInlineKeyboard4RPSGame():
    InlineKB = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Камень", callback_data="Камень")],
            [InlineKeyboardButton(text="Ножницы", callback_data="Ножницы")],
            [InlineKeyboardButton(text="Бумага", callback_data="Бумага")]
        ]
    )
    return InlineKB
#Метод формирования структуры InlineKeyboard для игры 21 Спичка
def getInlineKeyboard4Matches21Game():
    InlineKB = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1", callback_data="1")],
            [InlineKeyboardButton(text="2", callback_data="2")],
            [InlineKeyboardButton(text="3", callback_data="3")],
            [InlineKeyboardButton(text="4", callback_data="4")]
        ]
    )
    return InlineKB

#Обработка обратного вызова для InlineMenu
@router.callback_query()
async def callbacks(callback: CallbackQuery):
    gameId = dbLib.GetCurrentGame(callback.from_user.id)
    if (gameId == "RPS"):
        game = RPSGame()
        botChoice = game.botChoice()
        await callback.message.edit_text("Результат игры:", reply_markup=None)
        await callback.message.answer(f"Твой выбор - {callback.data}")
        await callback.message.answer(f"Мой выбор - {botChoice}")
        gameResult = game.gameResult(callback.data, botChoice)
        if gameResult == "N":
            dbLib.userplaylogs_gamefinish(callback.from_user.id, "Nobody")
            await callback.message.answer("Ничья!")
        elif gameResult == "P1":
            dbLib.userplaylogs_gamefinish(callback.from_user.id, "WinPlayer")
            await callback.message.answer("Ты победил!")
        elif gameResult == "P2":
            dbLib.userplaylogs_gamefinish(callback.from_user.id, "WinBot")
            await callback.message.answer("Победил геймбот!")
        await callback.message.answer("Хочешь сыграть ещё раз? Нажми Начать игру в меню!", reply_markup=None)
    elif (gameId == "Matches21"):
        playerChoice = int(callback.data)
        matchesCounter = dbLib.g21matches_getcounter(callback.from_user.id)
        game = Matches21Game(matchesCounter, playerChoice)
        botChoice = game.botChoice()
        await callback.message.edit_text(f"На кону спичек - {matchesCounter}", reply_markup=None)
        await callback.message.answer(f"Твой выбор - {playerChoice}")
        await callback.message.answer(f"Мой выбор - {botChoice}")
        gameResult = game.gameResult(botChoice)
        if gameResult == "Continue":
            dbLib.g21matches_setcounter(callback.from_user.id, matchesCounter - playerChoice - botChoice)
            await callback.message.answer(f"На кону осталось спичек - {matchesCounter - playerChoice - botChoice}. Сделай следующий ход!", reply_markup=getInlineKeyboard4Matches21Game())
        elif gameResult == "P1":
            dbLib.userplaylogs_gamefinish(callback.from_user.id, "WinPlayer")
            await callback.message.answer("Ты победил!")
            await callback.message.answer("Хочешь сыграть ещё раз? Нажми Начать игру в меню!", reply_markup=None)
        elif gameResult == "P2":
            dbLib.userplaylogs_gamefinish(callback.from_user.id, "WinBot")
            await callback.message.answer("Победил геймбот!")
            await callback.message.answer("Хочешь сыграть ещё раз? Нажми Начать игру в меню!", reply_markup=None)

#Метод формирования структуры главного меню (ReplyKeyboard)
def getMainMenu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Камень ножницы бумага")], 
            [KeyboardButton(text="21 спичка")],
        ],
        resize_keyboard=True,  # Автоматическое изменение размера
        input_field_placeholder="Выберите игру...",  # Подсказка в поле ввода
        selective=True,  # ← Ключевой параметр для iOS
        is_persistent=True,  # ← стараться сохранять
        one_time_keyboard=False #скрывает кнопку после использования пользователем???
    )
    return keyboard


#Метод формирования структуры меню игры (ReplyKeyboard)
def getGameMenu(game_name: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Начать игру")],
            [KeyboardButton(text="📜 Правила игры")],
            [KeyboardButton(text="⬅️ Вернуться в главное меню")]
        ],
        resize_keyboard=True,  # Автоматическое изменение размера
        input_field_placeholder=f"Игра: {game_name}",  # Подсказка в поле ввода
        selective=True,  # ← Ключевой параметр для iOS
        is_persistent=True,  # ← стараться сохранять
        one_time_keyboard=False #скрывает кнопку после использования пользователем
    )
    return keyboard


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
