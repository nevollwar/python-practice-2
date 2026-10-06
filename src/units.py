class Unit:
    def __init__(self, hp: int, attack: int,
                armor: int, speed: int,
                attack_range: int, symbol: str):
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.armor = armor
        self.speed = speed
        self.attack_range = attack_range
        self.symbol = symbol
        self.x = 0
        self.y = 0

    def move(self, new_x: int, new_y: int):
        """Перемещение юнита в новую точку"""
        self.x = new_x
        self.y = new_y

    def take_damage(self, damage: int):
        """Получение урона с учетом процентов брони"""
        real_damage = damage * (1 - self.armor / 100)
        self.hp -= real_damage
        if self.hp <= 0:
            self.hp = 0

    def attack_target(self, target: 'Unit'):
        """Нанести урон другому юниту"""
        self.target = target
        target.take_damage(self.attack)

    def is_alive(self):
        """Жив ли юнит"""
        return self.hp > 0

    def __str__(self) -> str:
        """Символ юнита для отрисовки на поле"""
        return self.symbol

class Infantry(Unit):
    """Тип: Пехота"""
    def __init__(self, hp: int, attack: int,
                 armor: int, speed: int,
                 attack_range: int, symbol: str):
        super().__init__(hp, attack, armor, speed, attack_range, symbol)

class Samurai(Infantry):
    """Вид 1: Самурай (Мастер меча)"""
    def __init__(self):
        super().__init__(
            hp=180,
            attack=25,
            armor=30,
            speed=2,
            attack_range=1,
            symbol="S"
        )

class YariAshigaru(Infantry):
    """Вид 2: Асигару с копьем (Танк)"""
    def __init__(self):
        super().__init__(
            hp=140,
            attack=15,
            armor=20,
            speed=1,
            attack_range=2,
            symbol="Y"
        )

class Shooter(Unit):
    """Тип: Стрелки"""
    def __init__(self, hp: int, attack: int,
                 armor: int, speed: int,
                 attack_range: int, symbol: str):
        super().__init__(hp, attack, armor, speed, attack_range, symbol)
        self.is_loaded = True  # Флаг: заряжено ли оружие

class YumiArcher(Shooter):
    """Лучник Юми"""
    def __init__(self):
        super().__init__(hp=100,
                         attack=12,
                         armor=5,
                         speed=1,
                         attack_range=5,
                         symbol="A")

class TeppoGunner(Shooter):
    """Стрелок с ружьем Тэппо"""
    def __init__(self):
        super().__init__(hp=100,
                         attack=35,
                         armor=5,
                         speed=1,
                         attack_range=7,
                         symbol="T")

class Cavalry(Unit):
    """Тип: Конница"""
    def __init__(self, hp: int, attack: int,
                 armor: int, speed: int, attack_range: int,
                 symbol: str):
        super().__init__(hp, attack, armor, speed, attack_range, symbol)
        self.can_jump = True  # Конница может перепрыгивать через препятствия

class MountedSamurai(Cavalry):
    """Конный самурай"""
    def __init__(self):
        super().__init__(hp=200,
                         attack=30,
                         armor=35,
                         speed=4,
                         attack_range=1,
                         symbol="K")

class Yabusame(Cavalry):
    """Конный лучник Ябусамэ"""
    def __init__(self):
        super().__init__(hp=130,
                         attack=20,
                         armor=10,
                         speed=5,
                         attack_range=6,
                         symbol="H")