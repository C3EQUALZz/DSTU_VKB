// Задача 5. Поиск максимума.
// Явный цикл for + условный оператор.
(function () {
    'use strict';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');

        const raw = prompt('Введите числа через запятую:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        const parts = raw.split(',').map(s => s.trim()).filter(Boolean);
        const numbers = parts.map(Number);

        if (numbers.length === 0 || numbers.some(Number.isNaN)) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите числа через запятую.';
            return;
        }

        let max = numbers[0];
        for (let i = 1; i < numbers.length; i++) {
            if (numbers[i] > max) {
                max = numbers[i];
            }
        }

        output.textContent =
            `Массив: [${numbers.join(', ')}]\n` +
            `Максимальное число: ${max}`;
    });
})();
