## Просмотрите список используемых ключей. Сколько свободных слотов для ключей присутствует?

> [!IMPORTANT]
> Для выполнения задания я использовал я использовал терминал, который открывается через приложение `Konsole`.
> Ожидается, что до этого вы выполнили прошлые задания. 

Для просмотра списка используемых ключей используйте команду, которая представлена ниже: 

```bash
sudo cryptsetup luksDump /dev/sdb4
```

Далее, чтобы узнать количество, у Вас будет параметр `Keyslots`. Вот там вы глазками уже смотрите. Представлю на фото ниже какой у меня результат. 

![изображение](https://github.com/user-attachments/assets/971eca5e-9829-463d-91d1-731480b5eb92)

