"""Снимки реально запущенного приложения для отчёта."""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:5001")
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / "docs" / "screenshots"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, locale="ru-RU")
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = page.goto(args.url, wait_until="networkidle")
        assert response is not None and response.status == 200
        assert page.locator("tbody tr").count() == 3
        page.screenshot(path=str(output / "index-desktop.png"), full_page=True)
        page.locator("nav").get_by_role("link", name="Расчёт ТТГ").click()
        page.wait_for_url("**/tempr")
        page.screenshot(path=str(output / "tempr-desktop.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(args.url, wait_until="networkidle")
        assert page.evaluate(
            "document.documentElement.scrollWidth <= window.innerWidth"
        ), "Mobile page overflows horizontally"
        page.screenshot(path=str(output / "index-mobile.png"), full_page=True)
        assert not errors, errors
        browser.close()
    print(f"Browser checks passed; screenshots: {output}")


if __name__ == "__main__":
    main()
