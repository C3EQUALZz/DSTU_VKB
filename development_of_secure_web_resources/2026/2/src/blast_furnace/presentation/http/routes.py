from decimal import Decimal

from dishka.integrations.flask import FromDishka, inject
from flask import Blueprint, current_app, render_template, request

from blast_furnace.application.calculate_temperature import CalculateTemperature
from blast_furnace.application.get_blast_reference import GetBlastReference
from blast_furnace.domain.temperature import BlastParameters

pages = Blueprint("pages", __name__, template_folder="templates", static_folder="static")


@pages.app_template_filter("decimal_ru")
def decimal_ru(value: Decimal) -> str:
    return str(value).replace(".", ",")


@pages.get("/")
@inject
def index(query: FromDishka[GetBlastReference]) -> str:
    return render_template("index.html", effects=query.execute())


@pages.route("/tempr", methods=["GET", "POST"])
@inject
def temperature(command: FromDishka[CalculateTemperature]) -> tuple[str, int]:
    values = {
        name: request.form.get(name, "")
        for name in ("t_blast", "humidity", "oxygen", "gas", "comment")
    }
    result = None
    error = None
    status = 200
    if request.method == "POST":
        try:
            numbers = []
            for name, label in (
                ("t_blast", "Температура дутья"),
                ("humidity", "Влажность дутья"),
                ("oxygen", "Содержание кислорода"),
                ("gas", "Расход природного газа"),
            ):
                try:
                    numbers.append(float(values[name].strip().replace(",", ".")))
                except ValueError:
                    raise ValueError(f"{label}: введите число.") from None
            parameters = BlastParameters(*numbers)
            if len(values["comment"]) > 500:
                raise ValueError("Комментарий должен содержать не более 500 символов.")
            result = command.execute(parameters, values["comment"])
        except ValueError as exc:
            error, status = str(exc), 400
        except OSError:
            current_app.logger.exception("Не удалось сохранить расчёт")
            error = "Не удалось сохранить расчёт в журнал. Повторите попытку позже."
            status = 503
    return render_template("tempr.html", values=values, tempr=result, error=error), status
