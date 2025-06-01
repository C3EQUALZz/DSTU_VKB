from typing import Final

from app.exceptions.app import global_exception_handler
from app.presenters.tasks.base import ITaskPresenter
from app.presenters.tasks.comparison_of_the_first_degree.impl import ComparisonOfFirstDegreePresenter
from app.presenters.tasks.continued_fractions.impl import ContinuedFractionPresenter
from app.presenters.tasks.euclidian_algorithms.impl import GCDCalculatorPresenter
from app.presenters.tasks.legendre_and_jacobi_symbols.impl import LegendreJacobiPresenter
from app.presenters.tasks.legendre_symbol.impl import LegendrePresenter
from app.presenters.tasks.quadratic_comparison.impl import QuadraticComparisonPresenter
from app.presenters.tasks.remainder_division.impl import RemainderDivisionPresenter
from app.presenters.tasks.system_of_comprasion_of_the_first_degree.impl import CRTPresenter
from app.views.application.application import Application
from app.views.tasks.base import ITaskView
from app.views.tasks.comparison_of_the_first_degree.impl import ComparisonOfFirstDegreeView
from app.views.tasks.continued_fractions.impl import ContinuedFractionView
from app.views.tasks.euclidian_algorithms.impl import GCDView
from app.views.tasks.legendre_and_jacobi_symbols.impl import LegendreJacobiView
from app.views.tasks.legendre_symbol.impl import LegendreView
from app.views.tasks.quadratic_comparison.impl import QuadraticComparisonView
from app.views.tasks.remainder_division.impl import RemainderDivisionView
from app.views.tasks.system_of_comprasion_of_the_first_degree.impl import CRTView

TASKS: Final[dict[str, tuple[type[ITaskPresenter], type[ITaskView]]]] = {
    "Алгоритм Евклида": (GCDCalculatorPresenter, GCDView),
    "Остаток от деления": (RemainderDivisionPresenter, RemainderDivisionView),
    "Сравнение 1 степени": (ComparisonOfFirstDegreePresenter, ComparisonOfFirstDegreeView),
    "Сис. сравн. 1 степени": (CRTPresenter, CRTView),
    "Сим. Лежандра, Якоби": (LegendreJacobiPresenter, LegendreJacobiView),
    "Сим. Лежандра": (LegendrePresenter, LegendreView),
    "Квадратичное сравн.": (QuadraticComparisonPresenter, QuadraticComparisonView),
    "Непрерывные дроби": (ContinuedFractionPresenter, ContinuedFractionView)
}

if __name__ == "__main__":
    app = Application(TASKS)
    app.report_callback_exception = global_exception_handler
    app.mainloop()
