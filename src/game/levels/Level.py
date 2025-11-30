from __future__ import annotations
from typing import Any

import pygame

from abc import ABC, abstractmethod

from game.Game import Game
from game.menu import *
from game.objects import *
from game.Utils import LEVEL_DIRECTORY, FRAME_HEIGHT, FRAME_WIDTH

from os import listdir
from os.path import isfile
from importlib import import_module

class Level(ABC, Activated):
    name: str

    player: Player
    phantom: PhantomPlayer
    activePlayer: Player

    colliders: list[Collideable]
    content: list[Object]
    actuators: list[ActuatorCollider]

    menu: Menu|None # pause, ou autre
    game: Game
    mainMenu: Menu # accueil

    def __init__(self, mainMenu: Menu, game: Game, name: str|None = None) -> None:
        self.name = self.__class__.__qualname__ if name == None else name # si aucun nom n'est donné, on donne celui de la classe
        self.game = game
        self.mainMenu = mainMenu

        self.initContent()
    
    def initContent(self):
        self.colliders = [
            RectangleCollider(0, 0, 0, FRAME_HEIGHT, 100, True, None, self.game.getScreen()), # mur écran gauche
            RectangleCollider(FRAME_WIDTH, 0, 0, FRAME_HEIGHT, 100, True, None, self.game.getScreen()) # mur écran droite
        ]
        self.content = []
        self.actuators = []
        self.menu = None
        
    @abstractmethod
    def load(self) -> None:
        """Permet de charger le niveau."""
        pass

    def reload(self, btn: TextButton|None=None) -> None:
        """Permet de recharger le niveau."""
        self.initContent()
        self.load()

    def update(self) -> None:
        """Permet de mettre à jour chacun des objets contenues dans le niveau"""
        self.handleKeys()
        if self.menu == None:
            for obj in self.content:
                obj.update()
    
    def show(self) -> None:
        """Permet d'afficher le niveau"""
        self.game.getScreen().fill("white")
        for o in self.content:
            o.show()
        phantom: PhantomPlayer = self.phantom

        showWidth: int = phantom.width * 2
        showHeight: int = phantom.height * 2

        showX: int = FRAME_WIDTH - showWidth - 10
        showY: int = 10

        phantom.showAtSize(FRAME_WIDTH - showWidth - 10, 10, showWidth, showHeight)
        
        if not phantom.isActive and not phantom.canSetActive():
            Image(showX - 5, showY - 5, showWidth + 10, showHeight + 10, "cross.png", self.game.getScreen()).show()
        
        if self.menu != None:
            self.menu.show()
            self.menu.run(self.game)

    def setActive(self) -> None:
        """Met le niveau en actif, c'est lui qui prend le contrôle"""
        self.game.setToRun(self.loop)

    def setMenu(self, menu: Menu):
        """Définie et affiche un menu"""
        self.menu = menu
    
    def closeMenu(self, btn: TextButton|None = None):
        """Ferme le menu ouvert"""
        self.menu = None

    def pauseGame(self):
        """Ouvre le menu de pause"""
        gameScreen: Surface = self.game.getScreen()
        buttonColor: Color = Color(0,255,0)

        buttons: list[ tuple[str,Callable[[TextButton], None]] ] = [
            ("Continuer", self.closeMenu),
            ("Recommencer", self.reload),
            ("Quitter", self.quitLevel)
        ]
        buttonWidth: int = 200
        buttonHeight: int = 100
        verticalGap: int = 50

        verticalUsedSpace: int = len(buttons) * (buttonHeight + verticalGap) - verticalGap
        yPos: int = FRAME_HEIGHT // 2 + verticalUsedSpace // 2 - buttonHeight # -buttonHeight car le calcul avant donne le haut de la boîte complète mais que le bouton à ses coordonnées en bas à gauche

        menu: Menu = Menu()
        for btn in buttons:
            menu.add(
                TextButton(-1, yPos, buttonWidth, buttonHeight, btn[0], None, 1000, None, buttonColor, btn[1], gameScreen)
            )
            yPos -= buttonHeight + verticalGap
        
        self.setMenu(menu)

    def quitLevel(self, btn: TextButton|None = None):
        """Quitte le niveau"""
        self.game.setToRun(self.mainMenu.run)

    def restart(self, btn: TextButton|None = None):
        """Redémarre le niveau"""
        self.reload()
    
    def onActuated(self, data: dict[str, Any] | None = None) -> None:
        if data != None and data.get("type", None) == EndGamePlayerDetectorCollider.__qualname__ and data.get("status", None) == "activated":
            endMenu: Menu = Menu()
            endMenu.add(
                TextButton(-1, Percent(52), Percent(80), Percent(28), "Recommencer", None, 1000, None, Color(205,205,10), self.restart, self.game.getScreen()),
                TextButton(-1, Percent(20), Percent(80), Percent(28), "Quitter", None, 1000, None, Color(205,205,10), self.quitLevel, self.game.getScreen())
            )
            self.setMenu(endMenu)

    def handleKeys(self):
        """Gère les touches pressées"""
        p = self.player
        phantom = self.phantom
        activePlayer = self.activePlayer

        actuators = self.actuators

        keyPressedMap = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: # touche pressé (ne compte pas le maintient)
                if self.menu != None: # si on est dans un menu
                    if event.dict["unicode"] == "\x1b": # Esc
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
                            if actuators[i].isColliding(activePlayer): # si il touche un actionneur
                                actuators[i].actuate() # on actionne l'actionneur
                                stop = True
                            i += 1
                    elif event.dict["unicode"] == "\x1b": # Esc
                        self.pauseGame()
            if event.type == pygame.MOUSEBUTTONDOWN and self.menu != None:
                self.menu.handleClick(event, self.game)

        if self.menu == None:
            if keyPressedMap[pygame.K_d]:
                activePlayer.xMove += 5
            if keyPressedMap[pygame.K_q]:
                activePlayer.xMove -= 5
            if keyPressedMap[pygame.K_SPACE]:
                activePlayer.jump()
    
    def loop(self, game: Game) -> None:
        """Boucle du niveau"""
        self.update()
        self.show()

