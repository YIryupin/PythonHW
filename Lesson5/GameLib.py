import random

class RPSGame():
    #Варинты выбора игрока
    __gameChoice = ["Камень", "Ножницы", "Бумага"]
    #Матрица выбора победителя: P1 - первый игрок P2 - второй игрок N - ничья
    __gameDesition = [["N","P1","P2"],
                      ["P2","N","P1"],
                      ["P1","P2","N"]]

    helpText = '''Правила игры Камень Ножницы Бумага: 
               2 игрока выбирают Камень Ножницы или Бумагу, 
               «Камень» побеждает ножницы («камень ломает ножницы»), 
               «Бумага» побеждает камень («бумага накрывает камень»), 
               «Ножницы» побеждают бумагу («ножницы разрезают бумагу»)''' 

    #Метод определения победителя
    def gameResult(self, Player1Choice: str, Player2Choice: str):
        return self.__gameDesition[self.__gameChoice.index(Player1Choice)][self.__gameChoice.index(Player2Choice)]

    #Метод случайного выбора победителя
    def botChoice(self):
        number = random.randint(0, 2)
        return self.__gameChoice[number]
    
    def getHelp(self):
        return self.helpText

    
#game = RPSGame()
#print(game.gameResult("Бумага", "Камень"))
#print(game.botChoice())
#print(game.botChoice())
#print(game.botChoice())