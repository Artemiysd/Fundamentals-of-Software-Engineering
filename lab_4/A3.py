
while True:
    data = input("Введите последовательность из 0 и 1 (не короче 5 символов): ").strip()

    if len(data) < 5:
        print("Ошибка: строка должна быть не меньше 5 символов.")
        continue
    if not all(ch in "01" for ch in data):
        print("Ошибка: можно вводить только символы 0 и 1.")
        continue
    break

total_packets = len(data)

lost_packets = data.count('0')

max_lost_streak = max(len(streak) for streak in data.split('1'))

loss_percent = round(lost_packets / total_packets * 100, 1)

if loss_percent <= 1:
    quality = "Отличное качество"
elif loss_percent <= 5:
    quality = "Хорошее качество"
elif loss_percent <= 10:
    quality = "Удовлетворительное качество"
elif loss_percent <= 20:
    quality = "Плохое качество"
else:
    quality = "Критическое состояние сети"

print("\nРЕЗУЛЬТАТ АНАЛИЗА:")
print(f"• Общее количество пакетов: {total_packets}")
print(f"• Количество потерянных пакетов: {lost_packets}")
print(f"• Длина самой длинной последовательности потерянных пакетов: {max_lost_streak}")
print(f"• Процент потерь: {loss_percent}%")
print(f"• Качество связи: {quality}")