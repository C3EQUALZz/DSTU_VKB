from typing import Final

from app.presenters.tasks.base import ITaskPresenter
from app.presenters.tasks.euclidian_algorithms.impl import GCDCalculatorPresenter
from app.views.application.application import Application
from app.views.base import IView
from app.views.tasks.euclidian_algorithms.impl import GCDView

TASKS: Final[dict[str, tuple[type[ITaskPresenter], type[IView]]]] = {
    "Алгоритм Евклида": (GCDCalculatorPresenter, GCDView)
}

if __name__ == "__main__":
    app = Application(TASKS)
    app.mainloop()
