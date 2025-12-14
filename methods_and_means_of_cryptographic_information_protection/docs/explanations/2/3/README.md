# Лабораторная работа 3

> [!NOTE]
> Ниже описаны гайды для запуска алгоритмов через `cli`. Я лично использую `Powershell` в `Pycharm`. 

```bash
python -m cryptography_methods.cli zero-knowledge-proof execute -i 10 -b 256
```

Для запуска с провальным можно использовать:

```bash
python -m cryptography_methods.cli zero-knowledge-proof execute -i 10 -b 256 --test-failure
```