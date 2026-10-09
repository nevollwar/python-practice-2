import random
from src.field import Field
from src.base import Base
from src.landscape import BambooForest, Mountain
from src.neutral_objects import HealShrine, Whetstone, MakibishiTrap, ArmorKit
from src.units import Samurai, YariAshigaru, YumiArcher, TeppoGunner, MountedSamurai, Yabusame, Unit


class Game:
    def __init__(self, width: int = 20, height: int = 15):
        self.width = width
        self.height = height

        # 1. Создаем поле
        self.field = Field(width, height, max_objects=20)

        # 2. Ставим базу игрока в координаты (1, 1)
        self.base = Base(x=1, y=1, hp=500, max_units=5)
        self.field.add_object(self.base, self.base.x, self.base.y)

        # 3. Рассыпем ландшафт и предметы
        self.setup_map()

        self.is_running = True

    def setup_map(self):
        """Генерация живого мира: леса, горы и лут по всей карте"""
        # 1. Засеиваем ландшафт (леса и горы)
        for y in range(self.height):
            for x in range(self.width):
                # Зону вокруг базы (1, 1) оставляем чистой равниной для спавна!
                if abs(x - self.base.x) <= 2 and abs(y - self.base.y) <= 2:
                    continue

                roll = random.random()
                if roll < 0.23:       # 23% шанс на Бамбуковый лес (*)
                    self.field.set_landscape(BambooForest(), x, y)
                elif roll < 0.33:     # 10% шанс на Горы (^)
                    self.field.set_landscape(Mountain(), x, y)

        # 2. Разбрасываем нейтральные объекты (сундуки, святилища, ловушки)
        # Количество предметов зависит от размера карты:
        items_count = max(4, (self.width * self.height) // 25)

        item_classes = [HealShrine, Whetstone, ArmorKit, MakibishiTrap]

        placed = 0
        while placed < items_count:
            rx = random.randint(0, self.width - 1)
            ry = random.randint(0, self.height - 1)

            # Не спавним лут прямо на базу или вплотную к ней
            if abs(rx - self.base.x) <= 2 and abs(ry - self.base.y) <= 2:
                continue

            # Спавним только в пустые клетки и не на горы
            if self.field.get_object(rx, ry) is None and self.field.landscape_grid[ry][rx].is_passable:
                chosen_item = random.choice(item_classes)()
                self.field.add_object(chosen_item, rx, ry)
                placed += 1

    def manage_base(self):
        """Меню управления базой: остаемся в меню, пока не нажмут 0"""
        while True:
            print("\n УПРАВЛЕНИЕ БАЗОЙ ")
            print(f"Здоровье замка: {self.base.hp}/{self.base.max_hp}")
            print(f"Армия базы: {len(self.base.units)}/{self.base.max_units} воинов")
            print("1 - Нанять воина")
            print("2 - Показать список отряда")
            print("0 - Выйти в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                print("\nНанять воина:")
                print("1 - [S] Самурай (Пехота)")
                print("2 - [Y] Асигару с копьем (Пехота)")
                print("3 - [A] Лучник Юми (Стрелки)")
                print("4 - [T] Тэппо с ружьем (Стрелки)")
                print("5 - [K] Конный самурай (Кавалерия)")
                print("6 - [H] Ябусамэ (Конный лучник)")

                unit_map = {
                    "1": Samurai, "2": YariAshigaru, "3": YumiArcher,
                    "4": TeppoGunner, "5": MountedSamurai, "6": Yabusame,
                }

                u_choice = input("Выберите воина: ")
                if u_choice in unit_map:
                    self.base.create_unit(unit_map[u_choice], self.field)
                else:
                    print("Неверный выбор воина!")

            elif choice == "2":
                print("\nВаши воины на службе:")
                if not self.base.units:
                    print("У вас пока нет нанятых воинов.")
                for idx, u in enumerate(self.base.units, 1):
                    print(f"{idx}. [{u.symbol}] в координатах ({u.x}, {u.y}) | HP: {u.hp}/{u.max_hp} | Атака: {u.attack}")

            elif choice == "0":
                break

    def manage_unit(self):
        """Меню управления воином на карте"""
        print("\n=== УПРАВЛЕНИЕ ЮНИТОМ ===")
        try:
            ux = int(input("Выберите координату X юнита: "))
            uy = int(input("Выберите координату Y юнита: "))
        except ValueError:
            print("Координаты должны быть числами!")
            return

        obj = self.field.get_object(ux, uy)

        if obj is None or not isinstance(obj, (Samurai, YariAshigaru, YumiArcher,
                                               TeppoGunner, MountedSamurai, Yabusame)):
            print("В этих координатах нет вашего воина!")
            return

        unit = obj
        print(f"\nЮнит [{unit.symbol}] готов к приказу! Скорость хода: {unit.speed} клеток.")
        print("1 - Переместиться")
        print("0 - Отмена")

        act = input("Действие: ")
        if act == "1":
            try:
                new_x = int(input(f"Куда идти по X (текущий {unit.x}): "))
                new_y = int(input(f"Куда идти по Y (текущий {unit.y}): "))
            except ValueError:
                print("Неверные координаты!")
                return

            distance = abs(new_x - unit.x) + abs(new_y - unit.y)
            if distance > unit.speed:
                print(f"Слишком далеко! Максимальная дистанция хода: {unit.speed} клеток.")
                return

            target_cell = self.field.get_object(new_x, new_y)

            from src.neutral_objects import NeutralObject
            if isinstance(target_cell, NeutralObject):
                unit + target_cell
                self.field.remove_object(new_x, new_y)

            self.field.remove_object(unit.x, unit.y)
            if self.field.add_object(unit, new_x, new_y):
                unit.move(new_x, new_y)
                print(f"Юнит [{unit.symbol}] успешно переместился в ({new_x}, {new_y})!")
            else:
                self.field.add_object(unit, unit.x, unit.y)
                print("Не удалось переместиться (клетка занята или непроходима)!")

    def run(self):
        """Главный цикл игры (Game Loop)"""
        print("=== САМУРАЙСКАЯ СТРАТЕГИЯ ЗАПУЩЕНА ===")
        while self.is_running:
            print("\n" + "=" * 30)
            self.field.display()
            print("=" * 30)

            print("1 - Управление базой")
            print("2 - Управление юнитом")
            print("3 - Закончить ход")
            print("4 - Справка (обозначения)")
            print("0 - Выход из игры")

            choice = input("Ваш выбор: ")

            if choice == "1":
                self.manage_base()
            elif choice == "2":
                self.manage_unit()
            elif choice == "3":
                self.base.unit_tracking()
                print("Ход завершен! Войска готовы к новым приказам.")
            elif choice == "4":
                self.show_help()
            elif choice == "0":
                print("Игра окончена. До встречи, сёгун!")
                self.is_running = False
            else:
                print("Неверная команда, попробуйте снова!")

    def show_help(self):
        """Справка по всем символам игры"""
        print("\n" + "=" * 45)
        print("          СПРАВКА / ЛЕГЕНДА КАРТЫ")
        print("=" * 45)
        print("ЗДАНИЯ:")
        print("  [B] - Замок (База игрока, спавнит войска)")
        print("\nЛАНДШАФТ:")
        print("  .   - Равнина (проходима для всех)")
        print("  *   - Бамбуковый лес (пехота проходит, конница НЕТ)")
        print("  ^   - Горы (непроходимы ни для кого)")
        print("\nВОИНЫ:")
        print("  [S] - Самурай (тяжелый мечник, ход 2)")
        print("  [Y] - Асигару (копейщик, достает через 1 клетку)")
        print("  [A] - Лучник Юми (дальний бой)")
        print("  [T] - Аркебузир Тэппо (бронебойный залп)")
        print("  [K] - Конный самурай (таранная конница, ход 4)")
        print("  [H] - Ябусамэ (конный лучник, ход 5)")
        print("\nПРЕДМЕТЫ НА КАРТЕ:")
        print("  [+] - Святилище (+50 HP к здоровью)")
        print("  [W] - Точильный камень (+10 к атаке)")
        print("  [!] - Ловушка Макибиси (-40 HP при наступании)")
        print("=" * 45)
        input("\nНажмите Enter, чтобы вернуться...")