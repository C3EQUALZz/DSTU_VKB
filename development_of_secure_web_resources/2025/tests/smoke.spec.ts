import { test, expect } from '@playwright/test';

/* ============================================================
 *  ЛР1 — HTML
 * ============================================================ */
test.describe('ЛР1. HTML', () => {
    test('index открывается и содержит 11 ссылок на задания', async ({ page }) => {
        await page.goto('/1/index.html');
        await expect(page).toHaveTitle(/ЛР №?1\.?.*HTML|Знакомство с HTML/i);
        const links = page.locator('ol li a');
        await expect(links).toHaveCount(11);
    });

    test('страница 01: видны заголовок, абзац и <hr>', async ({ page }) => {
        await page.goto('/1/01-simple-page.html');
        await expect(page.locator('h1')).toHaveText(/Привет, мир!/);
        await expect(page.locator('hr')).toHaveCount(1);
    });

    test('страница 07: таблица типов input не пуста', async ({ page }) => {
        await page.goto('/1/07-input-types.html');
        const rows = page.locator('tbody tr');
        const count = await rows.count();
        expect(count).toBeGreaterThanOrEqual(20);
    });
});

/* ============================================================
 *  ЛР2 — CSS
 * ============================================================ */
test.describe('ЛР2. CSS', () => {
    test('таблица 7×4 содержит 7 строк данных', async ({ page }) => {
        await page.goto('/2/03-table.html');
        const rows = page.locator('table.data-table tbody tr');
        await expect(rows).toHaveCount(7);
    });

    test('кнопки задания 2 присутствуют и реагируют на hover', async ({ page }) => {
        await page.goto('/2/02-buttons.html');
        const btn = page.locator('.btn-primary');
        await expect(btn).toBeVisible();
        // Проверим переход цвета: цвет до и после hover должен отличаться
        const colorBefore = await btn.evaluate(el => getComputedStyle(el).backgroundColor);
        await btn.hover();
        await page.waitForTimeout(250);
        const colorAfter = await btn.evaluate(el => getComputedStyle(el).backgroundColor);
        expect(colorBefore).not.toBe(colorAfter);
    });

    test('форма регистрации содержит все обязательные поля', async ({ page }) => {
        await page.goto('/2/05-registration.html');
        await expect(page.locator('input[name="first_name"]')).toBeVisible();
        await expect(page.locator('input[name="last_name"]')).toBeVisible();
        await expect(page.locator('input[name="email"]')).toBeVisible();
        await expect(page.locator('input[name="password"]')).toBeVisible();
        await expect(page.locator('input[name="password_confirm"]')).toBeVisible();
    });
});

/* ============================================================
 *  ЛР3 — адаптивная вёрстка
 * ============================================================ */
test.describe('ЛР3. Адаптивная вёрстка', () => {
    test('Grid: при ширине 1280px карточки в 4 столбца', async ({ page }) => {
        await page.setViewportSize({ width: 1280, height: 800 });
        await page.goto('/3/01-grid-products.html');
        const cols = await page.locator('.products').evaluate(el =>
            getComputedStyle(el).gridTemplateColumns.split(' ').length
        );
        expect(cols).toBe(4);
    });

    test('Grid: при ширине 900px карточки в 3 столбца', async ({ page }) => {
        await page.setViewportSize({ width: 900, height: 800 });
        await page.goto('/3/01-grid-products.html');
        const cols = await page.locator('.products').evaluate(el =>
            getComputedStyle(el).gridTemplateColumns.split(' ').length
        );
        expect(cols).toBe(3);
    });

    test('Grid: при ширине 480px карточки в 2 столбца', async ({ page }) => {
        await page.setViewportSize({ width: 480, height: 800 });
        await page.goto('/3/01-grid-products.html');
        const cols = await page.locator('.products').evaluate(el =>
            getComputedStyle(el).gridTemplateColumns.split(' ').length
        );
        expect(cols).toBe(2);
    });

    test('CSS-only гамбургер: при ширине 360px меню скрыто, чекбокс раскрывает', async ({ page }) => {
        await page.setViewportSize({ width: 360, height: 700 });
        await page.goto('/3/02-sticky-menu.html');

        const nav = page.locator('.nav');
        const maxHeightBefore = await nav.evaluate(el =>
            parseFloat(getComputedStyle(el).maxHeight)
        );
        expect(maxHeightBefore).toBeLessThan(50);   // меню свёрнуто

        // Чекбокс с hidden — кликаем по label, как сделал бы пользователь
        await page.locator('label.burger').click();
        await page.waitForTimeout(400);
        const maxHeightAfter = await nav.evaluate(el =>
            parseFloat(getComputedStyle(el).maxHeight)
        );
        expect(maxHeightAfter).toBeGreaterThan(100);
    });
});

