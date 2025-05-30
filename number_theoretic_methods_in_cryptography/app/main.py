from typing import Final

from app.exceptions.app import global_exception_handler
from app.presenters.tasks.base import ITaskPresenter
from app.presenters.tasks.comparison_of_the_first_degree.impl import ComparisonOfFirstDegreePresenter
from app.presenters.tasks.euclidian_algorithms.impl import GCDCalculatorPresenter
from app.presenters.tasks.remainder_division.impl import RemainderDivisionPresenter
from app.presenters.tasks.system_of_comprasion_of_the_first_degree.impl import CRTPresenter
from app.views.application.application import Application
from app.views.tasks.base import ITaskView
from app.views.tasks.comparison_of_the_first_degree.impl import ComparisonOfFirstDegreeView
from app.views.tasks.euclidian_algorithms.impl import GCDView
from app.views.tasks.remainder_division.impl import RemainderDivisionView
from app.views.tasks.system_of_comprasion_of_the_first_degree.impl import CRTView

TASKS: Final[dict[str, tuple[type[ITaskPresenter], type[ITaskView]]]] = {
    "Алгоритм Евклида": (GCDCalculatorPresenter, GCDView),
    "Остаток от деления": (RemainderDivisionPresenter, RemainderDivisionView),
    "Сравнение 1 степени": (ComparisonOfFirstDegreePresenter, ComparisonOfFirstDegreeView),
    "Сис. сравн. 1 степени": (CRTPresenter, CRTView)
}

if __name__ == "__main__":
    app = Application(TASKS)
    app.report_callback_exception = global_exception_handler
    app.mainloop()
