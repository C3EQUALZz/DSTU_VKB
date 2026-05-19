// Задача 10. Подсчёт гласных букв русского алфавита.
// for-of + проверка на вхождение в строку.
(function () {
    'use strict';

    const VOWELS = 'аеёиоуыэюя';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');

        const raw = prompt('Введите строку:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        if (raw.length === 0) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите хотя бы один символ.';
            return;
        }

        let count = 0;
        for (const ch of raw.toLowerCase()) {
            if (VOWELS.includes(ch)) {
                count++;
            }
        }

        output.textContent =
            `Строка: "${raw}"\n` +
            `Количество гласных: ${count}`;
    });
})();
