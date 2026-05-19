// Задание 7. DnD списков студентов.
// ВАЖНО: по условию запрещены CSS :hover / ::before / ::after — поэтому
// все эффекты «наведения», подсветки зоны drop, ошибки и т.п. реализованы
// через JS добавлением/снятием классов .is-hover / .is-dragover / .is-error и т.д.

(function () {
    'use strict';

    const MAX_CARDS = 35;

    const INITIAL_STUDENTS = [
        'Иванов И.И.', 'Оплачко О.О.', 'Петров П.П.',
        'Сазонов С.С.', 'Фадеев Ф.Ф.', 'Яковлев Я.Я.', 'Яровой Я.А.',
    ];

    const lists = document.querySelectorAll('.list');
    const ctxMenu = document.getElementById('ctx-menu');
    const addForm = document.getElementById('add-form');
    const newInput = document.getElementById('new-student');

    /* ===== Инициализация ===== */
    const groupList = document.querySelector('[data-list-id="group"]');
    const groupZone = groupList.querySelector('[data-zone]');
    INITIAL_STUDENTS.forEach(name => addCard(groupZone, name, /*silent*/ true));

    lists.forEach(updateCount);
    lists.forEach(refreshPlaceholder);

    /* ===== Добавление через форму ===== */
    addForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const value = newInput.value.trim();
        if (!value) return;

        const total = countAllCards();
        if (total >= MAX_CARDS) {
            flashError(newInput);
            alert(`Достигнут лимит карточек (${MAX_CARDS}).`);
            return;
        }
        addCard(groupZone, value);
        newInput.value = '';
        newInput.focus();
    });

    /* ===== Контекстное меню для всех карточек (делегирование) ===== */
    document.addEventListener('contextmenu', function (event) {
        const card = event.target.closest('.card');
        if (!card) return;
        event.preventDefault();
        openContextMenu(card, event.clientX, event.clientY);
    });
    document.addEventListener('click', hideContextMenu);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hideContextMenu(); });

    function openContextMenu(card, x, y) {
        ctxMenu.innerHTML = '';
        const liDelete = document.createElement('li');
        liDelete.textContent = 'Удалить';
        liDelete.addEventListener('click', function (e) {
            e.stopPropagation();
            removeCard(card);
            hideContextMenu();
        });
        const liClose = document.createElement('li');
        liClose.textContent = 'Закрыть';
        liClose.addEventListener('click', function (e) {
            e.stopPropagation();
            hideContextMenu();
        });
        ctxMenu.appendChild(liDelete);
        ctxMenu.appendChild(liClose);

        // Подсветка пункта при наведении — без :hover
        ctxMenu.querySelectorAll('li').forEach(li => {
            li.addEventListener('mouseenter', () => li.classList.add('is-active'));
            li.addEventListener('mouseleave', () => li.classList.remove('is-active'));
        });

        const menuWidth = 160;
        const menuHeight = 80;
        let posX = x;
        let posY = y;
        if (x + menuWidth > window.innerWidth)  posX = window.innerWidth - menuWidth - 8;
        if (y + menuHeight > window.innerHeight) posY = window.innerHeight - menuHeight - 8;

        ctxMenu.style.left = `${posX}px`;
        ctxMenu.style.top = `${posY}px`;
        ctxMenu.hidden = false;
    }
    function hideContextMenu() { ctxMenu.hidden = true; }

    /* ===== Создание карточки ===== */
    function addCard(zone, name, silent) {
        const li = document.createElement('li');
        li.className = 'card';
        li.draggable = true;
        li.textContent = name;
        wireCard(li);
        zone.appendChild(li);
        sortZone(zone);
        const list = zone.closest('.list');
        updateCount(list);
        refreshPlaceholder(list);
        if (!silent) {
            li.classList.add('is-success');
            setTimeout(() => li.classList.remove('is-success'), 600);
        }
        return li;
    }

    function removeCard(card) {
        const list = card.closest('.list');
        card.remove();
        updateCount(list);
        refreshPlaceholder(list);
    }

    /* ===== События на карточке (без CSS :hover) ===== */
    function wireCard(card) {
        card.addEventListener('mouseenter', () => card.classList.add('is-hover'));
        card.addEventListener('mouseleave', () => card.classList.remove('is-hover'));

        card.addEventListener('dragstart', function (event) {
            card.classList.add('is-dragging');
            if (event.dataTransfer) {
                event.dataTransfer.effectAllowed = 'move';
                event.dataTransfer.setData('text/plain', card.textContent);
            }
            dragState.card = card;
        });

        card.addEventListener('dragend', function () {
            card.classList.remove('is-dragging');
            if (!dragState.dropped && dragState.card) {
                // бросили вне зоны → ошибка
                flashError(dragState.card);
            }
            dragState.card = null;
            dragState.dropped = false;
            lists.forEach(l => l.classList.remove('is-dragover'));
        });
    }

    const dragState = { card: null, dropped: false };

    /* ===== События на списках-приёмниках ===== */
    lists.forEach(list => {
        list.addEventListener('dragenter', function (event) {
            event.preventDefault();
            list.classList.add('is-dragover');
        });
        list.addEventListener('dragover', function (event) {
            event.preventDefault();
            if (event.dataTransfer) event.dataTransfer.dropEffect = 'move';
        });
        list.addEventListener('dragleave', function (event) {
            // событие срабатывает и при движении между потомками, поэтому проверяем
            if (event.relatedTarget && list.contains(event.relatedTarget)) return;
            list.classList.remove('is-dragover');
        });
        list.addEventListener('drop', function (event) {
            event.preventDefault();
            list.classList.remove('is-dragover');
            const card = dragState.card;
            if (!card) return;
            const zone = list.querySelector('[data-zone]');
            zone.appendChild(card);
            sortZone(zone);
            // обновляем оба списка (так как мы переместили из одного в другой)
            lists.forEach(updateCount);
            lists.forEach(refreshPlaceholder);
            card.classList.add('is-success');
            setTimeout(() => card.classList.remove('is-success'), 600);
            dragState.dropped = true;
        });
    });

    /* ===== Сортировка по алфавиту ===== */
    function sortZone(zone) {
        const cards = Array.from(zone.querySelectorAll('.card'));
        cards.sort((a, b) => a.textContent.localeCompare(b.textContent, 'ru'));
        cards.forEach(c => zone.appendChild(c));
    }

    /* ===== Счётчик и плейсхолдер ===== */
    function updateCount(list) {
        const zone = list.querySelector('[data-zone]');
        const span = list.querySelector('[data-count]');
        span.textContent = zone.querySelectorAll('.card').length;
    }
    function refreshPlaceholder(list) {
        const zone = list.querySelector('[data-zone]');
        const has = zone.querySelectorAll('.card').length > 0;
        let ph = zone.querySelector('.placeholder');
        if (has && ph) ph.remove();
        if (!has && !ph) {
            ph = document.createElement('li');
            ph.className = 'placeholder';
            ph.textContent = 'Перетяни сюда';
            zone.appendChild(ph);
        }
    }

    function countAllCards() {
        let n = 0;
        lists.forEach(l => { n += l.querySelectorAll('.card').length; });
        return n;
    }

    function flashError(el) {
        el.classList.add('is-error');
        setTimeout(() => el.classList.remove('is-error'), 400);
    }
})();
