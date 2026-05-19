// Задача 2. Количество чётных чисел в массиве.
// Цикл for + условие if.
(function () {
    'use strict';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');

        const raw = prompt('Введите числа через запятую:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        const parts = raw.split(',').map(s => s.trim()).filter(s => s !== '');
        const numbers = parts.map(Number);

        if (numbers.length === 0 || numbers.some(Number.isNaN)) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите числа через запятую.';
            return;
        }

        let count = 0;
        for (let i = 0; i < numbers.length; i++) {
            if (numbers[i] % 2 === 0) {
                count++;
            }
        }

        output.textContent =
            `Массив: [${numbers.join(', ')}]\n` +
            `Количество чётных чисел: ${count}`;
    });
})();
