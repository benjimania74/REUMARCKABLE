import pygame
from pygame import Color, Surface, SRCALPHA

from engine.Object import Collideable, Object
from engine.Percent import Percent

from game.Game import Game
from game.Colliders import RectangleCollider, PlayerDetectorCollider, ActuatorCollider
from game.Player import Player
from game.PhantomPlayer import PhantomPlayer
from game.Image import Image
from game.Text import DynamicText, StaticText
from game.Utils import FRAME_WIDTH, FRAME_HEIGHT
from game.Menu import Menu
from game.Button import TextButton
from game.Utils import toPygameY, calcPercent
from game.levels.Level import loadLevel

class Rectangle(Object):
    toDraw: Surface
    drawSurface: Surface

    def __init__(self, x:int|Percent, y:int|Percent, width:int|Percent, height:int|Percent, color:Color, drawSurface: Surface) -> None:
        drawSurfaceWidth: int = drawSurface.get_width()
        drawSurfaceHeight: int = drawSurface.get_height()

        self.width = calcPercent(width, drawSurfaceWidth, drawSurfaceWidth)
        self.height = calcPercent(height, drawSurfaceHeight, drawSurfaceHeight)

        self.x = calcPercent(x, drawSurfaceWidth // 2 - self.width // 2, drawSurfaceWidth)
        self.y = calcPercent(y, drawSurfaceHeight // 2 - self.height // 2, drawSurfaceHeight)

        self.drawSurface = drawSurface

        self.toDraw = Surface((self.width, self.height), flags=SRCALPHA)
        self.toDraw.fill(color)

    def show(self):
        self.drawSurface.blit(
            self.toDraw,
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurface.get_height())
            )
        )

game: Game = Game()
mainMenu: Menu = Menu()

def startGame(btn: TextButton):
    tuto = loadLevel(1, mainMenu, game)
    if tuto != None:
        tuto.setActive()
    
def stopGame(btn: TextButton):
    game.stop()

gameScreen = game.getScreen()
objs: list[Object] = [
    Rectangle(-1,0,Percent(50),-1, Color(255,0,255), gameScreen),
    StaticText(0,0,0,0,"Reumarckable",None,32,Color(255,0,0),None,gameScreen),
    TextButton(-1,-1,300,80, "Jouer", None, 100, Color(0,255,0), Color(255,0,0), gameScreen, startGame),
    TextButton(-1, 100, 300, 80, "Quitter", None, 100, Color(0,255,0), Color(255,0,0), gameScreen, stopGame),
]
mainMenu.add(*objs)
game.setToRun(mainMenu.run)