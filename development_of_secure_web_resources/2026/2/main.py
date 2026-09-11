class BacteriaProducer:
    # Допишите инициализатор класса:
    # Задайте два атрибута экземпляра:
    # Первый хранит максимальное количество бактерий
    # Второй хранит текущее количество бактерий (по умолчанию 0)
    def __init__(self, max_bacteria):
        self.max_bacteria =
        self.current_bacteria_count =

    # Допишите метод, добавляющий бактерию в чашу
    # Если уже достигнуто максимальное число бактерий,
    # то добавлять новую нельзя, выведите сообщение об ошибке
    def create(self):
        if ...
            ...
        else:
            ...

    # Допишите метод, удаляющий бактерию из чаши.
    # Если в чаше уже нет бактерий, то удалять нечего;
    # выведите сообщение об ошибке
    def delete(self):
        if ...
            ...
        else:
            ...


# Пример запуска для самопроверки
bacteria_producer = BacteriaProducer(max_bacteria=3)
bacteria_producer.delete()
bacteria_producer.create()
bacteria_producer.create()
bacteria_producer.create()
bacteria_producer.create()
bacteria_producer.delete()