/* ============================================================
 *  ЛР4 — JavaScript
 * ============================================================ */
test.describe('ЛР4. JavaScript', () => {
    test('задача 1 — погода: -10°C → тёплая куртка', async ({ page }) => {
        await page.goto('/4/tasks/task01.html');
        page.on('dialog', d => d.accept('-10'));
        await page.locator('#run').click();
        await expect(page.locator('#output')).toContainText('тёплую куртку');
    });

    test('задача 1 — погода: 25°C → футболка', async ({ page }) => {
        await page.goto('/4/tasks/task01.html');
        page.on('dialog', d => d.accept('25'));
        await page.locator('#run').click();
        await expect(page.locator('#output')).toContainText('футболке');
    });

    test('задача 5 — максимум массива', async ({ page }) => {
        await page.goto('/4/tasks/task05.html');
        page.on('dialog', d => d.accept('3, 10, 7, 21, 4, 19'));
        await page.locator('#run').click();
        await expect(page.locator('#output')).toContainText('Максимальное число: 21');
    });

    test('задача 8 — возраст 25 → доступ разрешён', async ({ page }) => {
        await page.goto('/4/tasks/task08.html');
        page.on('dialog', d => d.accept('25'));
        await page.locator('#run').click();
        await expect(page.locator('#output')).toContainText('Доступ разрешён');
    });

    test('задача 10 — гласные в "Привет"', async ({ page }) => {
        await page.goto('/4/tasks/task10.html');
        page.on('dialog', d => d.accept('Привет'));
        await page.locator('#run').click();
        await expect(page.locator('#output')).toContainText('Количество гласных: 2');
    });
});

/* ============================================================
 *  ЛР5 — браузерные события
 * ============================================================ */
test.describe('ЛР5. Браузерные события', () => {
    test('модалка регистрации открывается по клику', async ({ page }) => {
        await page.goto('/5/01-nav-modal-timer.html');
        await expect(page.locator('#modal')).toBeHidden();
        await page.locator('#open-register').click();
        await expect(page.locator('#modal')).toBeVisible();
    });

    test('валидация email: некорректный адрес → ошибка', async ({ page }) => {
        await page.goto('/5/01-nav-modal-timer.html');
        await page.locator('#open-register').click();
        await page.fill('#modal input[name="name"]', 'Иван');
        await page.fill('#modal input[name="email"]', 'not-email');
        await page.fill('#modal input[name="password"]', 'Qq1!aaaaaaaa');
        await page.locator('#modal button[type="submit"]').click();
        await expect(page.locator('.field-error[data-for="email"]')).not.toBeEmpty();
    });

    test('валидный submit показывает «Спасибо!»', async ({ page }) => {
        await page.goto('/5/01-nav-modal-timer.html');
        await page.locator('#open-register').click();
        await page.fill('#modal input[name="name"]', 'Иван');
        await page.fill('#modal input[name="email"]', 'user@example.com');
        await page.fill('#modal input[name="password"]', 'Qq1!aaaaaaaa');
        await page.locator('#modal button[type="submit"]').click();
        await expect(page.locator('#modal-success')).toBeVisible();
    });

    test('таймер: запуск, секунда идёт', async ({ page }) => {
        await page.goto('/5/01-nav-modal-timer.html');
        await page.fill('#timer-seconds', '10');
        await page.locator('#timer-start').click();
        await page.waitForTimeout(1500);
        const text = await page.locator('#timer-display').textContent();
        expect(text).toMatch(/00:0[7-9]/);
    });

    test('галерея: hover показывает превью', async ({ page }) => {
        await page.goto('/5/04-gallery.html');
        await expect(page.locator('#preview')).toBeHidden();
        await page.locator('.thumb').first().hover();
        await expect(page.locator('#preview')).toBeVisible();
    });

    test('задание 7: начально 7 студентов в группе, 0 в долгах', async ({ page }) => {
        await page.goto('/5/07-students-dnd.html');
        await page.waitForLoadState('domcontentloaded');
        // Ждём, чтобы JS вставил карточки
        await page.waitForFunction(() => {
            return document.querySelector('[data-list-id="group"] [data-count]')?.textContent === '7';
        }, { timeout: 5000 });
        const debt = await page.locator('[data-list-id="debt"] [data-count]').textContent();
        expect(debt).toBe('0');
    });

    test('задание 7: добавление студента увеличивает счётчик', async ({ page }) => {
        await page.goto('/5/07-students-dnd.html');
        await page.waitForFunction(() => {
            return document.querySelector('[data-list-id="group"] [data-count]')?.textContent === '7';
        }, { timeout: 5000 });
        await page.fill('#new-student', 'Аркадьев А.А.');
        await page.locator('#add-form button[type="submit"]').click();
        await expect(page.locator('[data-list-id="group"] [data-count]')).toHaveText('8');
    });
});
