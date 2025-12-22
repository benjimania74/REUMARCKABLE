class Percent:
    value: float
    def __init__(self, value: float) -> None:
        self.value = value
    
    def getValue(self) -> float:
        return self.value

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return other * self.value / 100
        raise TypeError(f'Cannot multiply Percent with something that isn\'t a number')
    __rmul__ = __mul__

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Percent(self.getValue() + other.getValue())
        raise TypeError(f'Cannot add Percent with anything except Percent')