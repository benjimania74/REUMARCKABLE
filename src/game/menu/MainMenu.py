from .Menu import *
from ..objects.text import *
from ..objects.button import *
from ..objects import Rectangle
from ..Utils import *
from ..levels import *

class MainMenu(Menu):
    menuSelect: bool
    game: Game

    def __init__(self, game:Game) -> None:
        self.menuSelect = False
        super().__init__()
        
        gameScreen: Surface = game.getScreen()
        self.game = game
        objs: list[Object] = [
            Rectangle(-1,0,-1,-1, Color(255,255,255), gameScreen),
            StaticText(0,0,0,0,"Reumarckable",None,32,Color(255,0,0),None,gameScreen),
            TextButton(-1, FRAME_HEIGHT // 2 + 10, 300, 80, "Jouer", None, 100, MENU_BUTTON_TEXT_COLOR, MENU_BUTTON_COLOR, self.startGame, gameScreen),
            TextButton(-1, FRAME_HEIGHT // 2 - 90, 300, 80, "Quitter", None, 100, MENU_BUTTON_TEXT_COLOR, MENU_BUTTON_COLOR, self.stopGame, gameScreen),
        ]
        self.add(*objs)
    
    def run(self, game:Game):
        if self.menuSelect:
            self.startGame()
        else:
            super().run(game)
    
    def stopGame(self, btn: TextButton|None=None):
        self.game.stop()

    def startGame(self, btn: TextButton|None=None):
        game: Game = self.game
        gameScreen: Surface = game.getScreen()
        
        levels: list[Level] = loadLevels(self, game)

        levelMenu: Menu = Menu()
        levelMenuContent: list[Object] = [
            Rectangle(0,0,-1,-1, Color(255,255,255), gameScreen)
        ]
        i: int = 0
        width: int = calcPercent(Percent(18.), FRAME_WIDTH, FRAME_WIDTH)
        height: int = calcPercent(Percent(18.), FRAME_HEIGHT, FRAME_HEIGHT)

        horizontalTagNumber: int = FRAME_WIDTH // width
        linesNumber: int = FRAME_HEIGHT // height
        # calculs des espaces entre les boutons de niveaux
        # taille complète moins espace occupé divisé par nombre d'espace vide
        widthGap: int = ( FRAME_WIDTH - horizontalTagNumber * width ) // (horizontalTagNumber + 1)
        heightGap: int = ( FRAME_HEIGHT - linesNumber * height ) // (linesNumber + 1)

        while i < len(levels):
            level = levels[i]
            x: int = widthGap + (i % horizontalTagNumber) * ( widthGap + width )
            y: int = FRAME_HEIGHT - (heightGap + height) * (i // horizontalTagNumber + 1)

            def setActive(i: int) -> Callable[[TextButton], None]: # fonction car sinon ça modifie la fonction f à chaque boucle au lieu d'en créer une autre
                def f(btn: TextButton) -> None:
                    level = levels[i]
                    level.reload()
                    level.setActive()
                return f
            card: TextButton = TextButton(x, y, width, height, level.name, None, 100, None, Color(100,25,171, 100), setActive(i), gameScreen)
            levelMenuContent.append(card)
            i += 1

        def back(btn: TextButton):
            self.menuSelect = False
            game.setToRun(self.run)

        levelMenuContent.append(
            TextButton(-1, heightGap, width, height, "Retour", None, 100, MENU_BUTTON_TEXT_COLOR, MENU_BUTTON_COLOR, back, gameScreen)
        )

        levelMenu.add(*levelMenuContent)
        game.setToRun(levelMenu.run)
        self.menuSelect = True