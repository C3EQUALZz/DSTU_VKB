// Задача 3. Сумма положительных чисел.
// Цикл for-of + условие if.
(function () {
    'use strict';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');

        const raw = prompt('Введите числа через пробел:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        const parts = raw.trim().split(/\s+/).filter(Boolean);
        const numbers = parts.map(s => Number(s.replace(',', '.')));

        if (numbers.length === 0 || numbers.some(Number.isNaN)) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите числа через пробел.';
            return;
        }

        let sum = 0;
        for (const n of numbers) {
            if (n > 0) sum += n;
        }

        output.textContent =
            `Числа: [${numbers.join(', ')}]\n` +
            `Сумма положительных чисел: ${sum}`;
    });
})();
