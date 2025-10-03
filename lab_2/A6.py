totalseconds = int(input('Сколько секунд прошло: '))

newHours = totalseconds // 3600
newMinutes = (totalseconds % 3600) // 60
newSeconds = totalseconds % 60

print(f'{newHours:02d}:{newMinutes:02d}:{newSeconds:02d}')