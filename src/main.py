from pygame import Color, Surface, SRCALPHA

from engine.Object import Object
from engine.Percent import Percent

from game.Game import Game
from game.menu import *
from game.Utils import toPygameY, calcPercent, FRAME_WIDTH, FRAME_HEIGHT
from game.levels.Level import Level, loadLevels
from game.objects import *

game: Game = Game()
mainMenu: Menu = Menu()

levels: list[Level] = loadLevels(mainMenu, game)


def startGame(btn: TextButton):
    levelMenu: Menu = Menu()
    levelMenuContent: list[Object] = [
        Rectangle(0,0,-1,-1, Color(255,255,255), gameScreen)
    ]
    i: int = 0
    width: int = FRAME_WIDTH // 5
    height: int = FRAME_HEIGHT // 5
    
    while i < len(levels):
        level = levels[i]
        x: int = 10 + i * width
        y: int = FRAME_HEIGHT - 10 + (i - 1) * height

        def setActive(bnt: TextButton):
            level.setActive()
        card: TextButton = TextButton(x, y, width, height, level.name, None, 100, None, Color(100,25,171, 100), setActive, gameScreen)
        levelMenuContent.append(card)
        i += 1

    levelMenu.add(*levelMenuContent)
    game.setToRun(levelMenu.run)
    
def stopGame(btn: TextButton):
    game.stop()

gameScreen = game.getScreen()
objs: list[Object] = [
    Rectangle(-1,0,Percent(50),-1, Color(255,0,255), gameScreen),
    StaticText(0,0,0,0,"Reumarckable",None,32,Color(255,0,0),None,gameScreen),
    TextButton(-1,-1,300,80, "Jouer", None, 100, Color(0,255,0), Color(255,0,0), startGame, gameScreen),
    TextButton(-1, 100, 300, 80, "Quitter", None, 100, Color(0,255,0), Color(255,0,0), stopGame, gameScreen),
]
mainMenu.add(*objs)
game.setToRun(mainMenu.run)