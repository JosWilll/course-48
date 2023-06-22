import pygame as pg                 # Основний модуль для обробки ігрових подій
import tkinter.messagebox as tk     # Для повідомлень
from gameclass import *             # Власна бібліотека з класом, що описує ігрове поле


# Словник з кортежами дозволяє нам мати легкий доступ до кольорів.
# Тут зібрані нові підібрані кольори, а також кольори, які відповідають оригіналу
colors = {0: (190, 178, 204),               # (204, 192, 179),
          2: (227, 218, 238),               # (238, 228, 218),
          4: (220, 200, 236),               # (237, 224, 200),
          8: (185, 121, 242),               # (242, 177, 121),
          16: (190, 99, 245),               # (245, 149, 99),
          32: (160, 81, 214),               # (246, 124, 95),
          64: (150, 59, 246),               # (246, 94, 59),
          128: (240, 113, 229),             # (237, 207, 114),
          256: (237, 56, 220),              # (237, 204, 97),
          512: (237, 39, 216),              # (237, 200, 80),
          1024: (237, 22, 212),             # (237, 197, 63),
          2048: (237, 5, 207),              # (237, 194, 46),
          'light text': (246, 239, 255),    # (249, 246, 242),
          'dark text': (85, 75, 97),        # (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (170, 160, 187),            # (187, 173, 160),
          'game over': (208, 187, 148, 128)}

# Запускаємо модуль pygame
pg.init()

# Об'єкт ігрової дошки
Game = GameBoard()
Game.newgame()


