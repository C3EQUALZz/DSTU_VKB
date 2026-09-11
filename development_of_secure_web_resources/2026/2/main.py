class BacteriaProducer:
    """Колония с ограничением численности бактерий."""

    def __init__(self, max_bacteria):
        self.max_bacteria = max_bacteria
        self.current_bacteria_count = 0

    def create(self):
        if self.current_bacteria_count >= self.max_bacteria:
            print('Нет места под новую бактерию')
        else:
            self.current_bacteria_count += 1
            print(
                'Добавлена одна бактерия. Бактерий в колонии: '
                f'{self.current_bacteria_count}'
            )

    def delete(self):
        if self.current_bacteria_count == 0:
            print('В популяции нет бактерий, удалять нечего')
        else:
            self.current_bacteria_count -= 1
            print(
                'Одна бактерия удалена. Бактерий в колонии: '
                f'{self.current_bacteria_count}'
            )


if __name__ == '__main__':
    # Пример запуска для самопроверки из задания.
    bacteria_producer = BacteriaProducer(max_bacteria=3)
    bacteria_producer.delete()
    bacteria_producer.create()
    bacteria_producer.create()
    bacteria_producer.create()
    bacteria_producer.create()
    bacteria_producer.delete()
