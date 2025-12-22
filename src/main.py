from pygame import Color, Surface, SRCALPHA

from engine.Object import Object
from engine.Percent import Percent

from game.Game import Game
from game.menu import *
from game.Utils import *
from game.levels.Level import Level, loadLevels
from game.objects import *

game: Game = Game()
mainMenu: MainMenu = MainMenu(game)

game.setToRun(mainMenu.run)