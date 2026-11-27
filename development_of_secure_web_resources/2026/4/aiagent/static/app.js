// История существует только в этой вкладке и исчезает после перезагрузки.
const history = [];
const messages = document.querySelector('#messages');
const form = document.querySelector('#chat-form');
const question = document.querySelector('#question');
const send = document.querySelector('#send');
const clear = document.querySelector('#clear-chat');
const status = document.querySelector('#chat-status');
const suggestions = document.querySelectorAll('[data-question]');
let busy = false;

function element(tag, className, text) {
  const node = document.createElement(tag);
  node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function addMessage(role, text) {
  const node = element('div', `message ${role}`);
  node.append(element('span', 'message-label', role === 'user' ? 'ВЫ' : 'КОНСУЛЬТАНТ'));
  node.append(document.createTextNode(text));
  messages.append(node);
  messages.scrollTop = messages.scrollHeight;
}

function resetChat() {
  history.length = 0;
  messages.replaceChildren();
  addMessage('assistant', 'Привет! Помогу выбрать курс. Что вы хотите научиться делать и есть ли у вас опыт программирования?');
  status.textContent = '';
  status.className = 'chat-status';
  question.value = '';
  updateCounter();
}

function updateCounter() {
  document.querySelector('#char-count').textContent = `${question.value.length} / 2000`;
}

function setBusy(value) {
  busy = value;
  send.disabled = value;
  clear.disabled = value;
  question.disabled = value;
  suggestions.forEach(button => { button.disabled = value; });
  messages.setAttribute('aria-busy', String(value));
}

async function getJSON(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(typeof data.detail === 'string' ? data.detail : 'Не удалось выполнить запрос. Проверьте введенные данные.');
  }
  return data;
}

async function loadCourses() {
  const container = document.querySelector('#courses');
  try {
    const courses = await getJSON('/api/courses');
    container.replaceChildren();
    courses.forEach((course, index) => {
      const card = element('article', 'course');
      const top = element('div', 'course-top');
      top.append(element('span', 'course-number', `0${index + 1} / КУРС`));
      top.append(element('span', 'course-icon', ['py', '</>', '{ai}'][index]));
      card.append(top, element('h3', '', course.title), element('p', 'course-description', course.description));
      const duration = element('div', 'duration');
      duration.append(element('span', '', `${course.duration_weeks} нед.`), element('span', '', `${course.duration_hours} часов`));
      const topics = element('ul', 'topics');
      course.topics.forEach(topic => topics.append(element('li', '', topic)));
      const bottom = element('div', 'course-bottom');
      bottom.append(element('span', 'price', new Intl.NumberFormat('ru-RU', {style: 'currency', currency: course.currency, maximumFractionDigits: 0}).format(course.price)));
      const button = element('button', 'course-button', 'Спросить о курсе ↗');
      button.type = 'button';
      button.addEventListener('click', () => {
        document.querySelector('#consultant').scrollIntoView({behavior: 'smooth'});
        if (!busy) {
          question.value = `Расскажи о курсе «${course.title}».`;
          updateCounter();
          question.focus();
        }
      });
      bottom.append(button);
      card.append(duration, topics, bottom);
      container.append(card);
    });
  } catch {
    container.replaceChildren(element('p', '', 'Не удалось загрузить курсы. Обновите страницу, чтобы повторить.'));
  }
}

async function loadTerms() {
  const container = document.querySelector('#terms');
  try {
    const terms = await getJSON('/api/terms');
    container.append(element('span', '', terms.format), element('span', '', terms.access));
    container.append(element('span', '', terms.duration_note));
    container.append(element('span', '', `Условные способы оплаты: ${terms.payment_methods.join(', ')}.`));
    container.append(element('span', 'payment-note', terms.payment_note));
  } catch {
    container.textContent = 'Условия не загрузились. Учебная демонстрация: реальные платежи и заказы не принимаются.';
  }
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  const text = question.value.trim();
  if (busy || !text) return;
  if (text.length > 2000) {
    status.textContent = 'Вопрос должен быть не длиннее 2000 символов.';
    return;
  }
  setBusy(true);
  status.className = 'chat-status';
  status.textContent = 'Консультант готовит ответ…';
  // Добавляем в историю только завершенную пару: при ошибке вопрос можно повторить.
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 45000);
  try {
    const data = await getJSON('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      signal: controller.signal,
      body: JSON.stringify({messages: [
        ...history.slice(-19).map(message => ({...message, content: message.content.slice(0, 2000)})),
        {role: 'user', content: text},
      ]}),
    });
    history.push({role: 'user', content: text}, {role: 'assistant', content: data.answer});
    addMessage('user', text);
    addMessage('assistant', data.answer);
    question.value = '';
    updateCounter();
    status.textContent = '';
  } catch (error) {
    status.className = 'chat-status error';
    status.textContent = error.name === 'AbortError'
      ? 'Ответ задерживается. Нажмите отправить, чтобы повторить.'
      : error instanceof TypeError ? 'Нет связи с сервером. Повторите запрос.' : error.message;
  } finally {
    clearTimeout(timeout);
    setBusy(false);
    question.focus();
  }
});

clear.addEventListener('click', () => { resetChat(); question.focus(); });
question.addEventListener('input', updateCounter);
question.addEventListener('keydown', event => {
  if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    form.requestSubmit();
  }
});
suggestions.forEach(button => button.addEventListener('click', () => {
  question.value = button.dataset.question;
  updateCounter();
  question.focus();
}));
resetChat();
loadCourses();
loadTerms();
