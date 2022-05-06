from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import perf_counter

from slitherio.Actions import *


class Bot:
    """Interactuates with Slitherio class.

    Parameters
    ----------
    driver : selenium.webdriver.firefox.webdriver.WebDriver
        Contains the driver where the game is being played. Slitherio automatically passes it.
    score : int
        Integer value representing the score you have in the game. Slitherio passes it to this class when 
        instancing it.

    Attributes
    ----------
    score : int
        Stores an integer greater or equal than 10 (the minimum score you can have in slither.io which 
        represents in real time the score you have in the game. It is automatically updated by Slitherio.
    action_queue : selenium.webdriver.common.action_chains.ActionChains
        Contains an instance of ActionChains. It will be used as a queue of keyboard inputs.
    action_timer : dict
        This is a dictionary that contains three keys, one for each action the bot can take:
        'turn_right', 'turn_left' and 'turbo'. Their default value is None. 
        When an action is performed by the bot, a list of two items is assigned to its key. The first 
        value of the list is the moment that the bot added the action to the actions object, and the 
        second value is the time, in seconds, that the action is meant to last.
        The value of an action can also be indefinitely, in which case it will last indefinitely until
        either stop_action(action) or stop_actions() are called.
    """

    def __init__(self, driver, score):
        self.score = score
        self.action_queue = ActionChains(driver)
        self.action_timer = {
            TURN_RIGHT: None,
            TURN_LEFT: None,
            TURBO: None
        }

        self.setup()

    def setup(self):
        """Setup code of the bot.
        
        Inspired in Arduino. The code inside this method will be executed when an instance of the Bot is 
        created. When implementing the Bot class in your project, you can add content to this method using 
        a child of this class or using a decorator in an instance of the class.
        """
        ...

    def loop(self):
        """Main loop of the bot.
        
        Inspired in Arduino. The code inside this method will be executed every time the update 
        method is called. When implementing the Bot class in your project, you can add content 
        to this method using a child of this class or using a decorator in an instance of the class.
        """
        ...

    def act(self, action, time):
        """Makes the worm act.

        Adds the specified keyboard key_down input in the parameters as an action to the action_queue object. 
        Then, it registers in the action_timer dict the time that it will be running.

        Parameters
        ----------
        action : {'turn_right', 'turn_left', 'turbo'}
            Specifies the action (keyboard input) that the bot will perform.
        time : {float, 'indefinitely'}
            It represents the time that the given action is meant to last.
            If it is a float, it is assigned to the action_timer corresponding key together with the
            current time.
            If it is a str with value 'indefinitely', it will be assigned to the action_timer corresponding 
            acion. It indicates that the action won't stop unless it is manually stopped.
        """

        timer = INDEFINITELY if time == INDEFINITELY else [perf_counter(), time]

        if action == TURN_RIGHT:
            self.action_queue.key_down(Keys.ARROW_RIGHT)
            self.action_timer[TURN_RIGHT] = timer
        elif action == TURN_LEFT:
            self.action_queue.key_down(Keys.ARROW_LEFT)
            self.action_timer[TURN_LEFT] = timer
        elif action == TURBO:
            self.action_timer[TURBO] = timer
        self.action_queue.perform()
        
    def stop_action(self, action):
        """Stops a given action that the worm is performing.

        Assigns None to the action_timer corresponding action and adds the specified keyboard key_up input
        in the parameters to the action_queue object.

        Parameters
        ----------
        action : {'turn_right', 'turn_left', 'turbo'}
            Specifies the action (keyboard input) that the bot will stop performing.
        """

        if action == TURN_RIGHT:
            self.action_timer[action] = None
            self.action_queue.key_up(Keys.ARROW_RIGHT)
        elif action == TURN_LEFT:
            self.action_timer[action] = None
            self.action_queue.key_up(Keys.ARROW_LEFT)
        elif action == TURBO:
            self.action_timer[action] = None
            self.action_queue.key_up(Keys.ARROW_UP)
        self.action_queue.perform()

    def stop_actions(self):
        """Stops all actions that the worm is performing.

        Assigns None to the action_timer corresponding action and adds the specified keyboard key_up input
        in the parameters to the action_queue object.
        """

        for action, timer in self.action_timer.items():
            if timer is not None:
                self.action_timer[action] = None
                if action == TURN_RIGHT:
                    self.action_queue.key_up(Keys.ARROW_RIGHT)
                elif action == TURN_LEFT:
                    self.action_queue.key_up(Keys.ARROW_LEFT)
                elif action == TURBO:
                    self.action_queue.key_up(Keys.ARROW_UP)
        self.action_queue.perform()

    def update(self):
        """Updates de action_timer dict, performs actions and calls the loop method.

        Iterates the action_timer dict keys. If the value is not None, calculates if the difference between the 
        current time and the start time of the action is lower than the time that the action is meant to last.
        """

        for action, timer in self.action_timer.items():
            if timer is not None:
                if timer == INDEFINITELY or perf_counter() - timer[0] < timer[1]:
                    if action == TURBO:
                        if self.score in (10, 11):
                            self.action_queue.key_up(Keys.ARROW_UP)
                        else:
                            self.action_queue.key_down(Keys.ARROW_UP)
                else:
                    self.action_timer[action] = None

                    if action == TURN_RIGHT:
                        self.action_queue.key_up(Keys.ARROW_RIGHT)
                    elif action == TURN_LEFT:
                        self.action_queue.key_up(Keys.ARROW_LEFT)
                    else:  
                        self.action_queue.key_up(Keys.ARROW_UP)
        self.action_queue.perform()

        self.loop()