"""Проверка требований лабораторной работы средствами unittest."""
import io
import unittest
from contextlib import redirect_stdout
from itertools import product

from main import BacteriaProducer
from task2 import MushroomsCollector


def output_of(action, *args):
    stream = io.StringIO()
    with redirect_stdout(stream):
        action(*args)
    return stream.getvalue()


class BacteriaTests(unittest.TestCase):
    def test_initial_state(self):
        colony = BacteriaProducer(3)
        self.assertEqual(colony.max_bacteria, 3)
        self.assertEqual(colony.current_bacteria_count, 0)

    def test_create_and_limit_messages(self):
        colony = BacteriaProducer(1)
        self.assertEqual(output_of(colony.create),
                         'Добавлена одна бактерия. Бактерий в колонии: 1\n')
        self.assertEqual(output_of(colony.create), 'Нет места под новую бактерию\n')
        self.assertEqual(colony.current_bacteria_count, 1)

    def test_delete_and_empty_messages(self):
        colony = BacteriaProducer(1)
        output_of(colony.create)
        self.assertEqual(output_of(colony.delete),
                         'Одна бактерия удалена. Бактерий в колонии: 0\n')
        self.assertEqual(output_of(colony.delete),
                         'В популяции нет бактерий, удалять нечего\n')
        self.assertEqual(colony.current_bacteria_count, 0)

    def test_zero_capacity(self):
        colony = BacteriaProducer(0)
        self.assertEqual(output_of(colony.create), 'Нет места под новую бактерию\n')
        output_of(colony.delete)
        self.assertEqual(colony.current_bacteria_count, 0)

    def test_independent_colonies(self):
        first, second = BacteriaProducer(1), BacteriaProducer(2)
        output_of(first.create)
        self.assertEqual(second.current_bacteria_count, 0)
        self.assertEqual(second.max_bacteria, 2)

    def test_all_operation_sequences(self):
        # 4 вместимости × 256 последовательностей × 8 операций.
        for capacity in range(4):
            for sequence in product(('create', 'delete'), repeat=8):
                colony = BacteriaProducer(capacity)
                expected = 0
                for operation in sequence:
                    expected = (min(capacity, expected + 1) if operation == 'create'
                                else max(0, expected - 1))
                    output_of(getattr(colony, operation))
                    self.assertEqual(colony.current_bacteria_count, expected)


class MushroomTests(unittest.TestCase):
    def test_empty_basket(self):
        basket = MushroomsCollector()
        self.assertEqual(basket.mushrooms, [])
        self.assertEqual(str(basket), '')

    def test_poisonous_names(self):
        basket = MushroomsCollector()
        for name in ('Мухомор', 'Поганка'):
            self.assertIs(basket.is_poisonous(name), True)
            self.assertEqual(output_of(basket.add_mushroom, name),
                             'Нельзя добавить ядовитый гриб\n')
        self.assertEqual(basket.mushrooms, [])

    def test_edible_names_and_order(self):
        basket = MushroomsCollector()
        for name in ('Подосиновик', 'Белый', 'Лисичка'):
            self.assertIs(basket.is_poisonous(name), False)
            self.assertEqual(output_of(basket.add_mushroom, name), '')
        self.assertEqual(str(basket), 'Подосиновик, Белый, Лисичка')

    def test_independent_baskets(self):
        first, second = MushroomsCollector(), MushroomsCollector()
        first.add_mushroom('Белый')
        second.add_mushroom('Лисичка')
        self.assertIsNot(first.mushrooms, second.mushrooms)
        self.assertEqual(first.mushrooms, ['Белый'])
        self.assertEqual(second.mushrooms, ['Лисичка'])

    def test_repeated_mushrooms(self):
        basket = MushroomsCollector()
        basket.add_mushroom('Белый')
        basket.add_mushroom('Белый')
        self.assertEqual(str(basket), 'Белый, Белый')

    def test_rejection_preserves_contents(self):
        basket = MushroomsCollector()
        basket.add_mushroom('Белый')
        output_of(basket.add_mushroom, 'Поганка')
        self.assertEqual(str(basket), 'Белый')


if __name__ == '__main__':
    unittest.main(verbosity=2)
