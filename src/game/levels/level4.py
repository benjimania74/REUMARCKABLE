from game.Game import Game
from game.menu import *
from game.levels.Level import Level
from game.Utils import *
from game.menu import *
from game.menu import Menu
from game.objects import *

class Start(Level):
    def __init__(self, mainMenu: Menu, game: Game) -> None:
        super().__init__(mainMenu, game, "Début")
    
    def load(self) -> None:
        gameScreen: Surface = self.game.getScreen()

        colliders = self.colliders

        player: Player = Player(0, Percent(100), 50, 50, PLAYER_TEXTURE, self.colliders, gameScreen)
        phantom: PhantomPlayer = PhantomPlayer(0, Percent(90), 50, 50, PHANTOM_TEXTURE, self.colliders, gameScreen)

        rectangleCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,Color|str|None] ] = [
            # x, y, w, h, prio, hard,color
            (0, Percent(73), Percent(60), 50, 51, True, GROUND_TEXTURE), # sol haut gauche
            (Percent(90), Percent(73), Percent(10), 50, 51, True, GROUND_TEXTURE), # sol haut droite
        ]

        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, gameScreen) )

        doorsInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int|Percent,int|Percent,int,Color|str|None] ] = [
            # x, y, w, h, nW, nH, prio, color
            (Percent(60), Percent(73), Percent(30), 50, 0, 0, 51, DOOR_TEXTURE),
            (Percent(10), Percent(53), Percent(10), 50, 0, 0, 51, DOOR_TEXTURE)
        ]

        doors: list[Door] = []

        for dI in doorsInfo:
            doors.append(ClickDoor(*dI, gameScreen))
        
        doors[1].onActuated() # porte ouverte par défaut
        
        colliders += doors

        playerDetectorCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,list[Door],Color|str|None,list[Player]] ] = [
            (Percent(92.5), Percent(73), Percent(5), 50, 51, True, doors[0:1], BUTTON_COLOR, [player, phantom]), # sur plateforme en haut
            (Percent(20), Percent(53), Percent(80), 50, 51, True, doors[0:2], BUTTON_COLOR, [player, phantom]), # plateforme droite niveau 2
            (0, Percent(53), Percent(10), 50, 51, True, doors[1:2], BUTTON_COLOR, [player, phantom]) # plateforme gauche niveau 2
        ]

        playerDetectorColliders: list[PlayerDetectorCollider] = []

        for pdci in playerDetectorCollidersInfo:
            playerDetectorColliders.append(PlayerDetectorCollider(*pdci, gameScreen))

        end: EndGamePlayerDetectorCollider = EndGamePlayerDetectorCollider(0, Percent(33), FRAME_WIDTH, 50, 51, True, self, END_COLLIDER_TEXTURE, player, gameScreen)
        colliders.append(end)

        colliders += playerDetectorColliders

        colliders += [player, phantom]
        
        self.player = player
        self.phantom = phantom
        self.activePlayer = self.player

        self.content += colliders

export: dict[str,Any] = {
    "class_name": Start.__qualname__
}