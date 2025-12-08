import matplotlib.pyplot as plt
import seaborn as sns
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
sns.set_style("whitegrid")

def load_users_data(file_path):
    """
    Загружает пользователей из XML файла.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    users = {}
    for user in root.findall('user'):
        uid = int(user.find('user_id').text)  # берем id из тега <user_id>
        users[uid] = {
            'name': user.find('name').text,
            'age': int(user.find('age').text),
            'weight': int(user.find('weight').text),
            'level': user.find('fitness_level').text  # тег теперь fitness_level
        }
    return users

def load_workouts_data(file_path):
    """
    Загружает тренировки из XML файла.Возвращает список словарей по одной тренировке на элемент.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    workouts = []
    for w in root.findall('workout'):
        workouts.append({
            'id': int(w.find('workout_id').text),
            'user_id': int(w.find('user_id').text),
            'date': w.find('date').text,
            'type': w.find('type').text,
            'duration': int(w.find('duration').text),
            'distance': float(w.find('distance').text),
            'calories': int(w.find('calories').text),
            'heart_rate': int(w.find('avg_heart_rate').text),  # теперь avg_heart_rate
            'intensity': w.find('intensity').text
        })
    return workouts


def get_stats(users, workouts):
    """
    Рассчитывает общую статистику
    """
    total_workouts = len(workouts)
    total_users = len(users)
    total_calories = sum(w['calories'] for w in workouts)
    total_time_hours = sum(w['duration'] for w in workouts) / 60
    total_distance = sum(w['distance'] for w in workouts)

    print("ОБЩАЯ СТАТИСТИКА")
    print("===========================")
    print(f"Всего тренировок: {total_workouts}")
    print(f"Всего пользователей: {total_users}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {total_time_hours:.1f} часов")
    print(f"Пройдено дистанции: {total_distance:.1f} км")




# ----------------------------
# Функция 1: ТОП-3 самых активных пользователей
# ----------------------------
def analyze_user_activity(users, workouts):
    """
    Выводит ТОП-3 самых активных пользователей по количеству тренировок
    """
    stats = {}
    for uid, info in users.items():
        user_workouts = [w for w in workouts if w['user_id'] == uid]
        total_sessions = len(user_workouts)
        total_calories = sum(w['calories'] for w in user_workouts)
        total_hours = sum(w['duration'] for w in user_workouts) / 60
        stats[uid] = {
            'name': info['name'],
            'level': info['level'],
            'sessions': total_sessions,
            'calories': total_calories,
            'hours': total_hours
        }

    top3 = sorted(stats.values(), key=lambda x: x['sessions'], reverse=True)[:3]

    print("ТОП-3 АКТИВНЫХ ПОЛЬЗОВАТЕЛЕЙ:")
    for i, u in enumerate(top3, 1):
        print(f" {i}. {u['name']} ({u['level']}):")
        print(f"    Тренировок: {u['sessions']}")
        print(f"    Калорий: {u['calories']}")
        print(f"    Время: {u['hours']:.1f} часов")
    print()

# ----------------------------
# Функция 2: Распределение по типам тренировок
# ----------------------------
def analyze_workout_types(workouts):
    """
    Выводит статистику по каждому типу тренировки:
    """
    total_workouts = len(workouts)
    type_stats = defaultdict(list)

    for w in workouts:
        type_stats[w['type']].append(w)

    print("РАСПРЕДЕЛЕНИЕ ПО ТИПАМ ТРЕНИРОВОК:")
    for t, wlist in type_stats.items():
        count = len(wlist)
        percent = count / total_workouts * 100
        avg_duration = sum(w['duration'] for w in wlist) / count
        avg_calories = sum(w['calories'] for w in wlist) / count
        print(f" {t.capitalize()}: {count} тренировок ({percent:.1f}%)")
        print(f"   Средняя длительность: {avg_duration:.0f} мин")
        print(f"   Средние калории: {avg_calories:.0f} ккал")
    print()

# ----------------------------
# Функция 3: Найти все тренировки пользователя по имени
# ----------------------------
def find_user_workouts(users, workouts, user_name):
    """
    Возвращает список тренировок пользователя по имени
    """
    # находим user_id по имени
    uid = None
    for id_, info in users.items():
        if info['name'].lower() == user_name.lower():
            uid = id_
            break
    if uid is None:
        return []
    return [w for w in workouts if w['user_id'] == uid]

