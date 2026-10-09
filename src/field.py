import copy
from src.landscape import Plain
class Field:
    def __init__(self, width: int, height: int, max_objects: int):
        """
        Срабатывает при создании поля.
        Принимает: ширину, высоту и лимит объектов.
        """
        # 1. Проверяем размеры (размеры > 0)
        if width <= 0 or height <= 0:
            raise ValueError("Размеры поля должны быть больше 0!")

        # 2. Запоминаем характеристики поля
        self.width = width
        self.height = height
        self.max_objects = max_objects

        # 3. Счетчик объектов (контроль макс. количества)
        self.current_objects_count = 0

        # 4. Сама сетка: список списков, изначально заполненный None
        # (height строк, в каждой по width пустых ячеек)
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.landscape_grid = [[Plain() for _ in range(self.width)] for _ in range(self.height)]

    # Вспомогательные методы (защита от ошибок)

    def is_inside(self, x: int, y: int) -> bool:
        """Проверяет: координаты (x, y) вообще попадают внутрь поля?"""
        # Должно вернуть True, если x от 0 до width-1, и y от 0 до height-1
        if (0 <= x < self.width) and (0 <= y < self.height):
            return True
        return False

    # Основные методы

    def add_object(self, obj, x: int, y: int) -> bool:
        """
        1. Проверяем, что точка внутри карты (метод is_inside).
        2. Проверяем, что лимит объектов не превышен (current_objects_count < max_objects).
        3. Проверяем, что клетка пустая (там лежит None).
        Если всё ок:
            - кладем obj в self.grid[y][x]
            - увеличиваем счетчик на 1
            - возвращаем True
        """
        # Получаем ландшафт этой клетки
        terrain = self.landscape_grid[y][x] if self.is_inside(x, y) else None

        if (self.is_inside(x, y)
                and (self.current_objects_count < self.max_objects)
                and self.grid[y][x] is None
                and obj is not None
                and (terrain is None or terrain.can_enter(obj))):

            self.current_objects_count = self.current_objects_count + 1
            self.grid[y][x] = obj
            return True
        return False

    def remove_object(self, x: int, y: int) -> bool:
        """
        Возможность удаления объектов на поле.
        1. Проверяем координаты.
        2. Проверяем, что в клетке кто-то есть (не None).
        Если есть:
            - делаем self.grid[y][x] = None
            - уменьшаем счетчик на 1
            - возвращаем True
        """
        if self.is_inside(x, y) and self.grid[y][x] is not None:
            self.grid[y][x] = None
            self.current_objects_count = self.current_objects_count - 1
            return True
        return False

    def get_object(self, x: int, y: int):
        """
        Возвращает объект из клетки (x, y) или None, если там пусто.
        """
        if not self.is_inside(x, y):
            return None
        return self.grid[y][x]

    def copy(self):
        """
        Копирования поля (включая объекты на нем).
        """
        # Возвращает глубокую копию всего поля через copy.deepcopy(self)
        return copy.deepcopy(self)

    def display(self):
        """Вывод поля с идеальной двухстрочной разметкой координат"""
        # 1. Строка десятков (показываем 1, 2, 3... над десятками)
        tens_str = "     "
        for x in range(self.width):
            if x >= 10:
                tens_str += f"{x // 10} "
            else:
                tens_str += "  "  # для чисел меньше 10 просто пробелы
        print(tens_str)

        # 2. Строка единиц (0 1 2 3 4 5 6 7 8 9 0 1 2...)
        units_str = "     "
        for x in range(self.width):
            units_str += f"{x % 10} "
        print(units_str)

        # 3. Верхняя граница X
        print("   " + " ".join(["X"] * (self.width + 2)))

        # 4. Игровые строки с номерами Y
        for y in range(self.height):
            row_str = f"{y:2d} X "

            for x in range(self.width):
                obj = self.grid[y][x]
                if obj is None:
                    terrain = self.landscape_grid[y][x]
                    row_str += f"{terrain} "
                else:
                    row_str += f"{obj} "

            row_str += "X"
            print(row_str)

        # 5. Нижняя граница X
        print("   " + " ".join(["X"] * (self.width + 2)))

    def set_landscape(self, landscape_obj, x: int, y: int):
        """Установить ландшафт в клетку (горы, лес и т.д.)"""
        if self.is_inside(x, y):
            self.landscape_grid[y][x] = landscape_obj