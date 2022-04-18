from slitherio.Slitherio import Slitherio
from slitherio.Bot import Bot



class SillyBot(Bot):
    def __init__(self, game, username):
        super().__init__(game, username)
        
        self.turbo(30)

    def logic(self):
        self.turn_left(0.1)



game = Slitherio(
    maximize=False,
    headless=False
    )

bot = SillyBot(
    game=game,
    username='username',
    )

for i in range(2):
    game.new_game(username=bot.username)

    while game.running():
        game.update()
        bot.update()

game.close()