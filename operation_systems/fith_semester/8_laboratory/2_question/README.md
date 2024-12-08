## Установить ПО и сделать необходимые настройки. 

1. Нажмите сверху зеленую кнопку `Next`, чтобы `Cubic` начал установку ISO, после этого он выдаст терминал, где вы будете настаривать зависимости. 


> [IMPORTANT!]
> У всех зависимости по условию должны быть разные в группе

Я покажу какие завимости я поставил. 

2. Обновите полностью все пакеты

```bash
apt update
```

3. Я удалил пакеты, которые не нужны мне. Для этого я использовал команду, которая представлена ниже

```bash
apt purge libreoffice* rhythmbox thunderbird pix* hexchat
```

4. Обновим полностью систему, чтобы не было конфликтов с пакетами. Linux любит регулярные обновления :D

```bash
apt upgrade
``` 

5. Поставим зависимости

```bash
apt install keepassxc shotwell vlc plank audacity pdfarranger curl picard goodvibes screenruler -y
```

6. Поставлю различные кодеки. А почему бы и нет? 

```bash
sudo add-apt-repository multiverse
sudo apt install ubuntu-restricted-extras
```

> [NOTE!]
> У вас появится там окошко, просто попробуйте стрелочками выбрать `Ok`. Когда кнопка будет красная, то нажмите `Enter`

