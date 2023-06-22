def shiftleft(arr):
    """Зсовує елементи двовимірного списку вліво та додає однакові значення"""
    for i in range(len(arr)):
        # Тимчасовий список, на який ми будемо замінювати рядок
        newrow = []

        # Додаємо не нульові значення в newrow
        for j in range(len(arr[i])):
            if arr[i][j] != 0:
                newrow.append(arr[i][j])

        # Об'єднуємо однакові елементи
        for j in range(len(newrow)-1):
            # Перевірка на те, чи ми все ще знаходимось в межах списку newrow
            if j >= len(newrow)-1:
                break
            # Додаємо однакові елементи, видаляючи другий
            if newrow[j] == newrow[j+1]:
                newrow[j] *= 2
                newrow.pop(j+1)

        # Додаємо нулі, яких не вистачає
        for _ in range(len(newrow), len(arr[i])):
            newrow.append(0)

        # Присвоюємо новий рядок для списку
        arr[i] = newrow
    return arr


def shiftright(arr):
    """Зсовує елементи двовимірного списку вправо та додає однакові значення"""
    for i in range(len(arr)):
        # Тимчасовий список, на який ми будемо замінювати рядок
        newrow = []

        # Додаємо не нульові значення в newrow
        for j in range(len(arr[i])):
            if arr[i][j] != 0:
                newrow.append(arr[i][j])

        # Об'єднуємо однакові елементи
        for j in range(len(newrow)-1):
            # Перевірка на те, чи ми все ще знаходимось в межах списку newrow
            if j >= len(newrow)-1:
                break
            # Додаємо однакові елементи, видаляючи другий
            if newrow[j] == newrow[j+1]:
                newrow[j] *= 2
                newrow.pop(j+1)

        # Додаємо нулі, яких не вистачає
        for _ in range(len(newrow), len(arr[i])):
            newrow.insert(0, 0)

        # Присвоюємо новий рядок для списку
        arr[i] = newrow

    return arr


def shiftup(arr):
    """Зсовує елементи двовимірного списку догори та додає однакові значення"""
    for j in range(len(arr)):
        # Тимчасовий список, на який ми будемо замінювати стовпчик
        newcol = []

        # Додаємо в список ненульові елементи
        for i in range(len(arr[j])):
            if arr[i][j] != 0:
                newcol.append(arr[i][j])

        # Об'єднуємо однакові елементи, видаляючи дублікати
        for i in range(len(newcol)):
            if i >= len(newcol)-1:
                break
            if newcol[i] == newcol[i+1]:
                newcol[i] *= 2
                newcol.pop(i+1)

        # Додаємо нулі, яких не вистачає
        for i in range(len(newcol), len(arr[j])):
            newcol.append(0)

        # Замінюємо стовпець
        for i in range(len(arr[j])):
            arr[i][j] = newcol[i]

    return arr


def shiftdown(arr):
    """Зсовує елементи двовимірного списку вниз та додає однакові значення"""
    for j in range(len(arr)):
        # Тимчасовий список, на який ми будемо замінювати стовпчик
        newcol = []

        # Додаємо в список ненульові елементи
        for i in range(len(arr[j])):
            if arr[i][j] != 0:
                newcol.append(arr[i][j])

        # Об'єднуємо однакові елементи, видаляючи дублікати
        for i in range(len(newcol)):
            if i >= len(newcol) - 1:
                break
            if newcol[i] == newcol[i + 1]:
                newcol[i] *= 2
                newcol.pop(i + 1)

        # Додаємо нулі, яких не вистачає
        for i in range(len(newcol), len(arr[j])):
            newcol.insert(0, 0)

        # Замінюємо стовпець
        for i in range(len(arr[j])):
            arr[i][j] = newcol[i]

    return arr
