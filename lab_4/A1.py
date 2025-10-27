import time
import random

while True:
    try:
        n = int(input('Введите количество примеров: '))
        if n <= 0:
            print("Введите положительное число!")
            continue
        break
    except ValueError:
        print("Пожалуйста, введите целое число!")

correct_answers = 0
times = []

print()

for i in range(1, n + 1):
    a = random.randint(2, 9)
    b = random.randint(2, 9)

    print(f"Вопрос {i}/{n}")
    while True:
        start_time = time.time()
        user_input = input(f"{a} × {b} = ")

        try:
            answer = int(user_input)
            elapsed = round(time.time() - start_time, 1)
            times.append(elapsed)

            if answer == a * b:
                print(f"Верно! (Время: {elapsed} сек)\n")
                correct_answers += 1
            else:
                print(f"Неверно! Правильно: {a * b} (Время: {elapsed} сек)\n")
            break
        except ValueError:
            print("Пожалуйста, введите целое число!")

total_time = round(sum(times), 1)
avg_time = round(total_time / len(times), 1) if times else 0
percent = round(correct_answers / n * 100, 1)

print("=" * 50)
print("СТАТИСТИКА:")
print("=" * 50)
print(f"Общее время: {total_time} сек")
print(f"Среднее время на вопрос: {avg_time} сек")
print(f"Правильных ответов: {correct_answers}/{n}")
print(f"Процент правильных: {percent}%")