def draw():
    """Відмальовує зміни на екрані"""
    # Заповнюємо весь екран чорним кольором
    screen.fill(colors['bg'])

    # Ширина границь між клітинками
    borderwidth = 10

    # Ширина клітинок
    wd = (screen.get_width() - (Game.size + 1) * borderwidth) // Game.size

    # Радіус округлення кутів
    radius = screen.get_width() // 80

    # Задає шрифт для значень клітинок, та його розмір. None тут означає, що буде типовий шрифт pygame
    font = pg.font.Font(None, wd // 2)

    # Малюємо клітини
    for i in range(Game.size):
        for j in range(Game.size):
            # Отримуємо значення поточної клітинки. Від нього залежить колір клітинки
            val = Game.board[i][j]

            # Розраховуємо позицію клітинки. x та y тут - це початкові координати клітини
            x = j * wd + (j + 1) * borderwidth
            y = i * wd + (i + 1) * borderwidth

            # Малюємо клітинку. Обираємо колір клітинки в залежності від її значення
            pg.draw.rect(screen, colors[val], pg.Rect(x, y, wd, wd), border_radius=radius)

            # Починаємо відмальовку тексту на клітинці з її значенням, якщо воно не дорівнює одиниці (клітинка не пуста)
            if val != 0:
                # Для того, щоб визначити правильно розмір шрифта, нам потрібна довжина тексту - значення клітини
                valsize = len(str(val))

                # Задаємо колір шрифту. Якщо значення клітинки більше ніж 8, то текст буде світлого відтінку, бо кольори
                # клітинок темніші, а якщо менше - темного відтінку, бо клітинки світлі
                valclr = colors['light text'] if val > 8 else colors['dark text']

                # Зазначаємо шрифт. 25/3, як і 80 - випадкові значення, з яким, на мій погляд, розмір доречний.
                # Як і все інше, розмір скалюється від ширини екрану, тож всі операції проводимо саме з ним.
                font = pg.font.Font(None, int(screen.get_width() / 8.3 - (valsize * screen.get_width() / 80)))

                # В змінній text зберігаємо зображення значення клітинки, щоб потім його намалювати зверху клітинки
                text = font.render(str(val), True, valclr)

                # В змінній textrect зберігаємо прямокутне зображення text, щоб задати координати, де будемо малювати
                # значення клітини. Це буде центр клітини
                textrect = text.get_rect(center=(x + wd // 2, y + wd // 2))

                # Малюємо текст
                screen.blit(text, textrect)

    info_text = font.render(f'Хід: {Game.turns}, очки: {Game.score}', True, colors['dark text'])
    screen.blit(info_text, (borderwidth, Game.size * wd + (Game.size + 1) * borderwidth))

    pg.display.flip()


if __name__ == "__main__":
    fps = 60    # Скільки разів на секунду гра буде оновлюватися
    fpsClock = pg.time.Clock()      # Таймер для оновлення гри

    width, height = 600, 800    # Ширина та довжина вікна зі грою
    screen = pg.display.set_mode((width, height))   # Об'єкт екрану з грою
    pg.display.set_caption("2048")

    # Малюємо ігрове поле, щоб не було чорного екрану
    draw()

    # Виводимо вітальне повідомлення
    tk.showinfo(title="Вітаю у грі \"2048\"!", message="""-натискайте стрілочки для керування;
-об'єднуйте числа і наберіть число 2048 раніше, ніж заповниться поле;
-натисніть \'R\', щоб скасувати останній хід;
-натисніть \'Enter\', щоб почати заново.""")

    Game.board[0][0] = 2048

    # Відповідає за те, щоб коли клавіша затиснута, гра не посилала сигнал ходу постійно
    pressed = False

    run = True      # Поки ця змінна істинна, цикл гри буде відбуватися
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()

        # Якщо стан гри - C_PLAYING (гра в процесі), то перевіряємо головні кнопки керування
        if Game.state == C_PLAYING:
            if not pressed:
                # Якщо натиснута стрілка, рухаємо клітинки та задаємо pressed True (значить, що ми натиснули)
                if keys[pg.K_UP]:
                    Game.turn(C_UP)
                    pressed = True
                elif keys[pg.K_DOWN]:
                    Game.turn(C_DOWN)
                    pressed = True
                elif keys[pg.K_LEFT]:
                    Game.turn(C_LEFT)
                    pressed = True
                elif keys[pg.K_RIGHT]:
                    Game.turn(C_RIGHT)
                    pressed = True

            # Якщо натиснути R, гра повернеться на хід назад, але це можна робити раз за хід
            if keys[pg.K_r]:
                Game.revert()

            if keys[pg.K_RETURN]:
                reset = tk.askyesno(title="Ви впевнені?", message="Ви впевнені, що хочете почати заново?")
                if reset:
                    Game.newgame()

        if Game.state == C_LOOSE:
            # Оновлюємо екран один раз, щоб відмалювати останній хід
            draw()
            reset = tk.askyesno(title="Гру завершено!", message=
            f"""Гру завершено! фінальний рахунок: {Game.score}.
Чи бажаєте пограти заново?""")
            if reset:
                Game.newgame()
            else:
                run = False

        if Game.state == C_WIN:
            # Оновлюємо екран один раз, щоб відмалювати останній хід
            draw()
            reset = tk.askyesno(title="Перемога!", message=
            f"""Вітаю, Ви перемогли за {Game.turns} ходів!
Фінальний рахунок: {Game.score}.
Чи бажаєте пограти заново?""")
            if reset:
                Game.newgame()
            else:
                run = False

        # Якщо не натиснуті головні кнопки керування, передаємо False pressed, що означає, що можна ходити
        if not keys[pg.K_LEFT] and not keys[pg.K_RIGHT] and not keys[pg.K_UP] and not keys[pg.K_DOWN]:
            pressed = False

        # Відмальовуємо зміни на екрані
        draw()

        # Вмикаємо таймер, щоб затримати обробку гри
        fpsClock.tick(fps)

    # Виходимо і виводимо прощальне повідомлення
    tk.showinfo(title="Дякую!", message="Дякую за гру!"
                                        "\nРозробив: студент групи КНТ-112сп"
                                        "\nНУ \"Запорізька Політехніка\""
                                        "\nСтамінов Олексій")
    pg.quit()
