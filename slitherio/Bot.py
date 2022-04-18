from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import perf_counter

class Bot:
    def __init__(self, game, username):
        self.game = game
        self.actions = ActionChains(game.driver)
        self.actions_timer = {
            'right': None,
            'left': None,
            'turbo': None
        }

        self.username = username

    def turn_right(self, seconds):
        self.actions.key_down(Keys.ARROW_RIGHT)
        self.actions_timer['right'] = [perf_counter(), seconds]

    def turn_left(self, seconds):
        self.actions.key_down(Keys.ARROW_LEFT)
        self.actions_timer['left'] = [perf_counter(), seconds]

    def turbo(self, seconds):
        self.actions_timer['turbo'] = [perf_counter(), seconds]
        
        
    def logic(self):
        pass

    def update(self):
        for action, timer in self.actions_timer.items():
            if timer is not None:
                if perf_counter() - timer[0] < timer[1]:
                    if action == 'turbo':
                        if self.game.score in (10, 11):
                            self.actions.key_up(Keys.ARROW_UP)
                        else:
                            self.actions.key_down(Keys.ARROW_UP)
                else:
                    self.actions_timer[action] = None

                    if action == 'right':
                        self.actions.key_up(Keys.ARROW_RIGHT)
                    elif action == 'left':
                        self.actions.key_up(Keys.ARROW_LEFT)
                    else:  
                        self.actions.key_up(Keys.ARROW_UP)
        self.actions.perform()

        self.logic()