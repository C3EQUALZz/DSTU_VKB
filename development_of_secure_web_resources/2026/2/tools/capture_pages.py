"""Проверить приложение в Chrome и сохранить снимки для отчёта ЛР2."""

import argparse
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:5002")
    args = parser.parse_args()
    output = ROOT / "docs" / "screenshots"
    output.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1000}, locale="ru-RU")
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = page.goto(args.url, wait_until="networkidle")
        assert response is not None and response.status == 200
        assert page.locator("tbody tr").count() == 3
        page.screenshot(path=str(output / "index-desktop.png"), full_page=True)
        page.locator("nav").get_by_role("link", name="Расчёт ТТГ").click()
        page.wait_for_load_state("networkidle")
        expect(page.locator("#temperature-result")).to_have_count(0)
        expect(page.locator("form input[required]")).to_have_count(4)
        page.screenshot(path=str(output / "tempr-form.png"), full_page=True)
        for number, (values, expected) in enumerate(
            [
                (("1000", "10", "21", "0"), "2201,0"),
                (("1200", "15", "25", "8"), "2080,0"),
                (("1100", "20", "23", "5"), "2048,0"),
                (("1300", "1", "35", "0"), "3076,6"),
            ],
            start=1,
        ):
            for name, value in zip(
                ("t_blast", "humidity", "oxygen", "gas"), values, strict=True
            ):
                page.locator(f"#{name}").fill(value)
            comment = f"Контрольный расчёт № {number} из методички"
            page.locator("#comment").fill(comment)
            with page.expect_response(
                lambda r: r.url.endswith("/tempr") and r.request.method == "POST"
            ) as event:
                page.get_by_role("button", name="Рассчитать").click()
            assert event.value.status == 200
            expect(page.locator("#temperature-result")).to_have_text(expected)
            expect(page.locator("#result-comment")).to_have_text(comment)
            results.append(f"Контрольный расчёт {number}: {values} → {expected} °C — OK")
            if number == 1:
                page.screenshot(path=str(output / "tempr-result.png"), full_page=True)
        page.locator("#t_blast").fill("abc")
        with page.expect_response(
            lambda r: r.url.endswith("/tempr") and r.request.method == "POST"
        ) as event:
            page.get_by_role("button", name="Рассчитать").click()
        assert event.value.status == 400
        expect(page.get_by_role("alert")).to_contain_text("введите число")
        expect(page.locator("#temperature-result")).to_have_count(0)
        expect(page.locator("#humidity")).to_have_value("1")
        page.screenshot(path=str(output / "tempr-error.png"), full_page=True)
        results.append(
            "Неверный ввод: HTTP 400, сообщение с ошибкой, значения сохранены — OK"
        )
        page.locator("#t_blast").fill("1000")
        page.locator("#humidity").fill("10")
        page.locator("#oxygen").fill("21")
        page.locator("#gas").fill("0")
        payload = "<script>window.report_xss=true</script>"
        page.locator("#comment").fill(payload)
        page.get_by_role("button", name="Рассчитать").click()
        page.wait_for_load_state("networkidle")
        expect(page.locator("#result-comment")).to_have_text(payload)
        assert page.evaluate("window.report_xss === undefined")
        results.append(
            "Комментарий с HTML отображается текстом, JavaScript не выполняется — OK"
        )
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(args.url, wait_until="networkidle")
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        page.screenshot(path=str(output / "index-mobile.png"), full_page=True)
        page.goto(args.url + "/tempr", wait_until="networkidle")
        for name, value in zip(
            ("t_blast", "humidity", "oxygen", "gas"),
            ("1000", "10", "21", "0"),
            strict=True,
        ):
            page.locator(f"#{name}").fill(value)
        page.locator("#comment").fill("Мобильная проверка, 390 px")
        page.get_by_role("button", name="Рассчитать").click()
        expect(page.locator("#temperature-result")).to_have_text("2201,0")
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        page.screenshot(path=str(output / "tempr-mobile.png"), full_page=True)
        results.append(
            "Главная и расчёт при ширине 390 px, без горизонтального переполнения — OK"
        )
        assert not errors, errors
        results.append("Ошибок JavaScript не обнаружено")
        browser.close()
    text = (
        "Браузер: Google Chrome, локальное приложение "
        + args.url
        + "\n"
        + "\n".join(results)
        + "\n"
    )
    (ROOT / "docs" / "browser-verification.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
