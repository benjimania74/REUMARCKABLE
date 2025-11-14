from typing import Any
from .DynamicText import *
from engine import Activated

class ActuateText(DynamicText, Activated):
    firstText: str
    secondText: str

    def __init__(self, x: int | Percent, y: int | Percent, width: int | Percent, height: int | Percent, firstText: str, secondText: str, fontFile: str | None, fontSize: int, color: Color, backgroundColor: Color | None, drawSurface: Surface) -> None:
        super().__init__(x, y, width, height, firstText, fontFile, fontSize, color, backgroundColor, drawSurface)
        self.firstText = firstText
        self.secondText = secondText

    def onActuated(self, data: dict[str, Any]|None = None) -> None:
        self.text = self.secondText
    
    def show(self):
        super().show()
        self.text = self.firstText