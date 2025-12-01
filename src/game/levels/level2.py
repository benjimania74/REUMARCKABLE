from game.Game import Game
from game.menu import *
from game.levels.Level import Level
from game.Utils import *
from game.menu import *
from game.menu import Menu
from game.objects import *

class ButtonLevel(Level):
    def __init__(self, mainMenu: Menu, game: Game) -> None:
        super().__init__(mainMenu, game, "Bouton")
    
    def load(self) -> None:
        gameScreen: Surface = self.game.getScreen()

        colliders = self.colliders
        actuators = self.actuators
        content = self.content

        indicationTextsText: list[str] = [
            "Appuyez sur E au niveau du boutton violet"
        ]

        indicationTexts: list[Text] = []
        yPercent: float = 85
        for text in indicationTextsText:
            indicationTexts.append(
                StaticText(
                    Percent(5),
                    Percent(yPercent),
                    Percent(90),
                    Percent(10),
                    text,
                    None,
                    1000,
                    Color(0,0,0),
                    None,
                    gameScreen
                )
            )
            yPercent -= 10

        content += indicationTexts

        player: Player = Player(0, Percent(50), 50, 50, PLAYER_TEXTURE, self.colliders, gameScreen)
        phantom: PhantomPlayer = PhantomPlayer(0, Percent(40), 50, 50, PHANTOM_TEXTURE, self.colliders, gameScreen)

        rectangleCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,Color|str|None] ] = [
            (0, Percent(30), FRAME_WIDTH, 50, 51, True, GROUND_TEXTURE), # sol principal
            (300, 316, 250, 50, 51, True, GROUND_TEXTURE), # plateforme
        ]
        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, gameScreen) )

        door: Door = Door(Percent(80), Percent(30), 50, Percent(30), 50, Percent(5), 51, DOOR_TEXTURE, gameScreen)
        colliders.append(door)

        button: ButtonPlayerDetectorCollider = ButtonPlayerDetectorCollider(450, 376, 20, 10, 51, False, [door], BUTTON_COLOR, [player,phantom], gameScreen)
        actuators.append(button)

        end: EndGamePlayerDetectorCollider = EndGamePlayerDetectorCollider(Percent(90), Percent(37), 50, 5, 51, False, self, END_COLLIDER_TEXTURE, player, gameScreen)
        colliders.append(end)

        colliders += actuators
        colliders += [player, phantom]

        self.player = player
        self.phantom = phantom
        self.activePlayer = self.player

        content += colliders
    
export: dict[str,Any] = {
    "class_name": ButtonLevel.__qualname__
}