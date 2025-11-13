from __future__ import annotations

from abc import ABC, abstractmethod

from game.Game import Game
from game.Menu import Menu
from game.Utils import LEVEL_DIRECTORY

from os.path import isfile
from importlib import import_module

class Level(ABC):
    name: str
    game: Game
    mainMenu: Menu

    def __init__(self, name: str, mainMenu: Menu, game: Game) -> None:
        self.name = name
        self.game = game
        self.mainMenu = mainMenu

    @abstractmethod
    def load(self) -> None:
        pass
    @abstractmethod
    def update(self) -> None:
        pass
    @abstractmethod
    def show(self) -> None:
        pass

    def setActive(self) -> None:
        self.game.setToRun(self.loop)

    def loop(self, game: Game) -> None:
        self.update()
        self.show()
    


def loadLevel(id:int, mainMenu: Menu, game: Game) -> Level|None:
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
    res: Level|None = None
    try:
        export = getattr(module, "export") # on récupère la variable "export" définie dans le fichier
        level_class_name = export.get("class_name", None)
        if level_class_name != None: # on connait la classe du niveau
            level_class = getattr(module, level_class_name) # on récupère la classe du niveau
            if issubclass(level_class, Level): # si on a bien à faire à un niveau
                level = level_class( mainMenu, game )  # les niveaux, dans leurs fichiers, utilise un autre constructeur, mais Python ne nous laisse pas en faire plusieurs :(
                level.load()
                res = level
    except:
        pass   # si le module n'est pas un niveau, on retourne juste None
    return res