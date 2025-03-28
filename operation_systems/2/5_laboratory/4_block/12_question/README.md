## Также можно попробовать увеличить\уменьшить объём потребляемой системой памяти за счёт изменения размеров дискового кеша. Уровень выделяемой под кеш памяти хранится в `/proc/sys/vm/vfs_cache_pressure`. Значение по умолчанию: 100. Чтобы использовать меньше памяти под дисковые кеши (не желательно), поставьте значение 50. Если, наоборот, хочется больше отзывчивости системы, увеличьте размер кеша: `echo 1000 > /proc/sys/vm/vfs_cache_pressure`. Измените параметры до полного удовлетворения. Для того, чтобы настройки стали постоянными, занесите нужный параметр в файл `/etc/sysctl.conf` `vi /etc/sysctl.conf` `vm.vfs_cache_pressure = 1000`. Привести скриншот и пояснить работу данного пункта.

> [!IMPORTANT]
> Для выполнения данного задания я использовал терминал `Konsole`. 

Теперь используем команду для просмотра файла: 

```bash
sudo nano /etc/sysctl.conf
```

Теперь ставим данный параметр в файле: 

```bash
vm.vfs_cache_pressure = 1000
```

```bash
echo 1000 | sudo tee /proc/sys/vm/vfs_cache_pressure
sudo sysctl -w vm.vfs_cache_pressure=1000
```

Чтобы сделать эти настройки постоянными, добавьте соответствующие строки в файл `/etc/sysctl.conf`:

```bash
vm.swappiness=50
vm.vfs_cache_pressure=1000
```

После внесения изменений перезагрузите систему или выполните команду

```bash
sudo sysctl -p
```