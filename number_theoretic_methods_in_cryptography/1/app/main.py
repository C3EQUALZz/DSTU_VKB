from app.models.base import BaseGCDStrategy
from app.models.bezout import GCDBezout
from app.models.binary import GCDBinary
from app.models.classic import GCDMod
from app.presenters.app import GCDCalculatorPresenter
from app.views.app import GCDView

# Стратегии
STRATEGIES: dict[str, type[BaseGCDStrategy]] = {
    "Классический": GCDMod,
    "Бинарный": GCDBinary,
    "Расширенный": GCDBezout
}

if __name__ == "__main__":
    view: GCDView = GCDView(None)
    presenter: GCDCalculatorPresenter = GCDCalculatorPresenter(view, STRATEGIES)
    view.presenter = presenter
    view.run_button.configure(command=presenter.on_calculate)
    view.mainloop()

