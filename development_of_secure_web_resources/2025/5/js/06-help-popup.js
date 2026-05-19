// Задание 6. Всплывающее окно помощи.
// События: DOMContentLoaded → setTimeout → click (open/close, submit).
(function () {
    'use strict';

    const DELAY_MS = 5000;

    const popup = document.getElementById('help');
    const form = document.getElementById('help-form');
    const thanks = document.getElementById('help-thanks');

    // Появляется автоматически через 5 секунд после загрузки.
    setTimeout(function () {
        popup.hidden = false;
        const ta = form.querySelector('textarea');
        if (ta) ta.focus();
    }, DELAY_MS);

    // Закрытие — крестик, клик по фону, Escape.
    popup.querySelectorAll('[data-close]').forEach(el => {
        el.addEventListener('click', close);
    });
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !popup.hidden) close();
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const ta = form.querySelector('textarea');
        if (!ta.value.trim()) {
            ta.focus();
            return;
        }
        thanks.hidden = false;
        form.reset();
        // через 1.5 секунды закрываем
        setTimeout(close, 1500);
    });

    function close() {
        popup.hidden = true;
        thanks.hidden = true;
    }
})();
