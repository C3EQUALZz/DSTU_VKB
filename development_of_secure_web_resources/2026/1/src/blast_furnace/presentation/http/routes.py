from decimal import Decimal

from dishka.integrations.flask import FromDishka, inject
from flask import Blueprint, render_template

from blast_furnace.application.get_blast_reference import GetBlastReference

pages = Blueprint("pages", __name__, template_folder="templates", static_folder="static")


@pages.app_template_filter("decimal_ru")
def decimal_ru(value: Decimal) -> str:
    return str(value).replace(".", ",")


@pages.get("/")
@inject
def index(query: FromDishka[GetBlastReference]) -> str:
    return render_template("index.html", effects=query.execute())


@pages.get("/tempr")
def temperature() -> str:
    return render_template("tempr.html")
