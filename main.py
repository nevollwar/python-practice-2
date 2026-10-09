from src.game import Game


def start():
    print("=" * 40)
    print("       САМУРАЙСКАЯ СТРАТЕГИЯ: СЁГУН")
    print("=" * 40)

    try:
        w_input = input("Ширина поля (Enter = 20): ").strip()
        width = int(w_input) if w_input else 20

        h_input = input("Высота поля (Enter = 15): ").strip()
        height = int(h_input) if h_input else 15

        if width < 5 or height < 5:
            print("Слишком маленькое поле! Установлено минимальное 10х10.")
            width, height = 10, 10
    except ValueError:
        print("Ошибка ввода числа. Запускаем стандартное поле 20х15.")
        width, height = 20, 15

    game = Game(width=width, height=height)
    game.run()


if __name__ == "__main__":
    start()