## Для настройки привилегий учётных записей пользователей осуществить следующие действия: -вывести в терминал заданные в ОССН привилегии учётных записей пользователей командой usercaps, при работе в терминале Fly в «привилегированном» режиме; -запустить графическую утилиту «Политика безопасности» и открыть настройки учётной записи пользователя user1, в вкладке «Привилегии» установить Linux-привилегии cap_kill, cap_fowner и PARSEC-привилегии parsec_cap_chmac, parsec_cap_sig, после чего закончить работу с утилитой; -вывести привилегии учётной записи пользователя user1 командой usercaps user1;
-в графической утилите «Политика безопасности» открыть параметры
учётной записи пользователя user, в вкладке «Привилегии» выбрать Linux-
привилегии cap_kill,
cap_fowner и PARSEC-привилегии parsec_cap_chmac, parsec_cap_sig;
156
-запустить терминал Fly в «непривилегированном» режиме командой
fly-term и осуществить попытку запуска команды usercaps;
-определить расположение файла usercaps командой which usercaps,
выполненной из «привилегированного» режима, а затем выполнить в
«непривилегированном» режиме команду /usr/sbin/usercaps, проанализировать
результат;
-запустить терминал Fly в «привилегированном» режиме командой sudo
fly-term и выполнить модификацию Linux-привилегий и PARSEC-привилегий
командами:
usercaps -l 9 user1
usercaps -m 2 user1
usercaps -m 11 user1
-с использованием графической утилиты «Политика безопасности»
определить установленные привилегии и формат параметра модификации
привилегий учётных записей пользователей (десятичная, восьмеричная или
шестнадцатеричная система счисления при этом используется?);
-установить для учётной записи пользователя user1 полный список
привилегий командой usercaps -f user1, затем удалить все привилегии учётной
записи пользователя user1 командой usercaps -z user1;
-вывести списки Linux-привилегий и PARSEC-привилегий командами
usercaps -L и usercaps -M, соответственно

Вывести привилегии учётных записей пользователей:

```bash
sudo usercaps
```

Настройка привилегий для пользователя `user1` через графическую утилиту:
- Запустить «Политика безопасности».
- Открыть настройки учётной записи `user1`.
- Во вкладке «Привилегии» установить Linux-привилегии `cap_kill`, `cap_fowner` и PARSEC-привилегии `parsec_cap_chmac`, `parsec_cap_sig`.

Вывести привилегии учётной записи пользователя user1:

```bash
usercaps user1
```

**Настройка привилегий для пользователя `user`**:
   - Аналогично настроить привилегии для `user` через графическую утилиту. 
