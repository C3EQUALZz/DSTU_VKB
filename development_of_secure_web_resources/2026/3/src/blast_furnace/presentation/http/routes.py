from decimal import Decimal

from dishka.integrations.flask import FromDishka, inject
from flask import Blueprint, current_app, render_template, request

from blast_furnace.application.calculate_temperature import CalculateTemperature
from blast_furnace.application.get_blast_reference import GetBlastReference
from blast_furnace.domain.temperature import BlastParameters

pages = Blueprint("pages", __name__, template_folder="templates", static_folder="static")

BLAST_FIELDS = (
    ("t_blast", "Температура дутья, °C", "От 900 до 1300 °C"),
    ("humidity", "Влажность дутья, г/м³", "От 1 до 40 г/м³"),
    ("oxygen", "Содержание кислорода, %", "От 21 до 35 %"),
    ("gas", "Расход природного газа, м³/100 м³", "От 0 до 15 м³ на 100 м³ дутья"),
)


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
    values = _blast_values()
    comment = request.form.get("comment", "")
    result = None
    error = None
    status = 200
    if request.method == "POST":
        try:
            parameters = _parse_blast(values)
            if len(comment) > 500:
                raise ValueError("Комментарий должен содержать не более 500 символов.")
            result = command.execute(parameters, comment)
        except ValueError as exc:
            error, status = str(exc), 400
        except OSError:
            current_app.logger.exception("Не удалось сохранить расчёт")
            error = "Не удалось сохранить расчёт в журнал. Повторите попытку позже."
            status = 503
    return render_template(
        "tempr.html",
        values=values,
        fields=BLAST_FIELDS,
        comment=comment,
        tempr=result,
        error=error,
    ), status


@pages.route("/compare", methods=["GET", "POST"])
def compare() -> tuple[str, int]:
    first = _blast_values("first_")
    second = _blast_values("second_")
    result = None
    error = None
    if request.method == "POST":
        temperatures = []
        for index, values in enumerate((first, second), start=1):
            try:
                temperatures.append(_parse_blast(values).theoretical_temperature())
            except ValueError as exc:
                error = f"Режим {index}. {exc}"
                break
        if error is None:
            first_temperature, second_temperature = temperatures
            result = (
                first_temperature,
                second_temperature,
                second_temperature - first_temperature,
            )
    return render_template(
        "compare.html",
        first=first,
        second=second,
        fields=BLAST_FIELDS,
        result=result,
        error=error,
    ), 400 if error else 200


def _blast_values(prefix: str = "") -> dict[str, str]:
    return {name: request.form.get(prefix + name, "") for name, _, _ in BLAST_FIELDS}


def _parse_blast(values: dict[str, str]) -> BlastParameters:
    numbers = []
    for name, label, _ in BLAST_FIELDS:
        try:
            numbers.append(float(values[name].strip().replace(",", ".")))
        except ValueError:
            raise ValueError(f"{label}. Введите число.") from None
    return BlastParameters(*numbers)
