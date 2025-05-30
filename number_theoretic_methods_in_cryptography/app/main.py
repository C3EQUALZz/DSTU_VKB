from typing import Final

from app.exceptions.app import global_exception_handler
from app.presenters.tasks.base import ITaskPresenter
from app.presenters.tasks.comparison_of_the_first_degree.impl import ComparisonOfFirstDegreePresenter
from app.presenters.tasks.euclidian_algorithms.impl import GCDCalculatorPresenter
from app.presenters.tasks.remainder_division.impl import RemainderDivisionPresenter
from app.views.application.application import Application
from app.views.tasks.base import ITaskView
from app.views.tasks.comparison_of_the_first_degree.impl import ComparisonOfFirstDegreeView
from app.views.tasks.euclidian_algorithms.impl import GCDView
from app.views.tasks.remainder_division.impl import RemainderDivisionView

TASKS: Final[dict[str, tuple[type[ITaskPresenter], type[ITaskView]]]] = {
    "Алгоритм Евклида": (GCDCalculatorPresenter, GCDView),
    "Остаток от деления": (RemainderDivisionPresenter, RemainderDivisionView),
    "Сравнение первой степени": (ComparisonOfFirstDegreePresenter, ComparisonOfFirstDegreeView)
}

if __name__ == "__main__":
    app = Application(TASKS)
    app.report_callback_exception = global_exception_handler
    app.mainloop()
