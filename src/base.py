from src.units import Unit
from src.field import Field

class Base:
    def __init__(self, x: int, y: int, hp: int = 500, max_units: int = 5):
        self.new_unit = None
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.max_units = max_units
        self.symbol = "B"

        # Список юнитов, которые сейчас живы и принадлежат этой базе
        self.units = []

    def create_unit(self, unit_class: Unit, field: Field):
        # 1. Проверяем лимит базы
        if len(self.units) >= self.max_units:
            print("Лимит армии достигнут!")
            return None

        # 2. Ищем свободную соседнюю клетку вокруг базы
        spawn_x, spawn_y = None, None
        neighbors = [
            (self.x + 1, self.y), # справа
            (self.x - 1, self.y), # слева
            (self.x, self.y + 1), # снизу
            (self.x, self.y - 1), # сверху
        ]

        for nx, ny in neighbors:
            # Если клетка внутри поля и там пусто
            if field.is_inside(nx, ny) and field.get_object(nx, ny) is None:
                spawn_x, spawn_y = nx, ny
                break

        # Если вокруг базы всё заблокировано
        if spawn_x is None:
            print("Вокруг базы нет свободного места для спавна!")
            return None

        # 3. Рождаем юнита
        new_unit = unit_class()

        # 4. Ставим его на поле
        field.add_object(new_unit, spawn_x, spawn_y)
        new_unit.move(spawn_x, spawn_y)

        # 5. База берет его на учет в свой список
        self.units.append(new_unit)
        print(f"База создала юнита {new_unit} в точке ({spawn_x}, {spawn_y})!")

        return new_unit

    def unit_tracking(self):
        """Проверяет армию базы и удаляет погибших воинов"""
        # Считаем, сколько было до чистки
        old_count = len(self.units)

        # Оставляем только тех, кто жив
        self.units = [u for u in self.units if u.is_alive()]

        # Если кто-то умер, выводим информацию:
        dead_count = old_count - len(self.units)
        if dead_count > 0:
            print(f"База зафиксировала потери: погибло {dead_count} воинов.")

    def take_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            print("База уничтожена!")

    def is_alive(self) -> bool:
        return self.hp > 0

    def __str__(self) -> str:
        return self.symbol