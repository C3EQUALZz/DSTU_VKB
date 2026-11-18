"""Проверить SecureDev в Chrome и сохранить материалы для отчёта ЛР3."""

import argparse
import json
from base64 import urlsafe_b64decode
from pathlib import Path
from secrets import token_hex
from zlib import decompress

from playwright.sync_api import expect, sync_playwright

DOCS = Path(__file__).resolve().parents[1] / "docs"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:5003")
    args = parser.parse_args()
    url = args.url.rstrip("/")
    screenshots = DOCS / "screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)
    findings = [f"Google Chrome, {url}"]
    demo_suffix = token_hex(3)
    username = f"student-{demo_suffix}"
    password = token_hex(16)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1120, "height": 900}, locale="ru-RU")
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        for path in ("/tempr", "/compare"):
            response = page.goto(url + path, wait_until="networkidle")
            assert response is not None and response.status == 200
            initial = response.request.redirected_from
            assert initial is not None
            initial_response = initial.response()
            assert initial_response is not None and initial_response.status == 302
            expect(page).to_have_url(url + "/login")
            findings.append(f"Гость {path} → HTTP 302 /login → HTTP 200")
        expect(page.get_by_role("heading", name="Вход")).to_be_visible()
        assert (
            page.evaluate(
                "getComputedStyle(document.querySelector('.auth-form')).backgroundColor"
            )
            == "rgb(255, 255, 255)"
        )
        page.screenshot(path=screenshots / "01-login.png", full_page=True)

        page.get_by_role("link", name="Регистрация", exact=True).click()
        expect(page.get_by_label("Электронная почта")).to_be_visible()
        page.get_by_label("Имя пользователя").fill(username)
        page.get_by_label("Электронная почта").fill(f"{username}@example.org")
        page.screenshot(path=screenshots / "02-register.png", full_page=True)
        page.get_by_label("Пароль", exact=True).fill(password)
        page.get_by_label("Повторите пароль").fill(password)
        page.get_by_role("button", name="Зарегистрироваться").click()
        expect(page).to_have_url(url + "/")
        expect(page.locator("nav").get_by_text(username, exact=True)).to_be_visible()
        findings.append("Регистрация с email и автоматический вход подтверждены")

        cookie = next(c for c in page.context.cookies(url) if c["name"] == "session")
        assert cookie["httpOnly"] and cookie["sameSite"] == "Lax"
        assert not cookie["secure"] and cookie["expires"] > 0
        value = cookie["value"]
        encoded = value.lstrip(".").split(".", 1)[0]
        payload = urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
        fields = json.loads(decompress(payload) if value.startswith(".") else payload)
        assert set(fields) == {"session_id", "_permanent"}
        assert len(fields["session_id"]) == 43
        findings.append(
            "cookie session: HttpOnly=True, SameSite=Lax, Secure=False (локальный HTTP)"
        )
        findings.append('Поля cookie: {"session_id":"[скрыт]", "_permanent":true}')

        page.get_by_role("link", name="Расчёт ТТГ", exact=True).first.click()
        for name, number in zip(
            ("t_blast", "humidity", "oxygen", "gas"),
            ("1000", "10", "21", "0"),
            strict=True,
        ):
            page.locator(f"#{name}").fill(number)
        page.get_by_label("Комментарий к расчёту").fill("Контрольный расчёт")
        page.get_by_role("button", name="Рассчитать").click()
        expect(page.locator("#temperature-result")).to_have_text("2201,0")
        page.screenshot(path=screenshots / "03-tempr.png", full_page=True)
        findings.append("/tempr: 2201,0 °C")

        page.get_by_role("link", name="Сравнение режимов").click()
        for prefix, values in (
            ("first_", ("1000", "10", "21", "0")),
            ("second_", ("1200", "15", "25", "8")),
        ):
            for name, number in zip(
                ("t_blast", "humidity", "oxygen", "gas"), values, strict=True
            ):
                page.locator(f"#{prefix}{name}").fill(number)
        page.get_by_role("button", name="Сравнить").click()
        expect(page.locator("#first-temperature")).to_have_text("2201,0")
        expect(page.locator("#second-temperature")).to_have_text("2080,0")
        expect(page.locator("#temperature-difference")).to_have_text("-121,0")
        page.screenshot(path=screenshots / "04-compare.png", full_page=True)
        findings.append("/compare: 2201,0 °C и 2080,0 °C, разница −121,0 °C")

        page.set_viewport_size({"width": 390, "height": 844})
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        findings.append("На /compare при ширине 390 px нет горизонтального переполнения")
        page.set_viewport_size({"width": 1120, "height": 900})
        page.get_by_role("button", name="Выйти").click()
        expect(page).to_have_url(url + "/")
        assert all(c["name"] != "session" for c in page.context.cookies(url))
        page.goto(url + "/tempr", wait_until="networkidle")
        expect(page).to_have_url(url + "/login")
        page.get_by_label("Имя пользователя").fill(username)
        page.get_by_label("Пароль").fill(token_hex(16))
        page.get_by_role("button", name="Войти", exact=True).click()
        expect(page.get_by_role("alert")).to_have_text("Неверное имя или пароль.")
        page.screenshot(path=screenshots / "05-bad-login.png", full_page=True)
        findings.append("После выхода cookie удалена, /tempr перенаправляет на /login")
        findings.append("Неверный пароль отклонён с общим сообщением об ошибке")
        page.get_by_label("Пароль").fill(password)
        page.get_by_role("button", name="Войти", exact=True).click()
        expect(page).to_have_url(url + "/")
        expect(page.locator("nav").get_by_text(username, exact=True)).to_be_visible()
        findings.append("Повторный вход с верным паролем подтверждён")
        assert not errors, errors
        browser.close()

    verification = "\n".join(findings) + "\n"
    (DOCS / "browser-verification.txt").write_text(verification)
    print(verification)


if __name__ == "__main__":
    main()
