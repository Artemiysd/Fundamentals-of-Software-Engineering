#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Tuple, List


AUTHOR = "Gurin Artemiy"
TITLE_RU = "Генетический поиск"
SEPARATOR = "-" * 74  # Разделитель между операциями
SEQUENCES_FILE = "sequences.0.txt"  # Файл с белками
COMMANDS_FILE = "commands.0.txt"     # Файл с командами
OUTPUT_FILE = "genedata.0.txt"       # Файл, куда программа пишет результат


# --------------------------------------------------------
# ДЕКОДИРОВАНИЕ RLE ("3A" → "AAA")
# --------------------------------------------------------
def decode_rle(s: str) -> str:
    """
    Декодирует RLE-формат.
    Цифры 3..9 означают количество повторов следующего символа.
    Если цифра стоит в конце строки или после неё нет символа —
    просто добавляется как обычный символ.
    """
    result = []
    i = 0
    n = len(s)

    while i < n:
        c = s[i]

        # Проверяем, является ли символ цифрой от 3 до 9
        # и есть ли следующий символ
        if c.isdigit() and '3' <= c <= '9' and (i + 1) < n:
            count = ord(c) - ord('0')  # преобразуем символ цифры в число
            result.append(s[i + 1] * count)  # повторяем следующий символ count раз
            i += 2  # пропускаем цифру и символ
        else:
            result.append(c)  # обычный символ без кодирования
            i += 1

    return "".join(result)


# --------------------------------------------------------
# ЧТЕНИЕ ФАЙЛА С БЕЛКАМИ
# --------------------------------------------------------
def load_sequences(path: str) -> Dict[str, Tuple[str, str]]:
    """
    Загружает sequences.txt.
    Каждая строка имеет формат:
        <имя белка> <организм> <цепочка>
    Возвращает словарь:
        { protein_name : (organism, decoded_chain) }
    """
    proteins = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:  # пропускаем пустые строки
                continue

            parts = line.split("\t")

            if len(parts) < 3:
                continue  # пропускаем ошибки в файле

            name = parts[0].strip()
            organism = parts[1].strip()
            chain_raw = parts[2].strip()

            chain = decode_rle(chain_raw)  # декодируем цепочку

            proteins[name] = (organism, chain)

    return proteins


# --------------------------------------------------------
# ЧТЕНИЕ КОМАНД ИЗ commands.txt
# --------------------------------------------------------
def parse_commands(path: str) -> List[List[str]]:
    """
    Читает команды.
    Каждая строка имеет формат:
        search   SIIK
        diff     A   B
        mode     C
    Возвращает список списков: ["search", "SIIK"]
    """
    cmds = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            parts = line.split("\t")
            # убираем пустые элементы и пробелы
            cmds.append([p.strip() for p in parts if p.strip() != ""])

    return cmds


# --------------------------------------------------------
# ОПЕРАЦИЯ SEARCH
# --------------------------------------------------------
def cmd_search(proteins: Dict[str, Tuple[str, str]], pattern_raw: str):
    """
    Ищет фрагмент в цепочке белка.
    Возвращает список (организм, белок), где найден паттерн.
    """
    pattern = decode_rle(pattern_raw)
    found = []

    # перебираем все белки
    for pname, (org, chain) in proteins.items():
        if pattern in chain:  # ищем подстроку
            found.append((org, pname))

    return found


# --------------------------------------------------------
# ОПЕРАЦИЯ DIFF
# --------------------------------------------------------
def cmd_diff(proteins: Dict[str, Tuple[str, str]], name1: str, name2: str):
    """
    Считает различия между двумя белками.
    Различия = количество несовпадающих аминокислот + разница длин.
    """
    missing = []

    # проверка существования белков
    if name1 not in proteins:
        missing.append(name1)
    if name2 not in proteins:
        missing.append(name2)

    if missing:
        return False, "MISSING: " + ", ".join(missing)

    chain1 = proteins[name1][1]
    chain2 = proteins[name2][1]

    minlen = min(len(chain1), len(chain2))

    # считаем отличия по символам
    diffs = sum(1 for i in range(minlen) if chain1[i] != chain2[i])

    # добавляем разницу длин
    diffs += abs(len(chain1) - len(chain2))

    return True, str(diffs)


