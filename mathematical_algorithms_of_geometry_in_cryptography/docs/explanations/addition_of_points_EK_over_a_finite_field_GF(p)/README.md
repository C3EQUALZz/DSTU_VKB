# Сложение точек ЭК над конечным полем GF(p)

> [!IMPORTANT]
> Перейдите в директорию с файлом `cli.py` в терминале. `cd src/mathematical_algorithms_of_geometry_in_cryptography`

Для запуска варианта 1 можно использовать команду, которая представлена ниже:

- 1. Генерация кривой и поиск всех точек

```bash
python -m mathematical_algorithms_of_geometry_in_cryptography.cli elliptic-curve-gfp generate -a 1 -b 2 -p 17
```
> [!NOTE]
> - Создаст эллиптическую кривую y² = x³ + 1x + 2 над GF(17)
> - Найдет все точки на кривой
> - Выведет таблицу со всеми точками и порядок кривой

- 2. Сложение точек P + Q

```bash
python -m mathematical_algorithms_of_geometry_in_cryptography.cli elliptic-curve-gfp add -a 1 -b 2 -p 17 --px 3 --py 7 --qx 5 --qy 9
```

> [!NOTE]
> - Создаст кривую с параметрами a=1, b=2, p=17
> - Проверит, что точки P=(3,7) и Q=(5,9) принадлежат кривой
> - Вычислит P + Q
> - Выведет результат

- 3. Удвоение точки 2P

```bash
python -m mathematical_algorithms_of_geometry_in_cryptography.cli elliptic-curve-gfp double -a 1 -b 2 -p 17 --px 3 --py 7
```

> [!NOTE]
> - Создаст кривую с параметрами a=1, b=2, p=17
> - Проверит, что точка P=(3,7) принадлежит кривой
> - Вычислит 2P
> - Выведет результат

## Справка по командам:

```bash
# Показать все доступные команды
python -m mathematical_algorithms_of_geometry_in_cryptography.cli --help

# Показать команды для эллиптических кривых над GF(p)
python -m mathematical_algorithms_of_geometry_in_cryptography.cli elliptic-curve-gfp --help

# Справка по конкретной команде
python -m mathematical_algorithms_of_geometry_in_cryptography.cli elliptic-curve-gfp generate --help
python -m mathematical_algorithms_of_geometry_in_cryptography.cli elliptic-curve-gfp add --help
python -m mathematical_algorithms_of_geometry_in_cryptography.cli elliptic-curve-gfp double --help
```

