## Скопировать файл /etc/group в каталоги 1, 2, 3 и 4 используя абсолютные имена копируемого файла и каталога назначения.

Опять-таки поменяйте только папки на свою фамилию

```bash
mkdir -p ./Kovalev/1/{2,3} ./Kovalev/4
sudo cp /etc/group ./Kovalev/1/group
sudo cp /etc/group ./Kovalev/1/2/group
sudo cp /etc/group ./Kovalev/1/3/group
sudo cp /etc/group ./Kovalev/4/group
```