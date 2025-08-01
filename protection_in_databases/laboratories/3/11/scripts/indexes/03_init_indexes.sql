-- Добавляем колонку id, если её нет
ALTER TABLE istudents.mark ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;

-- Создаём индекс для tmark_fk
CREATE INDEX IF NOT EXISTS idx_tmark_fk ON istudents.mark(tmark_fk);

-- Создаём индекс для plyear
CREATE INDEX IF NOT EXISTS idx_plyear ON istudents.mark(plyear);

-- Создаем первичный ключ
ALTER TABLE istudents.studplan
ADD PRIMARY KEY (id);