prev_reading = int(input("Введите предыдущее показание счетчика: "))
curr_reading = int(input("Введите текущее показание счетчика: "))

MAX_READING = 10000

if curr_reading >= prev_reading:
    used = curr_reading - prev_reading
else:
    used = (MAX_READING - prev_reading) + curr_reading

if used <= 300:
    cost = 21
elif used <= 600:
    cost = 21 + (used - 300) * 0.06
elif used <= 800:
    cost = 21 + 300 * 0.06 + (used - 600) * 0.04
else:
    cost = 21 + 300 * 0.06 + 200 * 0.04 + (used - 800) * 0.025

avg_price = cost / used if used > 0 else 0

print("\n" + "-" * 40)
print(f"{'Показатель':<25}{'Значение':>15}")
print("-" * 40)
print(f"{'Предыдущее показание:':<25}{prev_reading:>15}")
print(f"{'Текущее показание:':<25}{curr_reading:>15}")
print(f"{'Израсходовано газа:':<25}{used:>15} м³")
print(f"{'Сумма к оплате:':<25}{cost:>14.2f} $")
print(f"{'Средняя цена за м³:':<25}{avg_price:>14.2f} $")
print("-" * 40)
