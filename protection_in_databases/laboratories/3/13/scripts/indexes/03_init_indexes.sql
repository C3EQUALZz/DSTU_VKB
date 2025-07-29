-- Добавляем колонку id, если её нет
ALTER TABLE istudents.mark ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;

-- Создаём индекс для tmark_fk
CREATE INDEX IF NOT EXISTS idx_tmark_fk ON istudents.mark(tmark_fk);

-- Создаём индекс для plyear
CREATE INDEX IF NOT EXISTS idx_plyear ON istudents.mark(plyear);

-- Создаем первичный ключ
ALTER TABLE istudents.studplan
ADD PRIMARY KEY (id);

-- Создаем внешний ключ
ALTER TABLE istudents.mark
ADD CONSTRAINT fk_mark_studplan
FOREIGN KEY (studplan_fk)
REFERENCES istudents.studplan(id);

-- Создаем индекс
CREATE INDEX CONCURRENTLY idx_mark_studplan_fk
ON istudents.mark (studplan_fk)