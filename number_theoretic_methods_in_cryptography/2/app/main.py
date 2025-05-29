from app.models.euler.impl import EulerModel
from app.presenters.impl import EulerPresenter
from app.views.impl import EulerView


def main() -> None:
    model: EulerModel = EulerModel()
    presenter: EulerPresenter = EulerPresenter(model)
    view: EulerView = EulerView(presenter)
    presenter.attach_view(view)
    view.mainloop()


if __name__ == "__main__":
    main()
