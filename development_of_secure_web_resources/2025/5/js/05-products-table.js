// Задание 5. Интерактивная таблица товаров.
// Использует: click (qty blur), dblclick (price), contextmenu (row),
//             drag*-события для перестановки строк, click для закрытия меню.
(function () {
    'use strict';

    const tbody = document.querySelector('#products tbody');
    const ctxMenu = document.getElementById('context-menu');
    const priceModal = document.getElementById('price-modal');
    const priceInput = document.getElementById('price-modal-input');
    const priceName = document.getElementById('price-modal-name');
    const priceSave = document.getElementById('price-modal-save');

    let editingPriceRow = null;
    let ctxRow = null;

    /* ---- Инициализация ---- */
    recalculateAll();

    /* ---- Inline-edit количества: blur + Enter ---- */
    tbody.addEventListener('blur', function (event) {
        const cell = event.target.closest('[data-field="qty"]');
        if (!cell) return;
        const row = cell.closest('tr');
        const value = parseInt(cell.textContent, 10);
        if (Number.isNaN(value) || value < 0) {
            cell.textContent = '0';
        } else {
            cell.textContent = String(value);
        }
        recalc(row);
    }, true);

    tbody.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (event.target.matches('[data-field="qty"]')) event.target.blur();
        }
    });

    /* ---- Double-click по цене → модальное ---- */
    tbody.addEventListener('dblclick', function (event) {
        const cell = event.target.closest('[data-field="price"]');
        if (!cell) return;
        const row = cell.closest('tr');
        editingPriceRow = row;
        priceName.textContent = row.querySelector('[data-field="name"]').textContent;
        priceInput.value = cell.textContent;
        priceModal.hidden = false;
        priceInput.focus();
        priceInput.select();
    });

    priceModal.querySelectorAll('[data-close]').forEach(el => {
        el.addEventListener('click', closePriceModal);
    });
    priceSave.addEventListener('click', function () {
        if (!editingPriceRow) return;
        const v = Number(priceInput.value);
        if (Number.isFinite(v) && v >= 0) {
            editingPriceRow.querySelector('[data-field="price"]').textContent = String(v);
            recalc(editingPriceRow);
        }
        closePriceModal();
    });
    function closePriceModal() {
        priceModal.hidden = true;
        editingPriceRow = null;
    }

    /* ---- Контекстное меню ---- */
    tbody.addEventListener('contextmenu', function (event) {
        const row = event.target.closest('tr');
        if (!row) return;
        event.preventDefault();
        ctxRow = row;
        renderContextMenu(event.clientX, event.clientY);
    });
    document.addEventListener('click', hideContextMenu);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hideContextMenu(); });

    function renderContextMenu(x, y) {
        const items = [
            { label: 'Удалить', action: () => { ctxRow.remove(); recalculateAll(); } },
            { label: 'Изменить название', action: () => {
                const cell = ctxRow.querySelector('[data-field="name"]');
                const next = prompt('Новое название', cell.textContent);
                if (next !== null && next.trim()) cell.textContent = next.trim();
            }},
            { label: 'Добавить комментарий', action: () => {
                const text = prompt('Комментарий к товару:');
                if (text) {
                    ctxRow.title = text;
                    ctxRow.style.outline = '1px dashed #6366f1';
                }
            }},
        ];
        ctxMenu.innerHTML = '';
        for (const item of items) {
            const li = document.createElement('li');
            li.textContent = item.label;
            li.addEventListener('click', function (event) {
                event.stopPropagation();
                item.action();
                hideContextMenu();
            });
            ctxMenu.appendChild(li);
        }
        ctxMenu.style.left = `${x}px`;
        ctxMenu.style.top = `${y}px`;
        ctxMenu.hidden = false;
    }
    function hideContextMenu() { ctxMenu.hidden = true; ctxRow = null; }

    /* ---- Drag & Drop строк ---- */
    let dragRow = null;

    tbody.addEventListener('dragstart', function (event) {
        const row = event.target.closest('tr');
        if (!row) return;
        dragRow = row;
        row.classList.add('is-dragging');
        if (event.dataTransfer) {
            event.dataTransfer.effectAllowed = 'move';
            event.dataTransfer.setData('text/plain', row.dataset.id || '');
        }
    });

    tbody.addEventListener('dragover', function (event) {
        event.preventDefault();
        const row = event.target.closest('tr');
        if (!row || row === dragRow) return;
        row.classList.add('drag-over');
        if (event.dataTransfer) event.dataTransfer.dropEffect = 'move';
    });
    tbody.addEventListener('dragleave', function (event) {
        const row = event.target.closest('tr');
        if (row) row.classList.remove('drag-over');
    });
    tbody.addEventListener('drop', function (event) {
        event.preventDefault();
        const target = event.target.closest('tr');
        if (!target || !dragRow || target === dragRow) return;
        target.classList.remove('drag-over');
        const rows = Array.from(tbody.children);
        const dragIdx = rows.indexOf(dragRow);
        const targetIdx = rows.indexOf(target);
        if (dragIdx < targetIdx) {
            target.after(dragRow);
        } else {
            target.before(dragRow);
        }
    });
    tbody.addEventListener('dragend', function () {
        if (dragRow) dragRow.classList.remove('is-dragging');
        tbody.querySelectorAll('.drag-over').forEach(r => r.classList.remove('drag-over'));
        dragRow = null;
    });

    /* ---- Пересчёт ---- */
    function recalc(row) {
        const price = Number(row.querySelector('[data-field="price"]').textContent);
        const qty = Number(row.querySelector('[data-field="qty"]').textContent);
        const total = row.querySelector('[data-field="total"]');
        if (Number.isFinite(price) && Number.isFinite(qty)) {
            total.textContent = (price * qty).toFixed(2);
        } else {
            total.textContent = '—';
        }
    }
    function recalculateAll() {
        tbody.querySelectorAll('tr').forEach(recalc);
    }
})();
