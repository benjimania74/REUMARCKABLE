import pygame
from pygame import Color
from typing import Any

from game.Game import Game
from game.levels.Level import Level
from game.Utils import Percent, FRAME_WIDTH, FRAME_HEIGHT
from game.Menu import *
from game.objects import *

from engine.Object import *


class Tutorial(Level):
    menu: Menu|None

    def __init__(self, mainMenu: Menu, game: Game) -> None:
        super().__init__(mainMenu, game)
        self.name = "Tutoriel" # override du nom par défaut
        
    def load(self) -> None:
        self.menu = None
        game: Game = self.game
        colliders:list[Collideable] = []

        rectangleCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,Color|None] ] = [
            (0,200,FRAME_WIDTH//2 - 100,50,51,True,Color(0,255,0)), # sol principal
            (FRAME_WIDTH // 2 - 100, 180, FRAME_WIDTH // 2 + 100, 50, 51, True, Color(0,255,0)), # plateforme basse
            (Percent(50), 280, FRAME_WIDTH // 4, 50, 51, True, Color(50, 230, 65)), # plateforme haut
            (0, 0, 0, FRAME_HEIGHT, 100, True, None), # mur écran gauche
            (FRAME_WIDTH, 0, 0, FRAME_HEIGHT, 100, True, None) # mur écran droit
        ]
        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, game.getScreen()) )

        p: Player = Player(0,400, 50, 50, "background.jpg", colliders, game.getScreen())
        phantom: PhantomPlayer = PhantomPlayer(0, 350, 50, 50, Color(0,0,255), colliders, game.getScreen())
        colliders.append(p)
        colliders.append(phantom)

        end: PlayerDetectorCollider = PlayerDetectorCollider(1000, 320, 50, 50, 51, True, Color(0,255,0), p, game.getScreen())
        colliders.append(end)
        self.end = end

        toDisplay: list[Object] = []
        toDisplay += colliders

        endText: DynamicText = DynamicText(
            -1,
            -1,
            400,
            400,
            "",
            None,
            32,
            Color(0,0,0),
            None,
            game.getScreen()
        )

        toDisplay.append(endText)

        self.endText = endText

        actuators: list[ActuatorCollider] = []
        actuators.append(
            ActuatorCollider(150,260, 20,10, end,"", game.getScreen())
        )

        toDisplay += actuators

        self.toDisplay = toDisplay
        self.colliders = colliders
        self.actuators = actuators

        self.activePlayer = p
        self.p = p
        self.phantom = phantom

        self.game = game
    
    def closeMenu(self, button: TextButton|None=None):
        self.menu = None
    def quit(self, button: TextButton):
        self.game.getScreen().fill("black")
        self.game.setToRun(self.mainMenu.run)

    def update(self) -> None:
        activePlayer: Player = self.activePlayer
        p: Player = self.p
        phantom: PhantomPlayer = self.phantom
        actuators: list[ActuatorCollider] = self.actuators

        keyPressedMap = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.menu != None:
                    if event.dict["unicode"] == "\x1b":
                        self.closeMenu()
                else:
                    if event.dict["unicode"] in ["v", "V"]:
                        if activePlayer == p:
                            if phantom.canSetActive():
                                self.activePlayer = phantom
                                p.switchActive()
                                phantom.switchActive()
                        else:
                            self.activePlayer = p
                            p.switchActive()
                            phantom.switchActive()
                    elif event.dict["unicode"] in ["e", "E"]:
                        i = 0
                        stop = False
                        while i < len(actuators) and not stop:
                            if actuators[i].isColliding(activePlayer):
                                actuators[i].actuate()
                                stop = True
                            i += 1
                    elif event.dict["unicode"] == "\x1b": # echap
                        menu = Menu()
                        menu.add(
                            #Rectangle(0,0, FRAME_WIDTH, FRAME_HEIGHT, Color(0,0,255, 25), game.getScreen()),
                            TextButton(-1,-1,200,100, "Continuer", None, 32,None, Color(0,255,0), self.closeMenu, self.game.getScreen()),
                            TextButton(-1, 100, 200, 100, "Quitter", None, 32, None, Color(0,255,0), self.quit, self.game.getScreen())
                        )
                        self.menu = menu
            if event.type == pygame.MOUSEBUTTONDOWN and self.menu != None:
                self.menu.handleClick(event, self.game)

        if self.menu == None:
            if keyPressedMap[pygame.K_d]:
                activePlayer.xMove += 5
            if keyPressedMap[pygame.K_q]:
                activePlayer.xMove -= 5
            if keyPressedMap[pygame.K_SPACE]:
                activePlayer.jump()
            p.update()
            phantom.update()

    def show(self) -> None:
        self.game.getScreen().fill("white")

        if self.end.collidePlayer():
            self.endText.setText("Bravo !")
        else:
            self.endText.setText("")
        
        for o in self.toDisplay:
            o.show()
        self.activePlayer.showAt(0,0)
        
        if self.menu != None:
            self.menu.show()
            self.menu.run(self.game)

export: dict[str,Any] = {
    "class_name": Tutorial.__qualname__
}