# ----------------------------
# Функция 4: Детальный анализ пользователя
# ----------------------------
def analyze_user(users, workouts, user_name):
    user = None
    for u in users.values():
        if u['name'].lower() == user_name.lower():
            user = u
            break
    if user is None:
        print(f"Пользователь {user_name} не найден")
        return

    user_workouts = find_user_workouts(users, workouts, user_name)
    total_sessions = len(user_workouts)
    total_calories = sum(w['calories'] for w in user_workouts)
    total_hours = sum(w['duration'] for w in user_workouts) / 60
    total_distance = sum(w['distance'] for w in user_workouts)
    avg_calories = total_calories / total_sessions if total_sessions else 0

    # любимый тип тренировки
    type_counts = Counter(w['type'] for w in user_workouts)
    favorite_type = type_counts.most_common(1)[0][0] if type_counts else "нет"

    print(f"ДЕТАЛЬНЫЙ АНАЛИЗ ДЛЯ ПОЛЬЗОВАТЕЛЯ: {user_name}")
    print("===========================================")
    print(f"Возраст: {user['age']} лет, Вес: {user['weight']} кг")
    print(f"Уровень: {user['level']}")
    print(f"Тренировок: {total_sessions}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {total_hours:.1f} часов")
    print(f"Пройдено дистанции: {total_distance:.1f} км")
    print(f"Средние калории за тренировку: {avg_calories:.0f}")
    print(f"Любимый тип тренировки: {favorite_type}")
    print()



def plot_workout_types(workouts):
    type_counts = Counter(w['type'] for w in workouts)
    labels = [t.capitalize() for t in type_counts.keys()]
    sizes = list(type_counts.values())

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Распределение по типам тренировок")
    plt.show()

def plot_user_activity(users, workouts):
    activity = defaultdict(int)
    for w in workouts:
        activity[w['user_id']] += 1

    names = [users[uid]['name'] for uid in activity.keys()]
    counts = [activity[uid] for uid in activity.keys()]

    plt.figure(figsize=(10, 6))
    plt.bar(names, counts, color='skyblue')
    plt.title("Активность пользователей (кол-во тренировок)")
    plt.ylabel("Количество тренировок")
    plt.xlabel("Пользователи")
    plt.xticks(rotation=45)
    plt.show()





def plot_workout_efficiency_per_min(workouts):
    type_stats = defaultdict(list)
    for w in workouts:
        if w['duration'] > 0:
            type_stats[w['type']].append(w['calories'] / w['duration'])

    types = [t.capitalize() for t in type_stats.keys()]
    avg_calories_per_min = [sum(vals)/len(vals) for vals in type_stats.values()]

    plt.figure(figsize=(10, 6))
    plt.bar(types, avg_calories_per_min, color='purple')
    plt.title("Эффективность тренировок (калории за минуту)")
    plt.ylabel("Калории/мин")
    plt.xlabel("Тип тренировки")
    plt.show()

def plot_user_calories(users, workouts):
    calories_data = defaultdict(int)
    for w in workouts:
        calories_data[w['user_id']] += w['calories']

    names = []
    calories = []
    colors = []

    level_color = {
        'продвинутый': 'red',
        'средний': 'orange',
        'начальный': 'green'
    }

    for uid, total_cal in calories_data.items():
        names.append(users[uid]['name'])
        calories.append(total_cal)
        colors.append(level_color.get(users[uid]['level'], 'gray'))

    plt.figure(figsize=(10, 6))
    plt.bar(names, calories, color=colors)
    plt.title("Общие затраченные калории пользователями")
    plt.ylabel("Калории")
    plt.xlabel("Пользователи")
    plt.xticks(rotation=45)

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='Продвинутый'),
        Patch(facecolor='orange', label='Средний'),
        Patch(facecolor='green', label='Начальный')
    ]
    plt.legend(handles=legend_elements, title="Уровень пользователя")
    plt.show()
if __name__ == "__main__":
    users = load_users_data('users.xml')
    workouts = load_workouts_data('workouts.xml')
    get_stats(users, workouts)

    analyze_user_activity(users, workouts)
    analyze_workout_types(workouts)
    analyze_user(users,workouts,"Борис")

    plot_workout_types(workouts)
    plot_user_activity(users, workouts)
    plot_workout_efficiency_per_min(workouts)
    plot_user_calories(users, workouts)