# --------------------------------------------------------
# ОПЕРАЦИЯ MODE
# --------------------------------------------------------
def cmd_mode(proteins: Dict[str, Tuple[str, str]], name: str):
    """
    Находит наиболее частую аминокислоту.
    Если частоты равны — выбирается буква по алфавиту.
    """
    if name not in proteins:
        return False, "MISSING: " + name

    chain = proteins[name][1]
    freq = {}

    # считаем количество каждой аминокислоты
    for c in chain:
        freq[c] = freq.get(c, 0) + 1

    max_count = max(freq.values())

    # выбираем символы, имеющие максимальную частоту
    candidates = sorted([c for c, cnt in freq.items() if cnt == max_count])

    chosen = candidates[0]  # алфавитно первый

    return True, f"{chosen}\t{max_count}"


# --------------------------------------------------------
# ФОРМАТИРОВАНИЕ ВЫВОДА ДЛЯ SEARCH
# --------------------------------------------------------
def format_search_output(found):
    """
    Возвращает строки вывода для операции search.
    """
    if not found:
        return ["NOT FOUND"]

    out = []
    out.append("organism\t\t\tprotein")

    for org, pname in found:
        out.append(f"{org}\t\t{pname}")

    return out


# --------------------------------------------------------
# ГЛАВНАЯ ФУНКЦИЯ
# --------------------------------------------------------
def main():
    # загружаем белки
    proteins = load_sequences(SEQUENCES_FILE)

    # читаем команды
    commands = parse_commands(COMMANDS_FILE)

    # формируем строки результата
    lines_out = []

    # первые две строки — имя + заголовок
    lines_out.append(AUTHOR)
    lines_out.append(TITLE_RU)
    lines_out.append(SEPARATOR)

    # обрабатываем команды по очереди
    for idx, cmd_parts in enumerate(commands, start=1):
        op = cmd_parts[0].lower()

        # Формируем строку вида:
        # "001   search   SIIK"
        if op == "search" and len(cmd_parts) >= 2:
            header_param = decode_rle(cmd_parts[1])
        elif op == "diff" and len(cmd_parts) >= 3:
            header_param = f"{cmd_parts[1]}\t{cmd_parts[2]}"
        elif op == "mode" and len(cmd_parts) >= 2:
            header_param = cmd_parts[1]
        else:
            header_param = "\t".join(cmd_parts[1:])

        lines_out.append(f"{idx:03d}   {op:<5}   {header_param} ")

        # ---------------------------
        # Выполняем нужную операцию
        # ---------------------------
        if op == "search":
            found = cmd_search(proteins, cmd_parts[1])
            lines_out.extend(format_search_output(found))

        elif op == "diff":
            ok, res = cmd_diff(proteins, cmd_parts[1], cmd_parts[2])
            lines_out.append("amino-acids difference:")
            lines_out.append(res)

        elif op == "mode":
            ok, res = cmd_mode(proteins, cmd_parts[1])
            lines_out.append("amino-acid occurs:")
            if not ok:
                lines_out.append(res)
            else:
                sym, cnt = res.split("\t")
                lines_out.append(f"{sym}\t{cnt}")

        else:
            lines_out.append("UNKNOWN COMMAND")

        lines_out.append(SEPARATOR)

    # --------------------------------------------------------
    # Записываем результат в файл
    # --------------------------------------------------------
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for ln in lines_out:
            out.write(ln + "\n")


# --------------------------------------------------------
# ТОЧКА ВХОДА
# --------------------------------------------------------
if __name__ == "__main__":
    main()