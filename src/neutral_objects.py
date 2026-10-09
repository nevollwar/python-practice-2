class NeutralObject:
    """Базовый класс (интерфейс) для всех нейтральных объектов"""
    def __init__(self, name: str, symbol: str ):
        self.name = name
        self.symbol = symbol

    def apply(self, unit):
        pass

    def __add__(self, unit):
        """Срабатывает при: item + unit"""
        self.apply(unit)
        return unit

    def __radd__(self, unit):
        """Срабатывает при: unit + item (сложение в обратную сторону)"""
        self.apply(unit)
        return unit

    def __str__(self):
        return self.symbol

class HealShrine(NeutralObject):
    def __init__(self):
        super().__init__(name="Святилище исцеления", symbol="+")

    def apply(self, unit):
        unit.hp = min(unit.max_hp, unit.hp + 50)
        print(f"{unit.symbol} помолился в святилище: HP восстановилось до {unit.hp}!")

class Whetstone(NeutralObject):
    def __init__(self):
        super().__init__(name="Точильный камень", symbol="W")

    def apply(self, unit):
        unit.attack += 10
        print(f"{unit.symbol} наточил клинок: Атака выросла до {unit.attack}!")

class ArmorKit(NeutralObject):
    def __init__(self):
        super().__init__(name="Мастер доспехов", symbol="D")

    def apply(self, unit):
        unit.armor = min(80, unit.armor + 10)
        print(f"{unit.symbol} улучшил доспех: Броня выросла до {unit.armor}%!")

class MakibishiTrap(NeutralObject):
    def __init__(self):
        super().__init__(name="Ловушка с шипами", symbol="!")

    def apply(self, unit):
        unit.hp = max(0, unit.hp - 40)
        print(f"{unit.symbol} наступил на шипы макибиси! Осталось HP: {unit.hp}!")