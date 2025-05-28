# Создать в таблице `istudents.mark` первичный ключ (`id`) и создать индекс для поля `tmark_fk`


```postgresql
-- Добавляем колонку id, если её нет
ALTER TABLE istudents.mark ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;

-- Создаём индекс для tmark_fk
CREATE INDEX IF NOT EXISTS idx_tmark_fk ON istudents.mark(tmark_fk);
```