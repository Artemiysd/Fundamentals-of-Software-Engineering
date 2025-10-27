
n = int(input("Введите количество строк (n): "))
m = int(input("Введите количество столбцов (m): "))

print("\n=== Прямоугольник ===")
for i in range(n):
    for j in range(m):
        print('*', end='')
    print()

print("\n=== Правый треугольник ===")
for i in range(1, n + 1):
    for j in range(i):
        print('*', end='')
    print()

print("\n=== Рамка ===")
for i in range(n):
    for j in range(m):
        if i == 0 or i == n - 1 or j == 0 or j == m - 1:
            print('*', end='')
        else:
            print(' ', end='')
    print()