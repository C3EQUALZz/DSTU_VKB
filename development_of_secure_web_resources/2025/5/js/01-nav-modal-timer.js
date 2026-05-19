// Задания 1–3 (одна страница):
//   * Задание 1 — hover-эффекты у пунктов меню реализованы средствами CSS
//     (через transition + transform: scale), JS не требуется.
//   * Задание 2 — модальная форма регистрации с валидацией.
//   * Задание 3 — таймер обратного отсчёта.

(function () {
    'use strict';

    /* ============================================================
     *  Задание 2: модальная форма регистрации
     * ============================================================ */
    const modal = document.getElementById('modal');
    const openBtn = document.getElementById('open-register');
    const form = document.getElementById('register-form');
    const successMsg = document.getElementById('modal-success');

    openBtn.addEventListener('click', function (event) {
        event.preventDefault();
        openModal();
    });

    modal.querySelectorAll('[data-close]').forEach(el => {
        el.addEventListener('click', closeModal);
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !modal.hidden) {
            closeModal();
        }
    });

    function openModal() {
        modal.hidden = false;
        modal.setAttribute('aria-hidden', 'false');
        const firstInput = form.querySelector('input');
        if (firstInput) firstInput.focus();
    }

    function closeModal() {
        modal.hidden = true;
        modal.setAttribute('aria-hidden', 'true');
        successMsg.hidden = true;
    }

    /* ---- Валидация email по упрощённому RFC 5321 ---- */
    function validateEmail(value) {
        if (!value) return 'Email обязателен';
        if (value.length > 254) return 'Email длиннее 254 символов';

        const atIdx = value.indexOf('@');
        if (atIdx < 0 || value.indexOf('@', atIdx + 1) >= 0) return 'Должен быть ровно один @';

        const local = value.slice(0, atIdx);
        const domain = value.slice(atIdx + 1);

        if (!local || local.length > 64) return 'Локальная часть пустая или длиннее 64';
        if (!domain || domain.length > 255) return 'Домен пустой или длиннее 255';
        if (/\.{2,}/.test(value)) return 'Точки не должны идти подряд';
        if (value.startsWith('.') || value.endsWith('.')) return 'Не должно начинаться/заканчиваться точкой';

        const labels = domain.split('.');
        if (labels.length < 2) return 'У домена должна быть хотя бы одна точка';
        const tld = labels[labels.length - 1];
        if (tld.length < 2 || tld.length > 63) return 'TLD должен быть длиной 2…63';

        const allowedLocal = /^[A-Za-z0-9._%+\-]+$/;
        if (!allowedLocal.test(local)) return 'В локальной части недопустимые символы';
        const allowedDomain = /^[A-Za-z0-9.\-]+$/;
        if (!allowedDomain.test(domain)) return 'В домене недопустимые символы';

        return '';
    }

    /* ---- Валидация пароля ---- */
    function validatePassword(value) {
        if (!value) return 'Пароль обязателен';
        if (value.length < 12) return 'Пароль должен быть не короче 12 символов';
        if (!/[a-zа-яё]/.test(value) || !/[A-ZА-ЯЁ]/.test(value)) return 'Нужны буквы разного регистра';
        if (!/[0-9]/.test(value)) return 'Нужна хотя бы одна цифра';
        if (!/[!@#$%^&*]/.test(value)) return 'Нужен хотя бы один спецсимвол из !@#$%^&*';
        return '';
    }

    function validateName(value) {
        if (!value) return 'Имя обязательно';
        if (value.length < 2) return 'Имя должно быть длиннее 1 символа';
        return '';
    }

    function showError(field, msg) {
        const input = form.elements[field];
        const note = form.querySelector(`.field-error[data-for="${field}"]`);
        if (msg) {
            input.classList.add('is-invalid');
            note.textContent = msg;
        } else {
            input.classList.remove('is-invalid');
            note.textContent = '';
        }
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        successMsg.hidden = true;

        const name = form.elements.name.value.trim();
        const email = form.elements.email.value.trim();
        const password = form.elements.password.value;

        const errors = {
            name: validateName(name),
            email: validateEmail(email),
            password: validatePassword(password),
        };

        let hasError = false;
        for (const field of Object.keys(errors)) {
            showError(field, errors[field]);
            if (errors[field]) hasError = true;
        }
        if (!hasError) {
            successMsg.hidden = false;
            form.reset();
        }
    });

    /* ============================================================
     *  Задание 3: таймер обратного отсчёта
     * ============================================================ */
    const input = document.getElementById('timer-seconds');
    const display = document.getElementById('timer-display');
    const message = document.getElementById('timer-message');
    const startBtn = document.getElementById('timer-start');
    const pauseBtn = document.getElementById('timer-pause');
    const resetBtn = document.getElementById('timer-reset');

    let remaining = Number(input.value);
    let timerId = null;

    renderDisplay();

    input.addEventListener('input', function () {
        if (timerId) return;
        const v = Math.max(1, Math.min(3600, Number(input.value) || 0));
        input.value = v;
        remaining = v;
        renderDisplay();
    });

    startBtn.addEventListener('click', function () {
        if (timerId) return;
        if (remaining <= 0) remaining = Number(input.value) || 60;

        input.disabled = true;
        message.textContent = 'Идёт отсчёт…';
        message.classList.remove('is-done');

        timerId = setInterval(() => {
            remaining--;
            renderDisplay();
            if (remaining <= 0) {
                stop();
                display.classList.add('is-done');
                message.textContent = 'Время вышло!';
                message.classList.add('is-done');
            }
        }, 1000);
    });

    pauseBtn.addEventListener('click', function () {
        if (!timerId) return;
        stop();
        message.textContent = 'Пауза. Нажмите «Запустить» чтобы продолжить.';
    });

    resetBtn.addEventListener('click', function () {
        stop();
        remaining = Number(input.value) || 60;
        input.disabled = false;
        display.classList.remove('is-done');
        message.classList.remove('is-done');
        message.textContent = '';
        renderDisplay();
    });

    function stop() {
        if (timerId) { clearInterval(timerId); timerId = null; }
        input.disabled = false;
    }

    function renderDisplay() {
        const m = String(Math.floor(remaining / 60)).padStart(2, '0');
        const s = String(remaining % 60).padStart(2, '0');
        display.textContent = `${m}:${s}`;
    }
})();
