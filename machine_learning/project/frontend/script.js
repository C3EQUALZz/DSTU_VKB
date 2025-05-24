document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.art-card');
  let lockTimer;

  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      // Запускаем таймер на 5 секунд
      lockTimer = setTimeout(() => {
        card.classList.add('locked');
      }, 5000);
    });

    card.addEventListener('mouseleave', () => {
      // Отменяем фиксацию, если не прошло 5 секунд
      clearTimeout(lockTimer);
      if (!card.classList.contains('locked')) {
        card.classList.remove('hover');
      }
    });

    // Закрытие по клику
    card.addEventListener('click', (e) => {
      e.stopPropagation();
      card.classList.remove('locked');
    });
  });

  // Закрытие всех карточек при клике вне их
  document.addEventListener('click', () => {
    cards.forEach(card => {
      card.classList.remove('locked');
    });
  });
});