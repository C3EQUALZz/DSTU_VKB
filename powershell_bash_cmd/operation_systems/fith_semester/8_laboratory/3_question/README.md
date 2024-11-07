## Настроить dash-панель через ~/.config/dconf и задать иконку учетной записи.

Я надеюсь, что Вы не перешли далее. Теперь нам в терминале надо будет настроить dash панель. 

1. Скачайте в случае Gnome расширения. 

```bash
sudo apt install gnome-shell-extensions
```

2. Я нашел готовый проект на GitHub, где есть настройка `dash-to-panel`. Выберу просто там параметры. 

```bash
sudo apt install git
sudo apt install make
sudo apt install gettext

git clone https://github.com/home-sweet-gnome/dash-to-panel.git
cd dash-to-panel
make install
```

У меня не получается настроить dash-панель через ~/.config/dconf и задать иконку учетной записи. Только есть вариант в тестовом режиме настроить и показать. 

В конце пропишем очистим

```bash
apt autoremove && apt clean && apt autoclean
```