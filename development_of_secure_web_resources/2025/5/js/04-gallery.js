// Задание 4. Галерея с превью.
// События: mouseenter, mouseleave, mousemove.
(function () {
    'use strict';

    const thumbs = document.querySelectorAll('.thumb');
    const preview = document.getElementById('preview');
    const inner = preview.querySelector('.preview__inner');

    thumbs.forEach(thumb => {
        thumb.addEventListener('mouseenter', function () {
            // Клонируем SVG из миниатюры в превью.
            inner.innerHTML = '';
            const svg = thumb.querySelector('svg').cloneNode(true);
            inner.appendChild(svg);
            preview.hidden = false;
        });

        thumb.addEventListener('mouseleave', function () {
            preview.hidden = true;
        });

        thumb.addEventListener('mousemove', function (event) {
            const padding = 18;
            const previewWidth = 260;
            const previewHeight = 260;

            let x = event.clientX + padding;
            let y = event.clientY + padding;

            // Сдвигаем превью, если оно вышло бы за пределы окна.
            if (x + previewWidth > window.innerWidth) {
                x = event.clientX - previewWidth - padding;
            }
            if (y + previewHeight > window.innerHeight) {
                y = event.clientY - previewHeight - padding;
            }

            preview.style.left = `${x}px`;
            preview.style.top = `${y}px`;
        });
    });
})();
