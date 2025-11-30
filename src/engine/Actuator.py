from typing import Any

class Activated:
    def onActuated(self, data:dict[str,Any]|None = None) -> None:
        pass

class Actuator:
    activateds: list[Activated]
    data: dict[str, Any]
    
    def actuate(self) -> None:
        for activated in self.activateds:
            activated.onActuated(self.data)
        