-- Тест 1: GIN индекс
EXPLAIN ANALYZE
SELECT * FROM clients
WHERE email_tsvector @@ to_tsquery('simple', 'protonmail');

-- Тест 2: GiST индекс
EXPLAIN ANALYZE
SELECT * FROM clients
WHERE email_tsvector @@ to_tsquery('simple', 'icloud');

-- Тест 3: SP-GiST индекс
EXPLAIN ANALYZE
SELECT * FROM clients
WHERE email_tsvector @@ to_tsquery('simple', 'hotmail');

-- Тест 4: B-tree индекс (для сравнения)
EXPLAIN ANALYZE
SELECT * FROM clients
WHERE email LIKE '%protonmail%';