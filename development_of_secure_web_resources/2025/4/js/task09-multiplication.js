// Задача 9. Таблица умножения.
// Цикл for от 1 до 10.
(function () {
    'use strict';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');
        output.innerHTML = '';

        const raw = prompt('Введите число, для которого построить таблицу умножения:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        const n = Number(raw.trim());
        if (raw.trim() === '' || Number.isNaN(n)) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите число.';
            return;
        }

        const header = document.createElement('p');
        header.style.marginTop = '0';
        header.innerHTML = `<strong>Таблица умножения на ${n}:</strong>`;
        output.appendChild(header);

        const lines = [];
        for (let i = 1; i <= 10; i++) {
            lines.push(`${n} × ${i} = ${n * i}`);
        }
        output.insertAdjacentHTML('beforeend', lines.join('<br>'));
    });
})();
