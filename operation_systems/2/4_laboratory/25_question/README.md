## с помощью команды `chmod` установите права доступа 077 на созданный файл `quart1`. Вновь попробуйте прочесть его. Ответьте, почему владельцу файла запрещается доступ, если файл доступен для всех? Что необходимо сделать, чтобы вернуть владельцу права на доступ?

Открываем терминал через комбинацию (`CTRL + ALT + F<number>`), где `number` - это число от 1 до 6. Для выполнения команды используйте команду ниже: 

```bash
chmod 077 quart1
```

<details>
  <summary>Что обозначают цифры в команде?</summary>
  
  - Первая цифра `0`: это права для владельца. В данном случае она равна `0`, что означает, что специальные права не установлены.
  - Вторая цифра `7`: это права для группы. `7` в восьмеричном формате означает, что группа имеет все права: чтение (`4`) + запись (`2`) + исполнение (`1`) = `7`.
  - Третья цифра `7`: это права для других пользователей.

</details>

Выводы: Не получится прочитать его по тем причинам, потому что мы поставили `0` для владельца файла в команде `chmod`. Чтобы вернуть владельцу права на доступ, надо поставить `7` вместо `0`. 
