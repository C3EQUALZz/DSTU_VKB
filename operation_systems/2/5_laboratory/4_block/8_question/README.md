## Чтобы не подключать `swap`-файл или `swap`-раздел каждый раз, добавьте соответствующую запись в `/etc/fstab`: `# vi /etc/fstab` `/dev/sdc3 none swap sw 0 0` `/swapfile none swap sw 0 0`

> [!IMPORTANT]
> Для выполнения данного задания я использовал терминал, который открывается через терминал `Konsole`.

Выполните команду ниже для изменения файла:

```bash
sudo nano /etc/fstab
```

Теперь добавим эти строки в файл: 

```bash
/dev/sdd3 none swap sw 0 0
/swapfile none swap sw 0 0
```

