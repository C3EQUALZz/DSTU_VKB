// Задача 6. Слова длиной >= 5 символов.
// for + push.
(function () {
    'use strict';

    const runButton = document.getElementById('run');
    const output = document.getElementById('output');

    runButton.addEventListener('click', function () {
        output.classList.remove('is-error');
        output.innerHTML = '';

        const raw = prompt('Введите слова через пробел:');
        if (raw === null) { output.textContent = 'Ввод отменён.'; return; }

        const words = raw.trim().split(/\s+/).filter(Boolean);
        if (words.length === 0) {
            output.classList.add('is-error');
            output.textContent = 'Ошибка: введите хотя бы одно слово.';
            return;
        }

        const longWords = [];
        for (let i = 0; i < words.length; i++) {
            if (words[i].length >= 5) {
                longWords.push(words[i]);
            }
        }

        if (longWords.length === 0) {
            output.textContent = 'Слова длиной ≥ 5 символов не найдены.';
            return;
        }

        const ul = document.createElement('ul');
        for (const word of longWords) {
            const li = document.createElement('li');
            li.textContent = word;
            ul.appendChild(li);
        }

        const header = document.createElement('p');
        header.textContent = `Найдено слов длиной ≥ 5 символов: ${longWords.length}`;
        output.appendChild(header);
        output.appendChild(ul);

        const inline = document.createElement('p');
        inline.style.marginTop = '.6em';
        inline.style.color = '#475569';
        inline.textContent = `Через запятую: ${longWords.join(', ')}`;
        output.appendChild(inline);
    });
})();
