## Создать резервную копию c помощью системных команд.

Здесь есть два способа создания резервной копии. Использовать dd и tar. 

Выберите путь, где у вас достаточно места для создания backup. В моем случае в home было достаточно места. 

```bash
cd /
sudo tar -cvpzf /home/c3equalz/backup.tar.gz --exclude=/proc --exclude=/dev --exclude=/sys --exclude=/tmp --exclude=/mnt --exclude=/media --exclude=/lost+found --exclude=/home/c3equalz/backup.tar.gz /
```



