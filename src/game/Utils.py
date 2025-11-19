from sys import path

from engine.Percent import Percent

from pygame import Color

from typing import Union

Texture = Union[Color,str]

# Constantes
EXEC_DIRECTORY: str = path[0] + "/"

IMAGE_DIRECTORY: str = EXEC_DIRECTORY + "game/assets/images/"
NO_TEXTURE: str = "no_texture.png"
ICON: str = "icon.png"

LEVEL_DIRECTORY: str = EXEC_DIRECTORY + "game/levels/"

FRAME_NAME: str = "REUMARKABLE"
FRAME_WIDTH: int = 1280
FRAME_HEIGHT: int = 720

PLAYER_TEXTURE: Texture = Color(255,255,0)
PHANTOM_TEXTURE: Texture = Color(0,0,255)

GROUND_TEXTURE: Texture = Color(0,255,0)

DOOR_TEXTURE: Texture = Color(0,255,255)

END_COLLIDER_TEXTURE: Texture = Color(255,0,0)

BUTTON_COLOR: Texture = Color(255,0,255)

# Fonctions utiles
def toPygameY(y:int, height:int, surfaceHeight:int) -> int:
    """Transforme une coordonnée y pour laquel y=0 équivaut à ce que l'on soit en bas de la surface en coordonnée telle que y=0 équivaut à ce que l'on soit en haut de la surface"""
    return surfaceHeight - y - height

def calcPercent(val:int|Percent, value_neg: int, percent_of: int) -> int:
        res: int
        if isinstance(val, int):
            res = val if -1 < val else value_neg
        else:
            res = int(percent_of * val)
        return res