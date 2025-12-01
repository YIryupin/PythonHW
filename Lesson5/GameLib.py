import random

class RPSGame():
    gameChoice = ["Камень", "Ножницы", "Бумага"]
    gameDesition = [["N","P1","P2"],
                    ["P2","N","P1"],
                    ["P1","P2","N"]]
        
    def gameResult(self, Player1Choice: str, Player2Choice: str):
        return self.gameDesition[self.gameChoice.index(Player1Choice)][self.gameChoice.index(Player2Choice)]

    def botChoice(self):
        number = random.randint(0, 2)
        return self.gameChoice[number]
    
#game = RPSGame()
#print(game.gameResult("Бумага", "Камень"))
#print(game.botChoice())
#print(game.botChoice())
#print(game.botChoice())