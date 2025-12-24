from game.Game import Game
from game.menu import *
from game.levels.Level import Level
from game.Utils import *
from game.menu import *
from game.menu import Menu
from game.objects import *

class Corridor(Level):
    def __init__(self, mainMenu: Menu, game: Game) -> None:
        super().__init__(mainMenu, game, "Couloir")
    
    def load(self) -> None:
        gameScreen: Surface = self.game.getScreen()

        colliders = self.colliders

        player: Player = Player(30, Percent(25), 50, 50, PLAYER_TEXTURE, self.colliders, gameScreen)
        phantom: PhantomPlayer = PhantomPlayer(30, Percent(65), 50, 50, PHANTOM_TEXTURE, self.colliders, gameScreen)

        colliders += [player, phantom]

        rectangleCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,Color|str|None] ] = [
            # x, y, w, h, prio, hard,color
            (0, Percent(50), -1, 50, 51, True, GROUND_TEXTURE),
            (Percent(16), Percent(30), FRAME_WIDTH - 16, 10, 51, True, GROUND_TEXTURE)
        ]
        rectangleCollidersInfo += [(Percent(16*i), Percent(15), Percent(8), 50, 51, True, GROUND_TEXTURE) for i in range(6)]

        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, gameScreen) )
        
        n = len(rectangleCollidersInfo) - 3
        doorsInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int|Percent,int|Percent,int,Color|str|None] ] = [
            # x, y, w, h, nW, nH, prio, color
            (Percent(7.8 + 16*i), Percent(15), Percent(9), 50, 0, 0, 51, DOOR_TEXTURE) for i in range(n)
        ]

        doors: list[Door] = []

        for dI in doorsInfo:
            door: Door = ClickDoor(*dI, gameScreen)
            door.onActuated()
            doors.append(door)

        colliders += doors

        playerDetectorCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,list[Door],Color|str|None,list[Player]] ] = [
            # x, y, w, h, prio, hard, doors, color, players
            (Percent(7.8 + 16*(i+1)), Percent(50), Percent(9), 50, 51, True, doors[n-1-i:n-i], PLAYER_DETECTOR_COLOR, [phantom]) for i in range(n)
        ]

        playerDetectorColliders: list[PlayerDetectorCollider] = []

        for pdci in playerDetectorCollidersInfo:
            playerDetectorColliders.append(PlayerDetectorCollider(*pdci, gameScreen))
        
        colliders += playerDetectorColliders

        end: EndGamePlayerDetectorCollider = EndGamePlayerDetectorCollider(Percent(88), Percent(15), Percent(12), 50, 51, True, self, END_COLLIDER_TEXTURE, player, gameScreen)
        colliders.append(end)

        self.player = player
        self.phantom = phantom
        self.activePlayer = player

        self.content += colliders


export: dict[str,Any] = {
    "class_name": Corridor.__qualname__
}