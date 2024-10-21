## Теория информации

Здесь расположены реализации лабораторных работ на 2024 - 2025 год. Каждый год лабораторные меняются по порядку и содержимому. 
Не надейтесь, что у Вас будет то же самое, так как минимум лекторы меняются каждый год у ВКБ. 

Здесь в лабораторных требуется интерфейс, а Python в случае написания интерфейсов - полная шляпа. Поэтому решил делать full stack web.

Из технологий: 

- `FastAPI`
- `ReactJS`
- `react-router-dom`
- `save-file`
- `AntD`
- `Vite`
- `nodejs`
- `Redis`
- `Python 3.11`

---

### Создание виртуального окружения и загрузка зависимостей для Python

В корне проекта пропишите команду

```bash
python -m venv venv
```

Теперь активируйте venv

- `Windows` - `venv\Scripts\activate.bat`
- `Linux / MacOS` - `source venv/bin/activate`

У вас в терминале должна появится надпись `(.venv)`. Место расположения зависит от конфигурации вашей командной строки. 

Теперь установка зависимостей

```bash
cd ./combined_languages/theory_of_information/backend
pip install -r requirements.txt
```

### Настройка окружения для nodejs

```bash
cd ./combined_languages/theory_of_information/frontend
npm i
```

---

### Запуск backend: 

Вы должны находиться в папке `DSTU_VKB` - корень проекта, а дальше запускать через консоль, используя команду ниже

```bash
uvicorn combined_languages.theory_of_information.backend.main:app --reload --port 8002
```

### Запуск frontend:

Вы должны находиться в папке `combined_languages/theory_of_information/frontend`, а потом запускаете через консоль, используя команду ниже

```bash
npm run dev
```

---

### Логика лабораторных работ

Для каждой лабораторной есть такая логика: 
- Model - задача лабораторной работы 
- Router - backend часть для лабораторной
- Page - frontend страница лабораторной 


> [NOTE!]
> Это первый опыт автора написания backend и frontend, тут достаточно много говнокода.
> Я знаю, что многое можно улучшить, добавив IoC, использовать подход DDD, но я слишком поздно узнал, а рефачить не хочется. 

