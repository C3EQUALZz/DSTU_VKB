// Задача 8. Проверка возраста для доступа.
// if / else.
(function () {
    'use strict';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');

        const raw = prompt('Введите ваш возраст:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        const age = Number(raw.trim());
        if (raw.trim() === '' || !Number.isFinite(age) || age < 0) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите неотрицательное число.';
            return;
        }

        if (age >= 18) {
            output.textContent = `Возраст: ${age}\nДоступ разрешён`;
        } else {
            output.textContent = `Возраст: ${age}\nДоступ запрещён`;
        }
    });
})();
