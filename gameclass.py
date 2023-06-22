import random               # Модуль для генерації випадкових чисел
from ArrShift import *      # Власний модуль, в якому описані способи зсуву та об'єднання однакових елементів

# Константи
C_LEFT = 0
C_UP = 1
C_RIGHT = 2
C_DOWN = 3

C_NEW = 0
C_PLAYING = 1
C_WIN = 2
C_LOOSE = 3


# Клас, що описує ігрове поле, та функції, пов'язані з грою
class GameBoard:
    def __init__(self, sz=4):

        # Розмір ігрового поля, типово 4
        self.size = sz

        # Ігрове поле, self.size x self.size
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

        # Очки гравця
        self.score = 0

        # Кількість ходів гравця
        self.turns = 0

        # Попередня ігрова дошка, для повернення на крок назад
        self.lastboard = [[0 for _ in range(self.size)] for _ in range(self.size)]

        # Якщо false, то ми не можемо повернутися на крок назад
        self.canrevert = False

        # Стан гри, якщо C_LOOSE, то ми програли, якщо C_WIN, то ми виграли, якщо C_PLAYING, то ми граємо
        self.state = C_PLAYING

    def newgame(self):
        """Рестарт гри"""
        # Оновлюємо ігрове поле
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

        # Створюємо два випадкових початкових числа
        self.spawnnumber()
        self.spawnnumber()

        # Оновлюємо ходи та очки
        self.turns = 0
        self.score = 0

        self.state = C_PLAYING

    def checkwin(self):
        """Перевіряє, чи існує 2048 десь на полі. Якщо існує - перемога"""
        for i in range(self.size):
            if 2048 in self.board[i]:
                self.state = C_WIN

    def getempties(self):
        """Повертає список з порядковими номерами пустих полів.
        Підказка: отримати доступ до поля - self.board[currid//self.size][currid % self.size]"""
        empties = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    empties.append(i*4+j)
        return empties

    def spawnnumber(self):
        """У випадковому пустому полі з'являється або 2 (Р=0.75), або 4 (Р=0.25)"""
        empties = self.getempties()
        if not empties:
            self.state = C_LOOSE

        currid = empties[random.randrange(0, len(empties))]

        if random.random() <= 0.75:
            self.board[currid//self.size][currid % self.size] = 2
        else:
            self.board[currid//self.size][currid % self.size] = 4

    def canmove(self, direction):
        """Перевіряє, чи можна походити в одному з напрямків"""
        if direction == C_UP:
            for j in range(self.size):
                for i in range(self.size-1, 0, -1):
                    if self.board[i][j] != 0:
                        if self.board[i-1][j] == 0 or self.board[i-1][j] == self.board[i][j]:
                            return True
        elif direction == C_RIGHT:
            for i in range(self.size):
                for j in range(self.size-1):
                    if self.board[i][j] != 0:
                        if self.board[i][j+1] == self.board[i][j] or self.board[i][j+1] == 0:
                            return True
        elif direction == C_DOWN:
            for j in range(self.size):
                for i in range(self.size-1):
                    if self.board[i][j] != 0:
                        if self.board[i+1][j] == self.board[i][j] or self.board[i+1][j] == 0:
                            return True
        elif direction == C_LEFT:
            for i in range(self.size):
                for j in range(self.size-1, 0, -1):
                    if self.board[i][j] != 0:
                        if self.board[i][j-1] == self.board[i][j] or self.board[i][j-1] == 0:
                            return True

        # Якщо напрямок задано неправильно, або для заданого ми не знайшли, що можна походити, повертаємо False
        return False

    def checkloose(self):
        """Перевірка на програш гри"""
        # Якщо ми не можемо рухатися в жодному з напрямків, то гру завершено
        if not self.canmove(C_LEFT) \
                and not self.canmove(C_UP) \
                and not self.canmove(C_RIGHT) \
                and not self.canmove(C_DOWN):
            self.state = C_LOOSE

    def turn(self, direction):
        """Функція, щоб походити, приймає такі параметри:\n
        0 - вліво;\n
        1 - вгору;\n
        2 - вправо;\n
        3 - вниз"""

        if not self.canmove(direction):
            return

        for i in range(self.size):
            for j in range(self.size):
                self.lastboard[i][j] = self.board[i][j]

        if direction == C_LEFT:
            shiftleft(self.board)

        elif direction == C_UP:
            shiftup(self.board)

        elif direction == C_RIGHT:
            shiftright(self.board)

        elif direction == C_DOWN:
            shiftdown(self.board)

        self.score = 0
        for i in range(self.size):
            self.score += sum(self.board[i])

        self.spawnnumber()
        self.turns += 1
        self.canrevert = True
        self.checkloose()
        self.checkwin()

    def revert(self):
        """Повертає ігрове поле на крок назад і зменшує кількість ходів на 1"""
        if not self.canrevert:
            return
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = self.lastboard[i][j]

        self.score = 0
        for i in range(self.size):
            self.score += sum(self.board[i])

        self.canrevert = False
        self.turns -= 1
