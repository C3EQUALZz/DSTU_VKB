## В ОССН версии 1.6 создать учётную запись пользователя `user`, с параметрами: максимальный и минимальный уровни доступа — 0, неиерархические категории — нет, уровень целостности — «Высокий», входит в группу администраторов — `astra-admin` (вторичная группа), разрешено выполнение привилегированных команд (`sudo`). Войти в ОССН с учётной записью пользователя user (Уровень_0, «Высокий»).

> [!IMPORTANT]
> Для выполнения данного задания я использовал `GUI`. 

Проверим, что у вас есть группа `astra admin`. Для начала перейдите в Параметры -> Пользователи и группы (вниз пролистайте) -> Группы.

![изображение](https://github.com/user-attachments/assets/31a63a36-7fc5-4a51-acb4-fcb9ad7acf25)

Теперь, если у вас нет группы `astra admin`, то создайте её. 
Смотрите на фото ниже для примера вам. 

![изображение](https://github.com/user-attachments/assets/c3bdef78-1f2f-4a71-846b-d872e4dd358b)

> [!NOTE]
> Группа по умолчанию у меня была с самого начала установки системы. Я вручную не создавал

Теперь перейдем к созданию пользователя `user`. Для начала перейдите в Параметры -> Пользователи и группы (вниз пролистайте) -> Пользователи. Теперь нам нужно создать пользователя `user`. 
Выставите ему такие параметры, как показано ниже:

- Макс. уровень доступа - 0
- Мин. уровень доступа - 0
- Уровень целостности - Высокий
- Входит в группу админтистраторов (вторичная группа) - `astra-admin`, `sudo`

В результате в GUI настройка выглядела у меня так:

![изображение](https://github.com/user-attachments/assets/c054700d-6b7e-4a6c-9a9c-51f1f2900711)

> [!NOTE]
> Я для удобства поставил пароль `1234`. 

Теперь вам остается войти под `user` (Уровень_0, Высокий). 
