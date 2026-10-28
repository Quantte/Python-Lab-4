from itertools import combinations
from typing import TypedDict


class Item(TypedDict):
    name: str
    symbol: str
    size: int  # сколько ячеек занимает
    value: int  # очки выживания


Inventory = list[list[str]]  # таблица rows x columns из символов предметов

ITEMS: list[Item] = [
    {"name": "Винтовка", "symbol": "r", "size": 3, "value": 25},
    {"name": "Пистолет", "symbol": "p", "size": 2, "value": 15},
    {"name": "Боекомплект", "symbol": "a", "size": 2, "value": 15},
    {"name": "Аптечка", "symbol": "m", "size": 2, "value": 20},
    {"name": "Ингалятор", "symbol": "i", "size": 1, "value": 5},
    {"name": "Нож", "symbol": "k", "size": 1, "value": 15},
    {"name": "Топор", "symbol": "x", "size": 3, "value": 20},
    {"name": "Оберег", "symbol": "t", "size": 1, "value": 25},
    {"name": "Фляжка", "symbol": "f", "size": 1, "value": 15},
    {"name": "Антидот", "symbol": "d", "size": 1, "value": 10},
    {"name": "Еда", "symbol": "s", "size": 2, "value": 20},
    {"name": "Арбалет", "symbol": "c", "size": 2, "value": 20},
]

START_SCORE: int = 10
TOTAL_VALUE: int = sum(item["value"] for item in ITEMS)


def calculate_score(selected: list[Item]) -> int:
    taken_value = sum(item["value"] for item in selected)
    # Взятые вещи прибавляются, оставленные вычитаются:
    # start + taken - (total - taken) = start + 2 * taken - total.
    return START_SCORE + 2 * taken_value - TOTAL_VALUE


def get_combinations(capacity: int) -> list[list[Item]]:
    valid_combinations: list[list[Item]] = []

    for count in range(len(ITEMS) + 1):
        for selected in combinations(ITEMS, count):
            used_cells = sum(item["size"] for item in selected)
            if used_cells <= capacity:
                valid_combinations.append(list(selected))

    return valid_combinations


def find_best_combination(capacity: int) -> tuple[list[Item], int]:
    best_selected: list[Item] = []
    best_score = calculate_score(best_selected)

    for selected in get_combinations(capacity):
        score = calculate_score(selected)
        if score > best_score:
            best_selected = selected
            best_score = score

    return best_selected, best_score


def find_positive_combinations(capacity: int) -> list[tuple[list[Item], int]]:
    positive: list[tuple[list[Item], int]] = []

    for selected in get_combinations(capacity):
        score = calculate_score(selected)
        if score > 0:
            positive.append((selected, score))

    return positive


def build_inventory(selected: list[Item], rows: int, columns: int) -> Inventory:
    # Каждый символ — одна ячейка; пустые ячейки добиваются пробелами.
    cells = "".join(item["symbol"] * item["size"] for item in selected).ljust(rows * columns)
    return [list(cells[start:start + columns]) for start in range(0, rows * columns, columns)]


def print_inventory(inventory: Inventory) -> None:
    for row in inventory:
        print(",".join(f"[{cell}]" for cell in row))


def main() -> None:
    best_selected, best_score = find_best_combination(3 * 3)

    print("Лучший инвентарь 3x3:")
    print_inventory(build_inventory(best_selected, 3, 3))
    print(f"Итоговые очки выживания: {best_score}")

    best_for_seven, score_for_seven = find_best_combination(7)
    positive_for_seven = find_positive_combinations(7)
    print("\nПроверка инвентаря на 7 ячеек:")
    print("Лучший набор: ")
    print_inventory(build_inventory(best_for_seven, 1, 7))
    print(f"Лучший счёт для 7 ячеек: {score_for_seven}")
    if not positive_for_seven:
        print("Для 7 ячеек положительных решений нет.")
        print("Полный перебор всех наборов показал, что лучший счёт не положительный.")

    positive = find_positive_combinations(9)
    print("\nВсе положительные комбинации для 9 ячеек:")
    for number, (selected, score) in enumerate(positive, start=1):
        print(f'{number}. [{" ".join(item["symbol"] for item in selected)}], очки: {score}')
    print(f"Всего положительных комбинаций: {len(positive)}")

if __name__ == "__main__":
    main()
