from src.units import Cavalry


class Landscape:
    """Базовый класс (интерфейс) для всех типов местности"""
    def __init__(self, name: str, symbol: str, is_passable: bool = True):
        self.name = name
        self.symbol = symbol
        self.is_passable = is_passable

    def can_enter(self, unit) -> bool:
        """Базовая проверка проходимости"""
        return self.is_passable

    def __str__(self) -> str:
        return self.symbol

class Plain(Landscape):
    def __init__(self):
        super().__init__(name="Равнина", symbol=".", is_passable=True)

class BambooForest(Landscape):
    def __init__(self):
        super().__init__(name="Бамбуковый лес", symbol="*", is_passable=True)

    def can_enter(self, unit) -> bool:
        """Бамбуковый лес: пехота проходит, конница нет"""
        if isinstance(unit, Cavalry):
            return False
        return True

class Mountain(Landscape):
    """Горы: непроходимы вообще ни для кого"""
    def __init__(self):
        super().__init__(name="Горы", symbol="^", is_passable=False)

    def can_enter(self, unit) -> bool:
        return False