from itertools import combinations


ITEMS = [
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

START_SCORE = 10
TOTAL_VALUE = sum(item["value"] for item in ITEMS)


def calculate_score(selected):
    taken_value = sum(item["value"] for item in selected)
    # Взятые вещи прибавляются, оставленные вычитаются:
    # start + taken - (total - taken) = start + 2 * taken - total.
    return START_SCORE + 2 * taken_value - TOTAL_VALUE


def get_combinations(capacity):
    valid_combinations = []

    for count in range(len(ITEMS) + 1):
        for selected in combinations(ITEMS, count):
            used_cells = sum(item["size"] for item in selected)
            if used_cells <= capacity:
                valid_combinations.append(list(selected))

    return valid_combinations


def find_best_combination(capacity):
    best_selected = []
    best_score = calculate_score(best_selected)

    for selected in get_combinations(capacity):
        score = calculate_score(selected)
        if score > best_score:
            best_selected = selected
            best_score = score

    return best_selected, best_score


def find_positive_combinations(capacity):
    positive = []

    for selected in get_combinations(capacity):
        score = calculate_score(selected)
        if score > 0:
            positive.append((selected, score))

    return positive


def build_inventory(selected, rows, columns):
    cells = []

    for item in selected:
        for _ in range(item["size"]):
            cells.append(item["symbol"])

    while len(cells) < rows * columns:
        cells.append(" ")

    inventory = []
    for row_number in range(rows):
        row_start = row_number * columns
        inventory.append(cells[row_start:row_start + columns])

    return inventory


def print_inventory(inventory):
    for row in inventory:
        print(",".join(f"[{cell}]" for cell in row))


def symbols_text(selected):
    return " ".join(item["symbol"] for item in selected)


def main():
    best_selected, best_score = find_best_combination(9)

    print("Лучший инвентарь 3x3:")
    print_inventory(build_inventory(best_selected, 3, 3))
    print(f"Итоговые очки выживания: {best_score}")
    print("Итоговый счёт положительный:", "да" if best_score > 0 else "нет")

    positive = find_positive_combinations(9)
    print("\nВсе положительные комбинации для 9 ячеек:")
    for number in range(len(positive)):
        selected, score = positive[number]
        print(f"{number + 1}. [{symbols_text(selected)}], очки: {score}")
    print(f"Всего положительных комбинаций: {len(positive)}")

    best_for_seven, score_for_seven = find_best_combination(7)
    positive_for_seven = find_positive_combinations(7)
    print("\nПроверка инвентаря на 7 ячеек:")
    print(f"Лучший набор: [{symbols_text(best_for_seven)}]")
    print(f"Лучший счёт для 7 ячеек: {score_for_seven}")
    if positive_for_seven:
        print("Для 7 ячеек есть положительные решения.")
    else:
        print("Для 7 ячеек положительных решений нет.")
        print("Полный перебор всех наборов показал, что лучший счёт не положительный.")


if __name__ == "__main__":
    main()
