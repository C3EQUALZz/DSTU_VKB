import pytest
from python_language.probability_theory_and_mathematical_statistics.second_test_work.main import DataInteraction

data = [*range(1000)]


def test_slice_all_elems():
    """
    Проверка того, что правильно берутся все элементы генеральной совокупности.
    """

    data_interaction = DataInteraction(data, slice(0, len(data)), "Генеральная совокупность", chart_histogram=False,
                                       chart_frequency_range=False)

    assert len(data_interaction.data) == 1000, "Неправильный срез в первом задании"


def test_slice_are_taken_after_1():
    """
    Выборка состоит из элементов ГС, которые берутся через 1
    """

    data_interaction = DataInteraction(data, slice(0, len(data), 2), "Выборка через 1", chart_histogram=False,
                                       chart_frequency_range=False)

    assert len(data_interaction.data) == 500, "Неправильный срез во втором задании"


def test_slice_are_taken_from_1_through_3():
    """
    Выборка состоит из элементов ГС, которые берутся через 3, начиная с 1
    """

    data_interaction = DataInteraction(data, slice(1, len(data), 3), "Выборка через 1", chart_histogram=False,
                                       chart_frequency_range=False)

    assert len(data_interaction.data) == 333, "Неправильный срез в третьем задании"


if __name__ == '__main__':
    pytest.main()
