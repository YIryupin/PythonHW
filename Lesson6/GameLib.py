import random
import math

class RPSGame():
    #Варинты выбора игрока
    __gameChoice = ["Камень", "Ножницы", "Бумага"]
    #Матрица выбора победителя: P1 - первый игрок P2 - второй игрок N - ничья
    __gameDesition = [["N","P1","P2"],
                      ["P2","N","P1"],
                      ["P1","P2","N"]]

    HELP_TEXT = '''Правила игры Камень Ножницы Бумага: 
               2 игрока выбирают Камень Ножницы или Бумагу, 
               «Камень» побеждает ножницы («камень ломает ножницы»), 
               «Бумага» побеждает камень («бумага накрывает камень»), 
               «Ножницы» побеждают бумагу («ножницы разрезают бумагу»)''' 

    #Метод определения победителя
    def gameResult(self, Player1Choice: str, Player2Choice: str):
        return self.__gameDesition[self.__gameChoice.index(Player1Choice)][self.__gameChoice.index(Player2Choice)]

    #Метод случайного выбора бота
    def botChoice(self):
        number = random.randint(0, 2)
        return self.__gameChoice[number]
    
    @staticmethod
    def getHelp():
        return RPSGame.HELP_TEXT

    
#game = RPSGame()
#print(game.gameResult("Бумага", "Камень"))
#print(game.botChoice())
#print(game.botChoice())
#print(game.botChoice())

class Matches21Game():
    #Варинты выбора игрока
    __gameChoice = ["1", "2", "3", "4"]

    HELP_TEXT = '''Правила игры 21 спичка: 
               на кону 21 списчка
               2 игрока по очереди берут от 1 до 4 спичек,
               побеждает игрок взявший последние спички''' 

    def __init__(self, matchesCounter: int, player1Choice: int):
        self.MatchesCounter = matchesCounter
        self.Player1Choice = player1Choice
    def botChoice(self) -> int:
        rightRemain = (math.floor((self.MatchesCounter - self.Player1Choice) / 5))*5
        #Правильный выбор бота - всегда оставлять кол-во кратно 5
        botChoice = (self.MatchesCounter - self.Player1Choice) - rightRemain
        if ((self.MatchesCounter - self.Player1Choice) == 0): #Если Player1 забрал все спички, то бот ничего не забирает
            return 0
        elif (rightRemain == 0): #Если осталось менее 4х спичек, то бот забиарает всё что осталось
            return (self.MatchesCounter - self.Player1Choice)
        elif (botChoice == 0): #Если Player1 оставил кол-во спичек равное 5, то выбор бота случаен
            return random.randint(1, 4)
        return botChoice
    #Метод определения победителя
    def gameResult(self, Player2Choice: int) -> str:
        if ((self.MatchesCounter - self.Player1Choice) == 0):
            return "P1"
        elif ((self.MatchesCounter - self.Player1Choice - Player2Choice) == 0):
            return "P2"
        return "Continue"
    
    @staticmethod
    def getHelp():
        return Matches21Game.HELP_TEXT

# game = Matches21Game(3,3)
# bch = game.botChoice()
# print(bch)
# print(game.gameResult(bch))    