## Создать резервную копию c помощью системных команд.

Здесь есть два способа создания резервной копии. Использовать dd и tar.

[Мануал как правильно это делать](https://askubuntu.com/questions/524418/how-would-i-use-tar-for-full-backup-and-restore-with-system-on-ssd-and-home-on-h)

Выберите путь, где у вас достаточно места для создания backup. В моем случае в home было достаточно места. 

```bash
cd /
sudo tar -cvpzf /home/c3equalz/backup.tar.gz --exclude=/proc --exclude=/dev --exclude=/sys --exclude=/tmp --exclude=/mnt --exclude=/media --exclude=/lost+found --exclude=/home/c3equalz/backup.tar.gz /
```

У меня в консоли появилась ошибка, судя по обзорам это нормальное явление, так как мы это делаем не в LiveCD, здесь некоторые процессы не дают доступ. 