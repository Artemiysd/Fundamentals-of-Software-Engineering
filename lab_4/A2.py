
print("Выберите фигуру:")
print("1 — Прямоугольник")
print("2 — Правый треугольник")
print("3 — Рамка")

choice = input("Ваш выбор: ")

if choice == '1':
    n = int(input("Введите количество строк (n): "))
    m = int(input("Введите количество столбцов (m): "))

    for i in range(n):
        for j in range(m):
            print('*', end='')
        print()

elif choice == '2':
    n = int(input("Введите количество строк: "))

    for i in range(1, n + 1):
        for j in range(i):
            print('*', end='')
        print()

elif choice == '3':
    n = int(input("Введите количество строк (n): "))
    m = int(input("Введите количество столбцов (m): "))

    for i in range(n):
        for j in range(m):
            if i == 0 or i == n - 1 or j == 0 or j == m - 1:
                print('*', end='')
            else:
                print(' ', end='')
        print()

else:
    print("Ошибка: выберите 1, 2 или 3.")