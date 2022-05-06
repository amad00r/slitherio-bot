from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class Slitherio:
    """Handles the slither.io game using Selenium.

    Parameters
    ----------
    bot : slitherio.Bot.Bot
        Specifies the bot that will be used to play slither.io. It can either be the class
        slitherio.Bot.Bot or a child of it.
    username : str, optional
        Specifies the username. It will be visible in the game.
    headless : bool, default=False
        Specifies whether Selenium will run as a window or as a background process.
    maximize : bool, default=False
        Specifies whether the selenium window will maximize when opening or not.

    Attributes
    ----------
    bot : slitherio.Bot.Bot
        Contains a pointer to the bot that will be used to play slither.io. An instance of it
        will be created every time a new game is started. It can either be the class slitherio.Bot.Bot 
        or a child of it.
    bot_instance : slitherio.Bot.Bot
        Will contain the instances created of the bot.
    username : str
        Contains the username. It will be visible in the game.
    driver : selenium.webdriver.firefox.webdriver.WebDriver
        Contains a Selenium class which will handle the connection 
        between python and the Mozilla Firefox geckodriver.exe.
    score : int
        Stores an integer greater or equal than 10 (the minimum score you can have 
        in slither.io) which represents in real time the score you have in the game.
    """

    def __init__(self, bot, username=None, headless=False, maximize=False):
        self.bot = bot
        self.bot_instance = None

        if isinstance(username, str):
            self.username = username
        else:
            self.username = None

        if headless:
            options = Options()
            options.add_argument('--headless')
        else:
            options = None

        self.driver = webdriver.Firefox(options=options, service=Service(Path('slitherio/driver/geckodriver.exe').resolve()))

        if maximize:
            self.driver.maximize_window()

        self.driver.get('http://slither.io/')

        self.score = 10

    def new_game(self):
        """Starts a new slither.io game.

        It waits to act until it detects the html textbox called 'nick' to avoid issues when a game is 
        finishing. 
        
        If self.username is not None, it clears the textbox, writes the new username, and clicks the start 
        button. 
        
        When the game is starting, it waits until it detects the small minimap located on the bottom-right 
        corner to avoid any issues when the game is starting. 
        
        In the end, an instance of the specified bot class is created to start playing the game.
        """

        self.score = 10
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'nick')))
        if self.username is not None:
            self.driver.find_element(By.ID, 'nick').clear()
            self.driver.find_element(By.ID, 'nick').send_keys(self.username)
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div/div/div[3]').click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[15]/canvas')))
        sleep(0.5)
        self.bot_instance = self.bot(self.driver, self.score)

    def running(self):
        """Checks if the worm is dead or still alive.

        Returns
        -------
        bool
            True if it finds the minimap, False otherwise.
        """

        return self.driver.find_element(By.XPATH, '/html/body/div[15]/canvas').is_displayed()

    def update(self):
        """Updates the game and bot_instance info.

        It gets the score in plain text from the html span located on the bottom-left corner and converts
        it to an integer.

        ( The (try, except, pass) structure is not recommended in many cases. In this specific case, however,
        it is OK to use it because I'm already aware that it may sometimes fail to get the score due to the
        refresh of the html span, and it is not necessary to get noticed when it happens. )
        """

        try:
            self.score = int(self.driver.find_element(By.XPATH, '/html/body/div[13]/span[1]/span[2]').text)
        except:
            ...

        self.bot_instance.score = self.score
        self.bot_instance.update()

    def close(self):
        """Quits the driver and closes its window."""
        self.driver.quit()