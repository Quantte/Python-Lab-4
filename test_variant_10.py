import contextlib
import io
import unittest

import variant_10


REFERENCE_ITEMS = [
    ("r", 3, 25),
    ("p", 2, 15),
    ("a", 2, 15),
    ("m", 2, 20),
    ("i", 1, 5),
    ("k", 1, 15),
    ("x", 3, 20),
    ("t", 1, 25),
    ("f", 1, 15),
    ("d", 1, 10),
    ("s", 2, 20),
    ("c", 2, 20),
]
START_SCORE = 10
TOTAL_VALUE = sum(item[2] for item in REFERENCE_ITEMS)


def reference_combinations(capacity):
    combinations = []

    for mask in range(2 ** len(REFERENCE_ITEMS)):
        symbols = []
        size = 0
        taken_value = 0

        for index in range(len(REFERENCE_ITEMS)):
            if mask & (1 << index):
                symbol, item_size, value = REFERENCE_ITEMS[index]
                symbols.append(symbol)
                size += item_size
                taken_value += value

        if size <= capacity:
            score = START_SCORE + 2 * taken_value - TOTAL_VALUE
            combinations.append((tuple(symbols), size, score))

    return combinations


class Variant10Tests(unittest.TestCase):
    def test_formula_uses_taken_and_left_items(self):
        selected = [variant_10.ITEMS[0], variant_10.ITEMS[7]]
        taken_value = 25 + 25

        score = variant_10.calculate_score(selected)

        self.assertEqual(score, START_SCORE + 2 * taken_value - TOTAL_VALUE)

    def test_best_combination_for_nine_cells_matches_full_enumeration(self):
        reference = reference_combinations(9)
        expected_symbols, expected_size, expected_score = max(
            reference, key=lambda combination: combination[2]
        )

        selected, score = variant_10.find_best_combination(9)
        symbols = tuple(item["symbol"] for item in selected)
        size = sum(item["size"] for item in selected)

        self.assertEqual((symbols, size, score),
                         (expected_symbols, expected_size, expected_score))
        self.assertEqual(symbols, ("m", "k", "t", "f", "s", "c"))
        self.assertEqual(score, 35)

    def test_inventory_is_three_by_three_and_uses_item_symbols(self):
        selected, _ = variant_10.find_best_combination(9)

        inventory = variant_10.build_inventory(selected, 3, 3)

        self.assertEqual(len(inventory), 3)
        self.assertTrue(all(len(row) == 3 for row in inventory))
        cells = [cell for row in inventory for cell in row]
        expected_cells = []
        for item in selected:
            expected_cells.extend([item["symbol"]] * item["size"])
        self.assertEqual(cells, expected_cells)

    def test_all_positive_nine_cell_combinations_match_full_enumeration(self):
        expected = {
            (symbols, score)
            for symbols, _size, score in reference_combinations(9)
            if score > 0
        }

        actual = {
            (tuple(item["symbol"] for item in selected), score)
            for selected, score in variant_10.find_positive_combinations(9)
        }

        self.assertEqual(actual, expected)

    def test_seven_cells_have_no_positive_solution_and_optimum_is_minus_five(self):
        reference = reference_combinations(7)
        expected_score = max(combination[2] for combination in reference)
        optimal_symbols = {
            symbols
            for symbols, _size, score in reference
            if score == expected_score
        }

        selected, score = variant_10.find_best_combination(7)
        symbols = tuple(item["symbol"] for item in selected)

        self.assertEqual(score, expected_score)
        self.assertIn(symbols, optimal_symbols)
        self.assertEqual(score, -5)
        self.assertEqual(variant_10.find_positive_combinations(7), [])

    def test_main_prints_required_results(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            variant_10.main()

        text = output.getvalue()
        positive_count = len([
            combination for combination in reference_combinations(9)
            if combination[2] > 0
        ])
        self.assertIn("Итоговые очки выживания: 35", text)
        self.assertIn("Итоговый счёт положительный: да", text)
        self.assertIn(f"Всего положительных комбинаций: {positive_count}", text)
        self.assertIn("Для 7 ячеек положительных решений нет.", text)
        self.assertIn("Лучший счёт для 7 ячеек: -5", text)


if __name__ == "__main__":
    unittest.main()
