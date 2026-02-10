# Лабораторная работа 3

> [!NOTE]
> Ниже описаны гайды для запуска алгоритмов через `cli`. Я лично использую `Powershell` в `Pycharm`. 

```bash
python -m cryptography_methods.cli zero-knowledge-proof execute -i 10 -b 256
```

Для параллельного запуска:

```bash
python -m cryptography_methods.cli zero-knowledge-proof parallel -t 4 -k 5
```

Для запуска с провальным можно использовать:

```bash
python -m cryptography_methods.cli zero-knowledge-proof execute -i 10 -b 256 --test-failure
```

Для запуска с провальным можно использовать: 

```bash
python -m cryptography_methods.cli zero-knowledge-proof parallel -t 4 -k 5 --test-failure
```