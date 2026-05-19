// Задача 7. Подсчёт чисел, делящихся на 3.
// Цикл while + условие.
(function () {
    'use strict';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');

        const raw = prompt('Введите числа через пробел:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        const parts = raw.trim().split(/\s+/).filter(Boolean);
        const numbers = parts.map(Number);

        if (numbers.length === 0 || numbers.some(Number.isNaN)) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите числа через пробел.';
            return;
        }

        let count = 0;
        let i = 0;
        while (i < numbers.length) {
            if (numbers[i] % 3 === 0) count++;
            i++;
        }

        output.textContent =
            `Числа: [${numbers.join(', ')}]\n` +
            `Количество чисел, делящихся на 3: ${count}`;
    });
})();
