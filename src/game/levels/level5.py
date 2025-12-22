from game.Game import Game
from game.menu import *
from game.levels.Level import Level
from game.Utils import *
from game.menu import *
from game.menu import Menu
from game.objects import *

class Cages(Level):
    def __init__(self, mainMenu: Menu, game: Game) -> None:
        super().__init__(mainMenu, game, "Cages")
    
    def load(self) -> None:
        gameScreen: Surface = self.game.getScreen()

        colliders = self.colliders

        player: Player = Player(30, Percent(55), 50, 50, PLAYER_TEXTURE, self.colliders, gameScreen)
        phantom: PhantomPlayer = PhantomPlayer(FRAME_WIDTH - 80, Percent(55), 50, 50, PHANTOM_TEXTURE, self.colliders, gameScreen)
        rectangleCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,Color|str|None] ] = [
            # x, y, w, h, prio, hard,color
            (0, Percent(50), 20, Percent(15), 51, True, GROUND_TEXTURE), # mur gauche cage player
            (90, Percent(50), 20, Percent(15), 51, True, GROUND_TEXTURE), # mur droit cage player
            (FRAME_WIDTH - 110, Percent(50), 20, Percent(15), 51, True, GROUND_TEXTURE), # mur gauche cage phantom
            (FRAME_WIDTH - 20, Percent(50), 20, Percent(15), 51, True, GROUND_TEXTURE), # mur droit cage phantom
            (-1, Percent(80), 110, 20, 51, True, GROUND_TEXTURE), # sol cage fin
        ]

        plateformsPositions: list[tuple[int,Percent]] = [
            (160, Percent(40)),
            (500, Percent(40)),
            (330, Percent(45)),
        ]

        for pos in plateformsPositions:
            for i in range(5):
                y: Percent = Percent(11*i) + pos[1]
                rectangleCollidersInfo.append(
                    (pos[0], y, 50, 10, 51, True, GROUND_TEXTURE)
                )
                rectangleCollidersInfo.append(
                    (FRAME_WIDTH - pos[0] - 50 if pos[0] != -1 else -1, y, 50, 10, 51, True, GROUND_TEXTURE)
                )

        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, gameScreen) )

        doorsInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int|Percent,int|Percent,int,Color|str|None] ] = [
            # x, y, w, h, nW, nH, prio, color
            (0, Percent(50), 110, 20, 0, 0, 51, DOOR_TEXTURE), # porte sol cage player
            (FRAME_WIDTH - 110, Percent(50), Percent(15), 20, 0, 0, 51, DOOR_TEXTURE), # porte sol cage phantom
            (FRAME_WIDTH // 2 - 75, Percent(80), 20, Percent(15), 0, 0, 51, DOOR_TEXTURE), # porte gauche cage fin
            (FRAME_WIDTH // 2 + 55, Percent(80), 20, Percent(15), 0, 0, 51, DOOR_TEXTURE) # porte droite cage fin
        ]

        doors: list[Door] = []

        for dI in doorsInfo:
            doors.append(ClickDoor(*dI, gameScreen))
        
        colliders += doors

        playerDetectorCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,list[Door],Color|str|None,list[Player]] ] = [
            # x, y, w, h, prio, hard, portes, color
            (0, Percent(65), 110, 20, 51, True, doors[0:2], BUTTON_COLOR, [player,phantom]), # pdc player
            (FRAME_WIDTH - 110, Percent(65), 110, 20, 51, True, doors[0:2], BUTTON_COLOR, [player,phantom]), # pdc phantom
            (0, Percent(30), FRAME_WIDTH, 50, 51, True, doors[2:4], BUTTON_COLOR, [player,phantom]) # pdc sol
        ]

        playerDetectorColliders: list[PlayerDetectorCollider] = []

        for pdci in playerDetectorCollidersInfo:
            playerDetectorColliders.append(PlayerDetectorCollider(*pdci, gameScreen))

        end: EndGamePlayerDetectorCollider = EndGamePlayerDetectorCollider(
            -1, Percent(81.5), 100, 10, 51, True, self, END_COLLIDER_TEXTURE, player, gameScreen
        )
        colliders.append(end)

        colliders += playerDetectorColliders

        colliders += [player, phantom]
        
        self.player = player
        self.phantom = phantom
        self.activePlayer = self.player

        self.content += colliders


export: dict[str,Any] = {
    "class_name": Cages.__qualname__
}