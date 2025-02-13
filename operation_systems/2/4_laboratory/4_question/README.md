## Добавьте трех новых пользователей с соответствующими домашними директориями: `student7`, `student8`, `student9`. Задайте пароли для каждого из них

Создаем пользователя `student7`:

```bash
sudo useradd -m student7
```

Создаем пользователя `student8`:

```bash
sudo useradd -m student8
```

Создаем пользователя `student9`:

```bash
sudo useradd -m student9
```

Задаем пароль для `student7`:

```bash
sudo passwd student7
```

Задаем пароль для `student8`:

```bash
sudo passwd student8
```

Задаем пароль для `student9`:

```bash
sudo passwd student9
```

> [!NOTE]
> Не пугайтесь, что у Вас вылетело предупреждение. Система предупреждает, но не запрещает использовать данный пароль. Просто вбейте его ещё раз.
> Я, например, использовал пароль `123`. 

![изображение](https://github.com/user-attachments/assets/efa51c1d-4c1c-4ccb-b02c-eb1525fed79f)
