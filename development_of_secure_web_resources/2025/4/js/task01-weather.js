// Задача 1. Оценка погоды для одежды.
// Ветвящийся алгоритм: if / else if / else.
(function () {
    'use strict';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');

        const raw = prompt('Введите температуру (°C):');
        if (raw === null) {
            output.textContent = 'Ввод отменён.';
            return;
        }

        const temperature = Number(raw.trim().replace(',', '.'));
        if (raw.trim() === '' || Number.isNaN(temperature)) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите число.';
            return;
        }

        let advice;
        if (temperature < 0) {
            advice = 'Нужно одевать тёплую куртку';
        } else if (temperature <= 20) {
            advice = 'Можно обойтись лёгкой курткой';
        } else {
            advice = 'Можно идти в футболке';
        }

        output.textContent = `Температура: ${temperature}°C\n${advice}`;
    });
})();