def loadLevel(id:int, mainMenu: Menu, game: Game) -> Level|None:
    """Charge un niveau dynamiqument à partir de son identifiant"""
    res: Level|None = None
    if isfile(LEVEL_DIRECTORY + "level" + str(id) + ".py"):
        module = import_module( # on charge dynamiquement le fichier comme un module dans le même dossier
            __name__.replace(
                "." + Level.__qualname__, # __qualname__ => nom écrit de la classe donc là "Level"
                ".level" + str(id)
            )
        )
        res = loadLevelFromModule(module, mainMenu, game)
    return res

def loadLevelFromModule(module, mainMenu: Menu, game: Game) -> Level|None:
    """Charge un niveau depuis un module"""
    res: Level|None = None
    try:
        export = getattr(module, "export") # on récupère la variable "export" définie dans le fichier
        level_class_name = export.get("class_name", None)
        if level_class_name != None: # on connait la classe du niveau
            level_class = getattr(module, level_class_name) # on récupère la classe du niveau
            if issubclass(level_class, Level): # si on a bien à faire à un niveau
                level = level_class( mainMenu, game )  # on instancie le niveau
                level.load()
                res = level
    except:
        pass   # si le module n'est pas un niveau, on retourne juste None
    return res

def loadLevels(mainMenu: Menu, game: Game) -> list[Level]:
    """Charge les niveaux dynamiquement"""
    res: list[Level] = []

    levelFiles: list[str] = [f for f in listdir(LEVEL_DIRECTORY) if isfile(LEVEL_DIRECTORY + f) if f.endswith(".py") and f not in ["Level.py", "__init__.py"]]
    levelFiles.reverse()

    for levelFile in levelFiles:
        module = import_module(
            __name__.replace(
                "." + Level.__qualname__,
                "." + levelFile[:-3]
            )
        )
        level = loadLevelFromModule(module, mainMenu, game)
        if level != None:
            res.append(level)
    return res