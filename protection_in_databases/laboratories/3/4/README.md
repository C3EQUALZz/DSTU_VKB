# Создать в таблице `istudents.mark` первичный ключ (`id`) и создать индекс для поля `tmark_fk`.

Был просто создан файл `03_init_indexes.sql`, с помощью которого создается индекс.
Практическое применение и измерение находится в следующей директории. 

```postgresql
-- Добавляем колонку id, если её нет
ALTER TABLE istudents.mark ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;

-- Создаём индекс для tmark_fk
CREATE INDEX IF NOT EXISTS idx_tmark_fk ON istudents.mark(tmark_fk);
```