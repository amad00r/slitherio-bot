from slitherio.Slitherio import Slitherio
from slitherio.Bot import Bot
from slitherio.Actions import *

from random import random


class SillyBot(Bot):
    def setup(self):
        self.act(TURBO, 10)

    def loop(self):
        choice = random()
        if choice < 0.025:
            self.act(TURN_RIGHT, INDEFINITELY)
            self.stop_action(TURN_LEFT)
        elif choice < 0.05:
            self.act(TURN_LEFT, INDEFINITELY)
            self.stop_action(TURN_RIGHT)
        if self.score > 50:
            self.act(TURBO, 10)
        elif self.score < 30:
            self.stop_action(TURBO)


slitherio = Slitherio(
    bot=SillyBot,
    username='worm',
    headless=False,
    maximize=False
    )


for i in range(2):
    slitherio.new_game()

    while slitherio.running():
        slitherio.update()

slitherio.close()