// Задача 4. Угадай число.
// if / else if / else.
(function () {
    'use strict';

    const SECRET = 7;   // загаданное число от 1 до 10

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');

        const raw = prompt('Загадано число от 1 до 10. Введите ваш вариант:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        const guess = Number(raw.trim());
        if (raw.trim() === '' || !Number.isInteger(guess)) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите целое число.';
            return;
        }
        if (guess < 1 || guess > 10) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: число должно быть от 1 до 10.';
            return;
        }

        let message;
        if (guess > SECRET) {
            message = 'Ваше число больше загаданного';
        } else if (guess < SECRET) {
            message = 'Ваше число меньше загаданного';
        } else {
            message = 'Вы угадали!';
        }

        output.textContent = `Ваш ввод: ${guess}\n${message}`;
    });
})();
